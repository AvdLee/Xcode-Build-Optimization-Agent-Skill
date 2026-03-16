---
name: xcode-build-orchestrator
description: Orchestrate Xcode build optimization by benchmarking first, running the specialist analysis skills, prioritizing findings, requesting explicit approval, delegating approved fixes to xcode-build-fixer, and re-benchmarking after changes. Use when a developer wants an end-to-end build optimization workflow, asks to speed up Xcode builds, wants a full build audit, or needs a recommend-first optimization pass covering compilation, project settings, and packages.
---

# Xcode Build Orchestrator

Use this skill as the recommend-first entrypoint for end-to-end Xcode build optimization work.

## Non-Negotiable Rules

- Start in recommendation mode.
- Benchmark before making changes.
- Do not modify project files, source files, packages, or scripts without explicit developer approval.
- Preserve the evidence trail for every recommendation.
- Re-benchmark after approved changes and report the delta.

## Two-Phase Workflow

The orchestration is designed as two distinct phases separated by developer review.

### Phase 1 -- Analyze (recommend-only)

Run this phase in agent mode because the agent needs to execute builds, run benchmark scripts, write benchmark artifacts, and generate the optimization report. However, treat Phase 1 as **recommend-only**: do not modify any project files, source files, packages, or build settings. The only files the agent creates during this phase are benchmark artifacts and the optimization plan inside `.build-benchmark/`.

1. Collect the build target context: workspace or project, scheme, configuration, destination, and current pain point.
2. Run `xcode-build-benchmark` to establish a baseline if no fresh benchmark exists.
3. Verify the benchmark artifact has non-empty `timing_summary_categories`. If empty, the timing summary parser may have failed -- re-parse the raw logs or inspect them manually.
4. If incremental builds are the primary pain point and Xcode 16.4+ is available, recommend the developer enable **Task Backtraces** (Scheme Editor > Build tab > Build Debugging > "Task Backtraces"). This reveals why each task re-ran, which is critical for diagnosing unexpected replanning or input invalidation. Include any Task Backtrace evidence in the analysis.
5. If `SwiftCompile`, `CompileC`, `SwiftEmitModule`, or `Planning Swift module` dominate the timing summary, run `diagnose_compilation.py` with the same project inputs to capture type-checking hotspots.
6. Run the specialist analyses that fit the evidence by reading each skill's SKILL.md and applying its workflow:
   - [`xcode-compilation-analyzer`](../xcode-compilation-analyzer/SKILL.md)
   - [`xcode-project-analyzer`](../xcode-project-analyzer/SKILL.md)
   - [`spm-build-analysis`](../spm-build-analysis/SKILL.md)
7. Merge findings into a single prioritized improvement plan.
8. Generate the markdown optimization report using `generate_optimization_report.py` and save it to `.build-benchmark/optimization-plan.md`. This report includes the build settings audit, timing analysis, prioritized recommendations, and an approval checklist.
9. Stop and present the plan to the developer for review.

The developer reviews `.build-benchmark/optimization-plan.md`, checks the approval boxes for the recommendations they want implemented, and then triggers phase 2.

### Phase 2 -- Execute and verify (agent mode)

Run this phase in agent mode after the developer has reviewed and approved recommendations from the plan. Delegate all implementation work to [`xcode-build-fixer`](../xcode-build-fixer/SKILL.md) by reading its SKILL.md and applying its workflow.

10. Read `.build-benchmark/optimization-plan.md` and identify the approved items from the approval checklist.
11. Hand off to `xcode-build-fixer` with the approved plan. The fixer applies each approved change, verifies compilation, and re-benchmarks.
12. Append verification results to the optimization plan: post-change medians, absolute and percentage deltas, and confidence notes.
13. Report before and after results, plus any remaining follow-up opportunities.

## Prioritization Rules

Rank items using:

- measured evidence strength
- expected impact on incremental builds
- expected impact on clean builds
- implementation risk
- confidence

Prefer changes that are:

- measurable
- reversible
- low-risk
- likely to improve the most common developer loop first

## Approval Gate

Before implementing anything, present a short approval list that includes:

- recommendation name
- evidence summary
- estimated impact
- affected files or settings
- whether the change is low, medium, or high risk

Wait for explicit developer approval.

## Post-Approval Execution

After approval, delegate to `xcode-build-fixer`:

- the fixer implements only the approved items
- changes are applied atomically and kept scoped
- any deviations from the original recommendation plan are noted
- the fixer re-benchmarks with the same benchmark contract

## Final Report

The final report must include:

- baseline clean and incremental medians
- post-change clean and incremental medians
- absolute and percentage deltas
- what changed
- what was intentionally left unchanged
- confidence notes if noise prevents a strong conclusion
- a ready-to-paste community results row and a link to open a PR (see the report template)

## Preferred Command Paths

### Benchmark

```bash
python3 scripts/benchmark_builds.py \
  --project App.xcodeproj \
  --scheme MyApp \
  --configuration Debug \
  --destination "platform=iOS Simulator,name=iPhone 16" \
  --output-dir .build-benchmark
```

### Compilation Diagnostics

```bash
python3 scripts/diagnose_compilation.py \
  --project App.xcodeproj \
  --scheme MyApp \
  --configuration Debug \
  --destination "platform=iOS Simulator,name=iPhone 16" \
  --threshold 100 \
  --output-dir .build-benchmark
```

### Optimization Report

```bash
python3 scripts/generate_optimization_report.py \
  --benchmark .build-benchmark/<artifact>.json \
  --project-path App.xcodeproj \
  --diagnostics .build-benchmark/<diagnostics>.json \
  --output .build-benchmark/optimization-plan.md
```

## Additional Resources

- For the report template, see [references/orchestration-report-template.md](references/orchestration-report-template.md)
- For benchmark artifact requirements, see [../../references/benchmark-artifacts.md](../../references/benchmark-artifacts.md)
- For the recommendation format, see [../../references/recommendation-format.md](../../references/recommendation-format.md)
- For build settings best practices, see [../../references/build-settings-best-practices.md](../../references/build-settings-best-practices.md)
