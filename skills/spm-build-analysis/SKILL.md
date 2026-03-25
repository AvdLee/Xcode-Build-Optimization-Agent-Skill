---
name: spm-build-analysis
description: Analyze Swift Package Manager dependencies, package plugins, module variants, and CI-oriented build overhead that slow Xcode builds. Use when a developer suspects packages, plugins, or dependency graph shape are hurting clean or incremental build performance, mentions SPM slowness, package resolution time, build plugin overhead, duplicate module builds from configuration drift, circular dependencies between modules, oversized modules needing splitting, or modularization best practices.
---

# SPM Build Analysis

Use this skill when package structure, plugins, or dependency configuration are likely contributing to slow Xcode builds.

## Core Rules

- Treat package analysis as evidence gathering first, not a mandate to replace dependencies.
- Separate package-graph issues from project-setting issues.
- Do not rewrite package manifests or dependency sources without explicit approval.

## What To Inspect

- `Package.swift` and `Package.resolved`
- local packages vs remote packages
- package plugin and build-tool usage
- binary target footprint
- dependency layering, repeated imports, and potential cycles
- build logs or timing summaries that show package-related work

## Verification Before Recommending

Before including any local package in a recommendation, verify that it is actually part of the project's dependency graph. A `Vendor/` directory may contain packages that are not linked to any target.

- Check `project.pbxproj` for `XCLocalSwiftPackageReference` entries that reference the package path.
- Check `XCSwiftPackageProductDependency` entries to confirm the package's product is linked to at least one target.
- If a local package exists on disk but is not referenced in the project, do not include it in build-time recommendations.

When recommending version pins for branch-tracked dependencies:

- Use the helper script to scan all branch-pinned dependencies at once:
  ```bash
  python3 scripts/check_spm_pins.py --project App.xcodeproj
  ```
  This checks `git ls-remote --tags` for each branch-pinned package and reports which have tags available for pinning.
- If no tags exist, recommend pinning to a specific commit revision hash for determinism instead.
- Note which packages are branch-pinned because the upstream simply has no tags, versus packages that have tags but are intentionally tracking a branch.

## Focus Areas

- package graph shape and how much work changes trigger downstream
- plugin overhead during local development and CI
- checkout or fetch cost signals that show up in clean environments
- configuration drift that forces duplicate module builds
- risks from package targets that use different macros or options while sharing dependencies
- dependency direction violations (features depending on each other instead of shared lower layers)
- circular dependencies between modules (extract shared contracts into a protocol module)
- oversized modules (200+ files) that widen incremental rebuild scope
- umbrella modules using `@_exported import` that create hidden dependency chains
- missing interface/implementation separation that blocks build parallelism
- test targets depending on the app target instead of the module under test
- Swift macro rebuild cascading: heavy use of Swift macros (e.g., TCA, swift-syntax-based libraries) can cause a trivial source change to cascade into near-full rebuilds because macro expansion invalidates downstream modules
- `swift-syntax` building universally (all architectures) when no prebuilt binary is available, adding significant clean-build overhead
- multi-platform build multiplication: adding a secondary platform target (e.g., watchOS) can cause shared SPM packages to build multiple times (e.g., iOS arm64, iOS x86_64, watchOS arm64), multiplying `SwiftCompile`, `SwiftEmitModule`, and `ScanDependencies` tasks

## Modular SDK Migration Caveat

Migrating a dependency from a monolithic target to a modular multi-target SDK (e.g., replacing one umbrella library with separate Core, RUM, Logs, Trace modules) does not automatically reduce build time. Modular targets increase the number of `SwiftCompile`, `SwiftEmitModule`, and `ScanDependencies` tasks because each target must be compiled, scanned, and emit its module independently. The build-time trade-off depends on the project's parallelism headroom and how many of the modular targets are actually needed.

When considering a modular SDK migration:

- Compare the total `SwiftCompile` task count before and after.
- Benchmark both configurations before recommending the migration for build speed.
- If the motivation is API surface reduction (importing only what you use), note that build time may stay flat or increase while import hygiene improves.
- Only recommend modular SDK migration for build speed when the project currently compiles large portions of the monolithic SDK that it does not use, and the modular alternative lets it skip those unused portions entirely.

## Explicit Module Dependency Angle

When the same module appears multiple times in timing output, investigate whether different package or target options are forcing extra module variants. Uniform options often matter more than shaving a small amount of source code.

## Reporting Format

For each finding, include:

- evidence
- affected package or plugin
- likely clean-build vs incremental-build impact
- CI impact if relevant
- estimated impact
- approval requirement

If the main problem is not package-related, hand off to [`xcode-project-analyzer`](../xcode-project-analyzer/SKILL.md) or [`xcode-compilation-analyzer`](../xcode-compilation-analyzer/SKILL.md) by reading the target skill's SKILL.md and applying its workflow to the same project context.

## Additional Resources

- For the detailed audit checklist, see [references/spm-analysis-checks.md](references/spm-analysis-checks.md)
- For the shared recommendation structure, see [references/recommendation-format.md](references/recommendation-format.md)
- For source citations, see [references/build-optimization-sources.md](references/build-optimization-sources.md)
