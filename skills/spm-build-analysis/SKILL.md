---
name: spm-build-analysis
description: Analyze Swift Package Manager dependencies, package plugins, module variants, and CI-oriented build overhead that slow Xcode builds. Use when a developer suspects packages, plugins, or dependency graph shape are hurting clean or incremental build performance, mentions SPM slowness, package resolution time, build plugin overhead, or duplicate module builds from configuration drift.
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

## Focus Areas

- package graph shape and how much work changes trigger downstream
- plugin overhead during local development and CI
- checkout or fetch cost signals that show up in clean environments
- configuration drift that forces duplicate module builds
- risks from package targets that use different macros or options while sharing dependencies

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

If the main problem is not package-related, hand off to [`xcode-project-optimizer`](../xcode-project-optimizer/SKILL.md) or [`xcode-code-compilation-optimizer`](../xcode-code-compilation-optimizer/SKILL.md) by reading the target skill's SKILL.md and applying its workflow to the same project context.

## Additional Resources

- For the detailed audit checklist, see [references/spm-analysis-checks.md](references/spm-analysis-checks.md)
- For the shared recommendation structure, see [../../references/recommendation-format.md](../../references/recommendation-format.md)
- For source citations, see [../../references/build-optimization-sources.md](../../references/build-optimization-sources.md)
