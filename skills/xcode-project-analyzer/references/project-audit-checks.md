# Project Audit Checks

Use this reference when reviewing build-system configuration rather than source-level compile behavior.

## Target And Scheme Checks

- Confirm target dependencies are explicit and accurate.
- Remove dependencies that no longer reflect real build requirements.
- Ensure the scheme builds targets in `Dependency Order`.
- Look for oversized or monolithic targets that block parallel work.

## Build Script Checks

- Does each script need to run during incremental builds?
- Are input and output files declared?
- Should inputs and outputs be moved into `.xcfilelist` files?
- Can the script skip debug builds, simulator builds, or unchanged inputs?
- Would the script become parallelizable if dependency analysis were declared correctly?

## Build Setting Checks

Audit project-level and target-level settings against the [build settings best practices](../../../references/build-settings-best-practices.md). Present results as a checklist with `[x]`/`[ ]` indicators.

Key settings to verify:

- `SWIFT_COMPILATION_MODE` -- `singlefile` for Debug, `wholemodule` for Release
- `SWIFT_OPTIMIZATION_LEVEL` -- `-Onone` for Debug, `-O` or `-Osize` for Release
- `ONLY_ACTIVE_ARCH` -- `YES` for Debug, `NO` for Release
- `DEBUG_INFORMATION_FORMAT` -- `dwarf` for Debug, `dwarf-with-dsym` for Release
- `GCC_OPTIMIZATION_LEVEL` -- `0` for Debug, `s` for Release
- `ENABLE_TESTABILITY` -- `YES` for Debug, `NO` for Release
- `COMPILATION_CACHING` -- recommended `YES` for all configurations; caches repeated compilations during branch switching and clean builds
- `EAGER_LINKING` -- recommended `YES` for Debug; starts linking before all compilation finishes
- `SWIFT_USE_INTEGRATED_DRIVER` -- recommended `YES`; uses the integrated driver for better scheduling
- `CLANG_ENABLE_MODULES` -- recommended `YES`; caches module maps on disk for C/ObjC

Do not flag language-migration settings (`SWIFT_STRICT_CONCURRENCY`, `SWIFT_UPCOMING_FEATURE_*`) as build performance issues.

## Module And Header Checks

- `DEFINES_MODULE` is enabled for custom frameworks that should benefit from module maps.
- Public headers are self-contained enough to compile as a module.
- Import statements use framework-qualified imports where available.
- targets that should share built modules use consistent options

## Explicit Module Dependency Checks

- Check whether explicit modules are enabled or expected in the current Xcode version and Swift mode.
- Look for repeated module builds caused by configuration drift.
- Compare preprocessor macros or other build options across sibling targets that import the same modules.

## Recommendation Prioritization

- High: serial script bottlenecks, missing dependency metadata, or configuration drift causing redundant module builds.
- Medium: stale target structure or noncritical scripts running too often.
- Low: settings cleanup without strong evidence of current impact.
