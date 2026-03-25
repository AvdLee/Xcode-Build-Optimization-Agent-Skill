# Optimization Checks

This document describes every optimization check the agent skills perform, why each check matters for build time, and where to learn more. It is the developer-facing reference; implementation details live in the skill-level docs under `skills/*/references/`.

## Build Settings Audit

The `xcode-project-analyzer` audits project-level and target-level build settings against a curated best-practices checklist. Misconfigured settings are one of the most common causes of unnecessarily slow builds, especially in projects that have been migrated across Xcode versions.

**Debug configuration checks:**

| Setting | Key | Recommended | Why |
|---------|-----|-------------|-----|
| Compilation Mode | `SWIFT_COMPILATION_MODE` | `singlefile` | Recompiles only changed files instead of the entire target |
| Swift Optimization | `SWIFT_OPTIMIZATION_LEVEL` | `-Onone` | Optimization passes add compile time with no debug benefit |
| C/ObjC Optimization | `GCC_OPTIMIZATION_LEVEL` | `0` | Same rationale for C-family sources |
| Active Arch Only | `ONLY_ACTIVE_ARCH` | `YES` | Building all architectures doubles or triples compile and link time |
| Debug Info Format | `DEBUG_INFORMATION_FORMAT` | `dwarf` | `dwarf-with-dsym` generates a separate dSYM bundle, adding overhead |
| Testability | `ENABLE_TESTABILITY` | `YES` | Required for `@testable import`; minor overhead is expected |
| Compilation Conditions | `SWIFT_ACTIVE_COMPILATION_CONDITIONS` | includes `DEBUG` | Guards `#if DEBUG` code paths |
| Eager Linking | `EAGER_LINKING` | `YES` | Starts linking before all compilation finishes, reducing wall-clock time |

**Release configuration checks:**

| Setting | Key | Recommended | Why |
|---------|-----|-------------|-----|
| Compilation Mode | `SWIFT_COMPILATION_MODE` | `wholemodule` | Produces optimized runtime code |
| Swift Optimization | `SWIFT_OPTIMIZATION_LEVEL` | `-O` or `-Osize` | Optimized binaries for distribution |
| C/ObjC Optimization | `GCC_OPTIMIZATION_LEVEL` | `s` | Optimizes for size |
| Active Arch Only | `ONLY_ACTIVE_ARCH` | `NO` | Release must include all supported architectures |
| Debug Info Format | `DEBUG_INFORMATION_FORMAT` | `dwarf-with-dsym` | Required for crash symbolication |
| Testability | `ENABLE_TESTABILITY` | `NO` | Removes internal-symbol export overhead |

**General (all configurations) checks:**

| Setting | Key | Recommended | Why |
|---------|-----|-------------|-----|
| Compilation Caching | `COMPILATION_CACHING` | `YES` | Caches Swift and C-family compilation results; biggest wins on branch switching and clean builds |
| Integrated Swift Driver | `SWIFT_USE_INTEGRATED_DRIVER` | `YES` | Eliminates inter-process overhead for compilation scheduling |
| Clang Modules | `CLANG_ENABLE_MODULES` | `YES` | Caches module maps on disk instead of reprocessing headers |
| Explicit Modules | `SWIFT_ENABLE_EXPLICIT_MODULES` | Evaluate per-project | Improves parallelism but may regress due to scanning overhead; benchmark before and after |

**References:**
- [Improving the speed of incremental builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds) -- Apple Documentation
- [SwiftLee: Build performance analysis for speeding up Xcode builds](https://www.avanderlee.com/optimization/analysing-build-performance-xcode/)
- [Xcode Release Notes: Compilation Caching](https://developer.apple.com/documentation/xcode-release-notes/) (feature ID 149700201)
- [Bitrise: Xcode Compilation Cache FAQ](https://docs.bitrise.io/en/bitrise-build-cache/build-cache-for-xcode/xcode-compilation-cache-faq.html)

### CocoaPods Projects

CocoaPods is deprecated. When a project uses CocoaPods, do not attempt CocoaPods-specific build optimizations (linkage mode changes, `COCOAPODS_PARALLEL_CODE_SIGN`, Podfile tweaks). These are unreliable and frequently regress build times.

Recommend migrating to Swift Package Manager as the highest-impact long-term improvement. SPM advantages for build time: compilation caching works out of the box, better build parallelism from the dependency graph, no `pod install` xcconfig regeneration overhead, and native Xcode integration with full support for modern features like explicit modules.

Focus analysis on first-party targets and build settings the project controls directly. Do not audit `Pods.xcodeproj` or the Podfile.

## Script Phase Analysis

The `xcode-project-analyzer` inspects every Run Script phase in the project for missing metadata and unnecessary execution.

**What the agent checks:**

- Scripts without declared input and output files run on every build regardless of changes. The agent flags these and recommends adding declarations or `.xcfilelist` files.
- Scripts that always run (`alwaysOutOfDate = 1`) are flagged with a recommendation to make them conditional.
- Debug/simulator guards: scripts that upload symbols, run release-only tools, or perform network calls should be skipped in Debug or Simulator builds.
- Timestamp-touching tools: linters or formatters that modify file timestamps without changing content silently invalidate build inputs and force replanning of every Swift module.
- Parallelization: scripts with correctly declared dependencies can run in parallel with compilation instead of blocking it.

**References:**
- [Improving the speed of incremental builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds) -- Apple Documentation (script input/output declarations, `.xcfilelist`)
- [Swift Forums: Slow incremental builds because of "Planning Swift module"](https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803) -- timestamp invalidation case study

## Compile Hotspot Detection

The `xcode-compilation-analyzer` identifies Swift source files and expressions that take disproportionately long to type-check.

**What the agent checks:**

- Build Timing Summary categories to find targets where `CompileSwiftSources` dominates.
- Compiler diagnostic flags (`-warn-long-function-bodies`, `-warn-long-expression-type-checking`) to surface specific slow expressions.
- Optional deep diagnostics: `-debug-time-compilation` (per-file ranking), `-debug-time-function-bodies` (per-function timing), `-stats-output-dir` (compiler statistics as JSON).
- Patterns that commonly cause slow type-checking:
  - Complex chained or nested expressions without intermediate type annotations
  - Nested ternaries or overloaded generic chains
  - Long method chains (`.map().flatMap().filter().reduce()`) without typed intermediates
  - Closures passed to generic functions without explicit return types

**References:**
- [Improving build efficiency with good coding practices](https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices) -- Apple Documentation
- [SwiftLee: Build performance analysis for speeding up Xcode builds](https://www.avanderlee.com/optimization/analysing-build-performance-xcode/) -- compiler diagnostic flags

## Zero-Change Build Overhead

The `xcode-project-analyzer` measures and diagnoses the fixed cost of rebuilding when nothing has changed.

**What the agent checks:**

Even with no source edits, incremental builds incur fixed overhead. The agent measures zero-change build time and investigates these categories from the Build Timing Summary:

| Category | What it does | Why it matters |
|----------|-------------|----------------|
| `PhaseScriptExecution` | Script phases with `alwaysOutOfDate` or missing I/O | Runs on every build regardless of changes |
| `CodeSign` | Signs the app and embedded frameworks | Runs unconditionally; scales with signed binary count |
| `ValidateEmbeddedBinary` | Validates against provisioning profile | Runs unconditionally |
| `CopySwiftLibs` | Copies Swift standard libraries | Runs even when nothing changed |
| `RegisterWithLaunchServices` | Registers the built app | Fast but always present |
| `ProcessInfoPlistFile` | Re-processes Info.plist files | Scales with target count |
| `ExtractAppIntentsMetadata` | Extracts App Intents metadata from all targets including third-party dependencies | Driven by Xcode, not by per-target project settings; unnecessary overhead if the project does not use App Intents but not cleanly suppressible from the repo (classify as `xcode-behavior`) |

A zero-change build above 5 seconds on Apple Silicon typically indicates script phase overhead or excessive codesigning.

**References:**
- [Improving the speed of incremental builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds) -- Apple Documentation
- [Swift Forums: Slow incremental builds because of "Planning Swift module"](https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803) -- zero-change overhead breakdown

## Target Dependency Review

The `xcode-project-analyzer` audits target dependencies and scheme configuration for correctness and parallelism.

**What the agent checks:**

- Target dependencies are explicit and accurate. Missing dependencies cause build failures; inflated dependencies block parallel work.
- Removed or stale dependencies that no longer reflect real build requirements.
- Scheme builds targets in `Dependency Order` (not manual order).
- Oversized monolithic targets that serialize compilation when the work could be split across parallel targets.
- `DEFINES_MODULE` is enabled for custom frameworks that should benefit from module maps.
- Public headers are self-contained enough to compile as a module.

**References:**
- [Improving the speed of incremental builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds) -- Apple Documentation (target dependencies, module maps)

## Module Variant Detection

The `xcode-project-analyzer` and `spm-build-analysis` skills check for configuration drift that causes the same module to be built multiple times with different options.

**What the agent checks:**

- Targets that import the same SPM package but compile with different Swift compiler options produce separate module variants, inflating `SwiftEmitModule` task counts.
- Drift in `SWIFT_OPTIMIZATION_LEVEL`, `SWIFT_COMPILATION_MODE`, `OTHER_SWIFT_FLAGS`, and target-level overrides.
- Project-level vs target-level build setting overrides: settings should be at the project level unless a target has a specific reason to override.
- Preprocessor macros or other build options that differ across sibling targets importing the same modules.

**References:**
- [Building your project with explicit module dependencies](https://developer.apple.com/documentation/xcode/building-your-project-with-explicit-module-dependencies) -- Apple Documentation
- [WWDC24: Demystify explicitly built modules](https://developer.apple.com/videos/play/wwdc2024/10171/)
- [Bitrise: Demystifying Explicitly Built Modules for Xcode](https://bitrise.io/blog/post/demystifying-explicitly-built-modules-for-xcode)

## SPM Graph Analysis

The `spm-build-analysis` skill inspects Swift Package Manager dependencies for graph structure issues, plugin overhead, and dependency hygiene.

**What the agent checks:**

- Large umbrella packages that trigger widespread rebuilds.
- Dependency layering violations: features depending on features instead of flowing inward (Common/Core → Services → Features/UI).
- Circular dependencies (target-level cycles must be refactored; extract shared contracts into a separate module).
- Build-tool and command plugins that run during incremental builds even when no input changed.
- Branch-pinned packages (`branch:`) that force network checks on every fresh resolve; recommends pinning to tags or `revision:` hashes.
- Package reference verification: confirms packages listed in recommendations actually appear in `project.pbxproj` as linked dependencies.
- Transitive dependency minimization: flags `@_exported import` umbrella modules that create hidden rebuild chains.
- Interface/implementation separation opportunities for modules with heavy dependencies.
- Test target isolation: test targets should depend on the module under test, not the entire app target.

**References:**
- [Improving the speed of incremental builds](https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds) -- Apple Documentation
- [Building your project with explicit module dependencies](https://developer.apple.com/documentation/xcode/building-your-project-with-explicit-module-dependencies) -- Apple Documentation

## Swift Macro Impact

The `spm-build-analysis` skill checks for incremental build cascading caused by heavy Swift macro usage.

**What the agent checks:**

- Projects using macro-heavy libraries (e.g., TCA, swift-syntax-based tools) are susceptible to cascading where a trivial change rebuilds most of the app.
- Macro expansion can invalidate downstream modules even when the expanded output has not changed.
- `swift-syntax` building universally (all architectures) when no prebuilt binary is available adds significant overhead to clean builds and CI.
- Recommends isolating macro-using code into fewer, more stable modules to limit the invalidation blast radius.

**References:**
- [Swift Forums: Slow incremental builds because of "Planning Swift module"](https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803) -- macro cascading, swift-syntax overhead

## SwiftUI View Decomposition

The `xcode-compilation-analyzer` checks for SwiftUI view bodies that are expensive to type-check.

**What the agent checks:**

- Monolithic `body` properties (roughly 50+ lines) that force the type-checker to resolve a single large result-builder expression.
- `@ViewBuilder` helper properties instead of separate `struct View` types -- separate structs reduce the type-checker scope per `body`.
- Deeply nested `Group`/`VStack`/`HStack` hierarchies within a single body.
- Recommends extracting subviews into dedicated `struct View` types.

**References:**
- [Improving build efficiency with good coding practices](https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices) -- Apple Documentation

## Asset Catalog Parallelism

The `xcode-project-analyzer` checks asset catalog compilation for single-threaded bottlenecks.

**What the agent checks:**

- `CompileAssetCatalog` is single-threaded per target. Multiple catalogs within the same target compile sequentially in a single process.
- If asset catalog compilation appears as a significant timing category, recommends splitting assets into separate resource bundles across separate targets for parallel compilation.
- Asset catalog compilation is not cacheable by the Xcode compilation cache (`CompileAssetCatalogVariant` is non-cacheable).
- Checks whether asset catalogs rebuild during incremental builds even when no assets changed.

**References:**
- [Swift Forums: Slow incremental builds because of "Planning Swift module"](https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803) -- asset catalog single-threaded compilation
- [Bitrise: Xcode Compilation Cache FAQ](https://docs.bitrise.io/en/bitrise-build-cache/build-cache-for-xcode/xcode-compilation-cache-faq.html) -- non-cacheable task types

## Access Control Optimization

The `xcode-compilation-analyzer` checks for access control patterns that inflate compiler work.

**What the agent checks:**

- Classes not intended for subclassing should be marked `final`. This eliminates virtual dispatch overhead and lets the compiler de-virtualize method calls.
- Properties and methods not used outside their declaration or file should use `private` or `fileprivate`. Narrower visibility reduces the compiler's symbol search space.
- `internal` (the default) is preferred over `public` unless the symbol genuinely crosses module boundaries.
- `struct` and `enum` are preferred over `class` when reference semantics are not needed. Value types are simpler for the compiler to reason about.
- Objective-C bridging surfaces should be kept narrow. Swift members marked `private` do not need Objective-C visibility.

**References:**
- [Improving build efficiency with good coding practices](https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices) -- Apple Documentation

## Incremental Build Diagnostics

The `xcode-compilation-analyzer` and `xcode-project-analyzer` investigate categories that disproportionately inflate incremental builds.

**What the agent checks:**

- **Planning Swift module**: Can dominate incremental builds (up to 30s per module), sometimes exceeding clean build time. If modules are replanned but no compiles are scheduled, build inputs are being invalidated unexpectedly.
- **SwiftEmitModule**: Can take 60s+ after a single-line change in large modules. If it exceeds compile time for the same target, the module's public API surface may be unnecessarily wide.
- **Task Backtraces** (Xcode 16.4+): Enable via Scheme Editor > Build > Build Debugging to see why each task re-ran. The agent recommends enabling this when incremental build overhead is unexplained.
- **Multi-platform build multiplication**: Adding a secondary platform (e.g., watchOS) can cause shared SPM packages to build multiple times per platform/architecture combination.

**References:**
- [Swift Forums: Slow incremental builds because of "Planning Swift module"](https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803)
- [Building your project with explicit module dependencies](https://developer.apple.com/documentation/xcode/building-your-project-with-explicit-module-dependencies) -- Apple Documentation
- [WWDC24: Demystify explicitly built modules](https://developer.apple.com/videos/play/wwdc2024/10171/)
