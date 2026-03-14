# Orchestration Report Template

Use this structure when the orchestrator consolidates benchmark evidence and specialist findings. The `generate_optimization_report.py` script produces this format automatically when given the benchmark and diagnostics artifacts.

```markdown
# Xcode Build Optimization Plan

## Project Context
- **Project:** `App.xcodeproj`
- **Scheme:** `MyApp`
- **Configuration:** `Debug`
- **Destination:** `platform=iOS Simulator,name=iPhone 16`
- **Xcode:** Xcode 26.x
- **Date:** 2026-01-01T00:00:00Z
- **Benchmark artifact:** `.build-benchmark/<timestamp>-<scheme>.json`

## Baseline Benchmarks

| Metric | Clean | Incremental |
|--------|-------|-------------|
| Median | 0.000s | 0.000s |
| Min | 0.000s | 0.000s |
| Max | 0.000s | 0.000s |
| Runs | 3 | 3 |

### Clean Build Timing Summary

| Category | Tasks | Seconds |
|----------|------:|--------:|
| SwiftCompile | 325 | 271.245s |
| SwiftEmitModule | 30 | 23.625s |
| ... | ... | ... |

## Build Settings Audit

### Debug Configuration
- [x] `SWIFT_COMPILATION_MODE`: `(unset)` (recommended: `incremental`)
- [x] `SWIFT_OPTIMIZATION_LEVEL`: `-Onone` (recommended: `-Onone`)
- [x] `GCC_OPTIMIZATION_LEVEL`: `0` (recommended: `0`)
- [x] `ONLY_ACTIVE_ARCH`: `YES` (recommended: `YES`)
- [x] `DEBUG_INFORMATION_FORMAT`: `dwarf` (recommended: `dwarf`)
- [x] `ENABLE_TESTABILITY`: `YES` (recommended: `YES`)

### Release Configuration
- [x] `SWIFT_COMPILATION_MODE`: `wholemodule` (recommended: `wholemodule`)
- [x] `SWIFT_OPTIMIZATION_LEVEL`: `-O` (recommended: `-O`)
- ...

### Cross-Target Consistency
- [x] `SWIFT_COMPILATION_MODE` is consistent across all targets
- [ ] `OTHER_SWIFT_FLAGS` has target-level overrides: ...

## Compilation Diagnostics

| Duration | Kind | File | Line | Name |
|---------:|------|------|-----:|------|
| 150ms | function-body | MyView.swift | 42 | body |
| ... | ... | ... | ... | ... |

## Prioritized Recommendations

### 1. Recommendation title
**Category:** project
**Evidence:** ...
**Impact:** High
**Confidence:** High
**Risk:** Low

## Approval Checklist
- [ ] **1. Recommendation title** -- Impact: High | Risk: Low
- [ ] **2. Another recommendation** -- Impact: Medium | Risk: Low

## Next Steps

After implementing approved changes, re-benchmark with the same inputs:

...

Compare the new medians against the baseline to verify improvements.

## Verification (post-approval)

- Post-change clean median:
- Post-change incremental median:
- Clean delta:
- Incremental delta:

## Remaining follow-up ideas
- Item:
- Why it was deferred:

## Share your results

Add your improvement to the community results table by opening a pull request.
Copy the row below and append it to the table in README.md:

| <project-name> | <baseline-incremental> | <post-change-incremental> | <baseline-clean> | <post-change-clean> |

Open a PR: https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill/edit/main/README.md
```

## Usage Notes

- Keep approval-required items explicit.
- Do not imply that an unapproved recommendation was applied.
- If results are noisy, say that the verification is inconclusive instead of overstating success.
- The Build Settings Audit scope is strictly build performance. Do not flag language-migration settings like `SWIFT_STRICT_CONCURRENCY` or `SWIFT_UPCOMING_FEATURE_*`.
- The Compilation Diagnostics section is populated by `diagnose_compilation.py`. If not run, note that it was skipped.
