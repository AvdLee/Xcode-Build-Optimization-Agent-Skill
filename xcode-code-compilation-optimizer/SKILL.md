---
name: xcode-code-compilation-optimizer
description: Analyze Swift and mixed-language compile hotspots using build timing summaries and Swift frontend diagnostics, then produce a recommend-first source-level optimization plan. Use when a developer reports slow compilation, type-checking warnings, or expensive clean-build compile phases.
---

# Xcode Code Compilation Optimizer

Use this skill when compile time, not just general project configuration, looks like the bottleneck.

## Core Rules

- Start from evidence, ideally a recent `.build-benchmark/` artifact or raw timing-summary output.
- Prefer analysis-only compiler flags over persistent project edits during investigation.
- Rank findings by expected compile-time impact, not by how easy they are to describe.
- Do not edit source or build settings without explicit developer approval.

## What To Inspect

- `Build Timing Summary` output from a clean build
- long-running `CompileSwiftSources` or per-file compilation tasks
- ad hoc runs with:
  - `-Xfrontend -warn-long-expression-type-checking=<ms>`
  - `-Xfrontend -warn-long-function-bodies=<ms>`
- mixed Swift and Objective-C surfaces that increase bridging work

## Analysis Workflow

1. Identify whether the main issue is broad compilation volume or a few extreme hotspots.
2. Parse timing-summary categories and rank the biggest compile contributors.
3. Run or inspect long type-check diagnostics when expression complexity is suspected.
4. Map the evidence to a concrete recommendation list.
5. Separate code-level suggestions from project-level or module-level suggestions.

## Apple-Derived Checks

Look for these patterns first:

- missing explicit type information in expensive expressions
- complex chained or nested expressions that are hard to type-check
- delegate properties typed as `AnyObject` instead of a concrete protocol
- oversized Objective-C bridging headers or generated Swift-to-Objective-C surfaces
- header imports that skip framework qualification and miss module-cache reuse

## Reporting Format

For each recommendation, include:

- observed evidence
- likely affected file or module
- estimated impact
- confidence
- whether approval is required before applying it

If the evidence points to project configuration instead of source, hand off to `xcode-project-optimizer`.

## Preferred Tactics

- Suggest ad hoc flag injection through the build command before recommending persistent build-setting changes.
- Prefer narrowing giant view builders, closures, or result-builder expressions into smaller typed units.
- Recommend explicit imports and protocol typing when they reduce compiler search space.
- Call out when mixed-language boundaries are the real issue rather than Swift syntax alone.

## Additional Resources

- For the detailed audit checklist, see [references/code-compilation-checks.md](references/code-compilation-checks.md)
- For the shared recommendation structure, see [../references/recommendation-format.md](../references/recommendation-format.md)
- For source citations, see [../references/build-optimization-sources.md](../references/build-optimization-sources.md)
