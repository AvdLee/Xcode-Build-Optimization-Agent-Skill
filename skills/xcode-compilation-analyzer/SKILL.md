---
name: xcode-compilation-analyzer
description: Analyze Swift and mixed-language compile hotspots using build timing summaries and Swift frontend diagnostics, then produce a recommend-first source-level optimization plan. Use when a developer reports slow compilation, type-checking warnings, expensive clean-build compile phases, long CompileSwiftSources tasks, warn-long-function-bodies output, or wants to speed up Swift type checking.
---

# Xcode Compilation Analyzer

Use this skill when compile time, not just general project configuration, looks like the bottleneck.

## Core Rules

- Start from evidence, ideally a recent `.build-benchmark/` artifact or raw timing-summary output.
- Prefer analysis-only compiler flags over persistent project edits during investigation.
- Rank findings by expected **wall-clock** impact, not cumulative compile-time impact. When compile tasks are heavily parallelized (sum of compile categories >> wall-clock median), note that fixing individual hotspots may improve parallel efficiency without reducing build wait time.
- When the evidence points to parallelized work rather than serial bottlenecks, label recommendations as "Reduces compiler workload (parallel)" rather than "Reduces build time."
- Do not edit source or build settings without explicit developer approval.

## What To Inspect

- `Build Timing Summary` output from clean and incremental builds
- long-running `CompileSwiftSources` or per-file compilation tasks
- `SwiftEmitModule` time -- can reach 60s+ after a single-line change in large modules; if it dominates incremental builds, the module is likely too large or macro-heavy
- `Planning Swift module` time -- if this category is disproportionately large in incremental builds (up to 30s per module), it signals unexpected input invalidation or macro-related rebuild cascading
- ad hoc runs with:
  - `-Xfrontend -warn-long-expression-type-checking=<ms>`
  - `-Xfrontend -warn-long-function-bodies=<ms>`
- deeper diagnostic flags for thorough investigation:
  - `-Xfrontend -debug-time-compilation` -- per-file compile times to rank the slowest files
  - `-Xfrontend -debug-time-function-bodies` -- per-function compile times (unfiltered, complements the threshold-based warning flags)
  - `-Xswiftc -driver-time-compilation` -- driver-level timing to isolate driver overhead
  - `-Xfrontend -stats-output-dir <path>` -- detailed compiler statistics (JSON) per compilation unit for root-cause analysis
- mixed Swift and Objective-C surfaces that increase bridging work

## Analysis Workflow

1. Identify whether the main issue is broad compilation volume or a few extreme hotspots.
2. Parse timing-summary categories and rank the biggest compile contributors.
3. Run the diagnostics script to surface type-checking hotspots:
   ```bash
   python3 scripts/diagnose_compilation.py \
     --project App.xcodeproj \
     --scheme MyApp \
     --configuration Debug \
     --destination "platform=iOS Simulator,name=iPhone 16" \
     --threshold 100 \
     --output-dir .build-benchmark
   ```
   This produces a ranked list of functions and expressions that exceed the millisecond threshold. Use the diagnostics artifact alongside source inspection to focus on the most expensive files first.
4. Map the evidence to a concrete recommendation list.
5. Separate code-level suggestions from project-level or module-level suggestions.

## Apple-Derived Checks

Look for these patterns first:

- missing explicit type information in expensive expressions
- complex chained or nested expressions that are hard to type-check
- delegate properties typed as `AnyObject` instead of a concrete protocol
- oversized Objective-C bridging headers or generated Swift-to-Objective-C surfaces
- header imports that skip framework qualification and miss module-cache reuse
- classes missing `final` that are never subclassed
- overly broad access control (`public`/`open`) on internal-only symbols
- monolithic SwiftUI `body` properties that should be decomposed into subviews
- long method chains or closures without intermediate type annotations

## Reporting Format

For each recommendation, include:

- observed evidence
- likely affected file or module
- expected wait-time impact (e.g. "Expected to reduce your clean build by ~2s" or "Reduces parallel compile work but unlikely to reduce build wait time")
- confidence
- whether approval is required before applying it

If the evidence points to project configuration instead of source, hand off to [`xcode-project-analyzer`](../xcode-project-analyzer/SKILL.md) by reading its SKILL.md and applying its workflow to the same project context.

## Preferred Tactics

- Suggest ad hoc flag injection through the build command before recommending persistent build-setting changes.
- Prefer narrowing giant view builders, closures, or result-builder expressions into smaller typed units.
- Recommend explicit imports and protocol typing when they reduce compiler search space.
- Call out when mixed-language boundaries are the real issue rather than Swift syntax alone.

## Additional Resources

- For the detailed audit checklist, see [references/code-compilation-checks.md](references/code-compilation-checks.md)
- For the shared recommendation structure, see [references/recommendation-format.md](references/recommendation-format.md)
- For source citations, see [references/build-optimization-sources.md](references/build-optimization-sources.md)
