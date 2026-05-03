# Build Settings Best Practices

This reference lists Xcode build settings that affect build performance. Use it to audit a project and produce a pass/fail checklist.

The scope is strictly **build performance**. Do not flag language-migration settings like `SWIFT_STRICT_CONCURRENCY` or `SWIFT_UPCOMING_FEATURE_*` -- those are developer adoption choices unrelated to build speed.

## How To Read This Reference

Each setting includes:

- **Setting name** and the Xcode build-settings key
- **Recommended value** for Debug and Release
- **Why it matters** for build time
- **Risk** of changing it

Use checkmark and cross indicators when reporting:

- `[x]` -- setting matches the recommended value
- `[ ]` -- setting does not match; include the actual value and the expected value

## Debug Configuration

These settings optimize for fast iteration during development.

### Compilation Mode

- **Key:** `SWIFT_COMPILATION_MODE`
- **Recommended:** `singlefile` (Xcode UI: "Incremental"; or unset -- Xcode defaults to singlefile for Debug)
- **Why:** Single-file mode recompiles only changed files. `wholemodule` recompiles the entire target on every change.
- **Risk:** Low

### Swift Optimization Level

- **Key:** `SWIFT_OPTIMIZATION_LEVEL`
- **Recommended:** `-Onone`
- **Why:** Optimization passes add significant compile time. Debug builds do not benefit from runtime speed improvements.
- **Risk:** Low

### GCC Optimization Level

- **Key:** `GCC_OPTIMIZATION_LEVEL`
- **Recommended:** `0`
- **Why:** Same rationale as Swift optimization level, but for C/C++/Objective-C sources.
- **Risk:** Low

### Build Active Architecture Only

- **Key:** `ONLY_ACTIVE_ARCH` (`BUILD_ACTIVE_ARCHITECTURE_ONLY`)
- **Recommended:** `YES`
- **Why:** Building all architectures doubles or triples compile and link time for no debug benefit.
- **Risk:** Low

### Debug Information Format

- **Key:** `DEBUG_INFORMATION_FORMAT`
- **Recommended:** `dwarf`
- **Why:** `dwarf-with-dsym` generates a separate dSYM bundle which adds overhead. Plain `dwarf` embeds debug info directly in the binary, which is sufficient for local debugging.
- **Risk:** Low

### Enable Testability

- **Key:** `ENABLE_TESTABILITY`
- **Recommended:** `YES`
- **Why:** Required for `@testable import`. Adds minor overhead by exporting internal symbols, but this is expected during development.
- **Risk:** Low

### Active Compilation Conditions

- **Key:** `SWIFT_ACTIVE_COMPILATION_CONDITIONS`
- **Recommended:** Should include `DEBUG`
- **Why:** Guards conditional compilation blocks (e.g., `#if DEBUG`) and ensures debug-only code paths are included.
- **Risk:** Low

### Eager Linking

- **Key:** `EAGER_LINKING`
- **Recommended:** `YES`
- **Why:** Allows the linker to start work before all compilation tasks finish, reducing wall-clock build time. Particularly effective for Debug builds where link time is a meaningful fraction of total build time.
- **Risk:** Low

## Release Configuration

These settings optimize for production builds.

### Compilation Mode

- **Key:** `SWIFT_COMPILATION_MODE`
- **Recommended:** `wholemodule`
- **Why:** Whole-module optimization produces faster runtime code. Build time is secondary for release.
- **Risk:** Low

### Swift Optimization Level

- **Key:** `SWIFT_OPTIMIZATION_LEVEL`
- **Recommended:** `-O` or `-Osize`
- **Why:** Produces optimized binaries. `-Osize` trades some speed for smaller binary size.
- **Risk:** Low

### GCC Optimization Level

- **Key:** `GCC_OPTIMIZATION_LEVEL`
- **Recommended:** `s`
- **Why:** Optimizes C/C++/Objective-C for size, matching the typical release expectation.
- **Risk:** Low

### Build Active Architecture Only

- **Key:** `ONLY_ACTIVE_ARCH`
- **Recommended:** `NO`
- **Why:** Release builds must include all supported architectures for distribution.
- **Risk:** Low

### Debug Information Format

- **Key:** `DEBUG_INFORMATION_FORMAT`
- **Recommended:** `dwarf-with-dsym`
- **Why:** dSYM bundles are required for crash symbolication in production.
- **Risk:** Low

### Enable Testability

- **Key:** `ENABLE_TESTABILITY`
- **Recommended:** `NO`
- **Why:** Removes internal-symbol export overhead from release builds. Testing should use Debug configuration.
- **Risk:** Low

## General (All Configurations)

### Compilation Caching

- **Key:** `COMPILATION_CACHE_ENABLE_CACHING`
- **Recommended:** `YES`
- **Why:** Caches compilation results for Swift and C-family sources so repeated compilations of the same inputs are served from cache. The biggest wins come from branch switching and clean builds where source files are recompiled unchanged. This is an opt-in feature. The umbrella setting controls both `SWIFT_ENABLE_COMPILE_CACHE` and `CLANG_ENABLE_COMPILE_CACHE` under the hood; those can be toggled independently if needed.
- **Measurement:** Measured 5-14% faster clean builds across tested projects (87 to 1,991 Swift files). The benefit compounds in real developer workflows where the cache persists between builds -- branch switching, pulling changes, and CI with persistent DerivedData -- though the exact savings depend on how many files change between builds.
- **Risk:** Low -- can also be enabled via per-user project settings so it does not need to be committed to the shared project file.

### Integrated Swift Driver

- **Key:** `SWIFT_USE_INTEGRATED_DRIVER`
- **Recommended:** `YES`
- **Why:** Uses the integrated Swift driver which runs inside the build system process, eliminating inter-process overhead for compilation scheduling. Enabled by default in modern Xcode but worth verifying in migrated projects.
- **Risk:** Low

### Clang Module Compilation

- **Key:** `CLANG_ENABLE_MODULES`
- **Recommended:** `YES`
- **Why:** Enables Clang module compilation for C/Objective-C sources, caching module maps on disk instead of reprocessing headers on every import. Eliminates redundant header parsing across translation units.
- **Risk:** Low

### Explicit Module Builds

- **Key:** `SWIFT_ENABLE_EXPLICIT_MODULES` (C/ObjC enabled by default in Xcode 16+; for Swift use `_EXPERIMENTAL_SWIFT_EXPLICIT_MODULES`)
- **Recommended:** Evaluate per-project
- **Why:** Makes module compilation visible to the build system as discrete tasks, improving parallelism and scheduling. Reduces redundant module rebuilds by making dependency edges explicit. Some projects see regressions due to the overhead of dependency scanning, so benchmark before and after enabling.
- **Risk:** Medium -- test thoroughly; currently experimental for Swift targets.

### User Script Sandboxing

- **Key:** `ENABLE_USER_SCRIPT_SANDBOXING`
- **Recommended:** `YES` for any target that has Run Script build phases.
- **Why:** Sandboxing forces every Run Script phase to declare each file it reads or writes inside the project source root and the derived data directory. Undeclared accesses fail loudly at build time instead of silently corrupting incremental builds, and -- critically -- the resulting clean dependency graph is the prerequisite for safely enabling `FUSE_BUILD_SCRIPT_PHASES`. From WWDC22 session 110364 *Demystify parallelization in Xcode builds* (Ben, Xcode Build System team):

  > To mitigate this, Xcode supports user script sandboxing to precisely declare the dependencies of each script phase. Sandboxing is an opt-in feature that blocks shell scripts from accidentally accessing source files and intermediate build objects, unless those are explicitly declared as an input or output for the phase.

  Activation:

  > To enable Sandboxed Shell Scripts for a target, set ENABLE_USER_SCRIPT_SANDBOXING to YES in the build settings editor or an xcconfig file.

  Scope caveat (must be reported alongside the recommendation):

  > Enabling the build setting for a script's target blocks access to files inside the source root of the project as well as the derived data directory if they are not explicitly defined as inputs or outputs of the script in the project. The sandbox will not prevent unauthorized access to any other directory, so don't consider this a security feature.
- **Measurement:** Indirect. Sandboxing on its own does not change wall-clock build time; its role is to surface the missing input and output declarations that block `FUSE_BUILD_SCRIPT_PHASES` from being safely enabled. The wall-clock benefit is captured under `FUSE_BUILD_SCRIPT_PHASES`.
- **Risk:** Medium. Existing scripts with undeclared inputs or outputs will fail at build time until their dependency lists are completed. Treat enabling sandboxing as a one-time cleanup pass per target: turn it on, fix every violation Xcode lists in the build log, then enable phase fusion.

### Script Phase Fusion

- **Key:** `FUSE_BUILD_SCRIPT_PHASES`
- **Recommended:** `YES`, gated on (a) `ENABLE_USER_SCRIPT_SANDBOXING=YES` for the same target, and (b) every Run Script phase in the target declaring its complete inputs and outputs (or `.xcfilelist` files for long lists).
- **Why:** Without fusion, the build system runs consecutive Run Script phases serially within a target to avoid data races. From WWDC22 session 110364 *Demystify parallelization in Xcode builds* (Ben, Xcode Build System team):

  > If the scripts in a target are configured to run based on dependency analysis and specify their complete list of inputs and outputs, then the build setting FUSE_BUILD_SCRIPT_PHASES can be set to YES to indicate the build system should attempt to run them in parallel.

  Why sandboxing is the required prerequisite:

  > And in combination with the previously explained build setting FUSE_BUILD_SCRIPT_PHASES, script phases with correctly defined dependency edges through sandboxing can execute in parallel to reduce the critical path of the build.

  Enabling fusion without sandboxing in place means an undeclared input can let one script read a file before another has written it, causing intermittent build failures or stale outputs.
- **Measurement:** Target-dependent. A target with N parallelizable Run Script phases of average duration `t` saves up to `(N-1) * t` on every clean (or fully re-run) build once fusion is enabled. As a representative shape, NSK ships with 12 `PhaseScriptExecution` tasks on a clean build per the orchestrator's documented benchmarks; projects with several script phases per target are the strongest beneficiaries. Targets with only one Run Script phase, or whose phases already run in parallel because they are in different targets, see no direct improvement.
- **Risk:** Medium when both prerequisites are met (fusion can still expose latent dependency-declaration gaps in scripts the sandbox cleanup missed). High if enabled without sandboxing -- see the Why section above.

## Cross-Target Consistency

These checks find settings differences between targets that cause redundant build work.

### Project-Level vs Target-Level Overrides

Build-affecting settings should be set at the project level unless a target has a specific reason to override. Unnecessary per-target overrides cause confusion and can silently create module variants.

Settings to check for project-level consistency:

- `SWIFT_COMPILATION_MODE`
- `SWIFT_OPTIMIZATION_LEVEL`
- `ONLY_ACTIVE_ARCH`
- `DEBUG_INFORMATION_FORMAT`

### Module Variant Duplication

When multiple targets import the same SPM package but compile with different Swift compiler options, the build system produces separate module variants for each combination. This inflates `SwiftEmitModule` task counts.

Check for drift in:

- `SWIFT_OPTIMIZATION_LEVEL`
- `SWIFT_COMPILATION_MODE`
- `OTHER_SWIFT_FLAGS`
- Target-level build settings that override project defaults

### Out of Scope

Do **not** flag the following as build-performance issues:

- `SWIFT_STRICT_CONCURRENCY` -- language migration choice
- `SWIFT_UPCOMING_FEATURE_*` -- language migration choice
- `SWIFT_APPROACHABLE_CONCURRENCY` -- language migration choice
- `SWIFT_ACTIVE_COMPILATION_CONDITIONS` values beyond `DEBUG` (e.g., `WIDGETS`, `APPCLIP`) -- intentional per-target customization

## Checklist Output Format

When reporting results, use this structure:

```markdown
### Debug Configuration
- [x] `SWIFT_COMPILATION_MODE`: `singlefile` (recommended: `singlefile`)
- [ ] `DEBUG_INFORMATION_FORMAT`: `dwarf-with-dsym` (recommended: `dwarf`)
- [x] `SWIFT_OPTIMIZATION_LEVEL`: `-Onone` (recommended: `-Onone`)
...

### Release Configuration
- [x] `SWIFT_COMPILATION_MODE`: `wholemodule` (recommended: `wholemodule`)
...

### General (All Configurations)
- [ ] `COMPILATION_CACHE_ENABLE_CACHING`: `NO` (recommended: `YES`)
...

### Cross-Target Consistency
- [x] All targets inherit `SWIFT_OPTIMIZATION_LEVEL` from project level
- [ ] `OTHER_SWIFT_FLAGS` differs between Stock Analyzer and StockAnalyzerClip
...
```
