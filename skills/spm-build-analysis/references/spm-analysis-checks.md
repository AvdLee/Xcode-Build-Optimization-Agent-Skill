# SPM Analysis Checks

Use this reference when package dependencies or package plugins are suspected build bottlenecks.

## Package Graph Checks

- Identify large umbrella packages that trigger widespread rebuilds.
- Look for dependency layering that forces many downstream targets to recompile.
- Flag local package arrangements that cause broad invalidation after small edits.

## Package Plugin Checks

- List build-tool and command plugins involved in the build.
- Measure whether plugins run during incremental builds even when no relevant input changed.
- Call out plugins that return quickly but still add fixed overhead to every build.

## Package Reference Verification

- Before including any local package in a build-time recommendation, confirm it appears in the project's `XCLocalSwiftPackageReference` section of `project.pbxproj`.
- A package existing under `Vendor/` or as a directory in the repo does not mean it is linked. Only referenced packages affect build time.
- For remote packages, confirm the `XCRemoteSwiftPackageReference` entry exists and at least one `XCSwiftPackageProductDependency` links its product to a target.

## Version Pin Feasibility

- When recommending a switch from `branch:` to a tagged version, verify tags exist via `git ls-remote --tags <url>`.
- If no tags exist, recommend pinning to a specific `revision:` hash for deterministic resolution.
- Note the distinction: branch pins force network checks on every fresh resolve; revision pins are fully deterministic but do not benefit from semver range resolution.

## Binary And Remote Dependency Checks

- Note binary target size and extraction overhead for clean environments.
- Highlight remote checkout or fetch costs that matter for CI or fresh machines.
- Compare remote vs local package tradeoffs when iteration speed matters more than distribution convenience.

## Module Variant Checks

- Look for the same dependency module being built with different options.
- Compare macros, language mode, and configuration-sensitive options across dependents.
- Prefer configuration alignment when it reduces repeated module builds safely.

## Layered Architecture Validation

- Enforce a clear dependency direction: Common/Core --> Services/Domain --> Features/UI. Dependencies must flow in one direction only (inward/downward).
- Features should never depend on each other directly. If two features share types, move those types to a lower-layer module.
- Validate that `Package.swift` target dependency lists match the intended layer hierarchy.

## Circular Dependency Detection

- SPM supports cyclic *package* dependencies (since May 2024) but not cyclic *target* dependencies.
- Circular module dependencies should always be refactored: extract the shared contract (protocols, DTOs) into a separate module that both sides depend on.
- Check for hidden cycles through transitive dependencies by tracing the full dependency graph.

## Module Sizing Guidance

- Modules larger than roughly 200 files increase incremental build scope unnecessarily -- a single file change recompiles more than needed.
- Recommend splitting oversized modules by feature area or responsibility.
- Each module should have a clear, single-purpose responsibility. If a module's name requires "And" or "Utils" to describe, it likely needs splitting.

## Transitive Dependency Minimization

- Each module should depend only on what it directly uses. Unnecessary transitive dependencies widen the rebuild surface.
- Avoid "umbrella" modules that re-export everything via `@_exported import` -- they create hidden dependency chains where a change in any re-exported module triggers rebuilds in all importers.
- Use `@_exported import` sparingly and only for genuine convenience wrappers.

## Interface/Implementation Separation

- Define protocols and public types in lightweight "interface" modules (e.g., `NetworkingInterface`).
- Put implementations in separate modules (e.g., `NetworkingImpl`).
- Feature modules compile against the interface without waiting for the full implementation to build, improving parallelism.
- This pattern is most valuable when the implementation module has many files or heavy dependencies that would block downstream compilation.

## Test Target Isolation

- Test targets should depend on the module under test, not the entire app target. Depending on the app target forces a full app build before tests can compile.
- Shared test utilities (mocks, fixtures, helpers) belong in a dedicated `TestHelpers` module rather than being duplicated across test targets.
- Keep test-only dependencies out of production target dependency lists.

## Swift Macro Rebuild Impact

- Projects that heavily use Swift macros (e.g., TCA, swift-syntax-based libraries) are susceptible to incremental build cascading where a trivial change rebuilds most of the app.
- Macro expansion can invalidate downstream modules even when the expanded output has not changed, because the build system treats the macro input as a dependency.
- Check whether `swift-syntax` is building universally (all architectures) when no prebuilt binary is available. This adds significant overhead to clean builds and CI. Verify with the build log whether the `swift-syntax` target compiles for more architectures than `ONLY_ACTIVE_ARCH` would suggest.
- If macro-heavy packages dominate incremental build time, consider whether the macro-using code can be isolated into fewer, more stable modules to limit the invalidation blast radius.

## Multi-Platform Build Multiplication

- Adding a secondary platform target (e.g., watchOS, macOS Catalyst) can cause shared SPM packages to build multiple times -- once per platform and architecture combination.
- A project with iOS and watchOS targets may build shared packages 3x: iOS arm64, iOS x86_64 (simulator), and watchOS arm64.
- Check the build log for duplicate `SwiftCompile`, `SwiftEmitModule`, and `ScanDependencies` tasks for the same package across different platform/architecture slices.
- If multi-platform multiplication is a significant contributor, consider whether secondary platform targets can use a subset of shared packages, or whether packages can be prebuilt as binary targets for secondary platforms.

## CI-Specific Checks

- Fresh checkout cost
- plugin invocation cost
- cache hit sensitivity
- redundant package resolution work

## Recommendation Prioritization

Qualify every estimated impact with wall-clock framing. High-priority items should be those likely to reduce the developer's actual wait time, not just cumulative task totals. If the impact on wait time is uncertain, say so.

- High: package plugins or graph structure repeatedly inflating incremental builds, circular dependencies, umbrella re-exports causing cascading rebuilds, Swift macro cascading that causes near-full rebuilds from trivial changes.
- Medium: configuration drift that causes duplicate module variants, oversized modules, missing interface/implementation separation, multi-platform build multiplication, `swift-syntax` building universally without prebuilt binary.
- Low: clean-environment checkout costs that barely affect local iteration, minor transitive dependency cleanup.
