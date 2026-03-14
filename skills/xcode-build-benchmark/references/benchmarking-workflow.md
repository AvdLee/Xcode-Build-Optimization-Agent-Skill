# Benchmarking Workflow

Use this reference when you need the full operational contract for collecting Xcode build measurements.

## Goal

Produce a benchmark artifact that another skill can trust without rerunning the same setup discovery.

## Benchmark Contract

- Measure both clean and incremental builds unless the user narrows the scope.
- Use the same scheme, configuration, destination, and command flags for all measured runs.
- Record the exact command and any environment overrides.
- Keep clean and incremental runs in separate arrays in the artifact.
- Save wall-clock timing plus any parsed timing-summary categories.

## Suggested Run Counts

- Clean builds: 3 measured runs
- Incremental builds: 3 measured runs
- Warm-up: 0 to 1 validation run, excluded from the summary unless the user explicitly wants it included

## Clean Build Rules

- Clear build products with `xcodebuild clean` or an equivalent clean-build-folder step before each measured clean run.
- Do not change scheme, destination, or configuration between runs.
- If the command fails, store the failure and stop rather than mixing failed and successful runs.

## Incremental Build Rules

- Use the same build command after a successful baseline build.
- Do not clean between incremental runs.
- If the user wants edit-loop benchmarking, note the file change strategy explicitly in the artifact.
- If there are no source edits between runs, label the result as no-edit incremental timing.

## What To Capture

At minimum, keep:

- timestamp
- host machine info if available
- Xcode version if available
- workspace or project path
- scheme, configuration, destination
- exact `xcodebuild` command
- duration per run
- success or failure
- parsed timing-summary categories
- notes on warm-up behavior or unusual noise

## Reporting Guidance

Use medians for the headline number. Also include:

- min and max
- range
- category totals from the timing summary
- obvious outliers or instability

## Handoff Expectations

The next optimization skill should be able to answer:

- Is the main problem clean, incremental, or both?
- Which build categories dominate time?
- Which command produced the evidence?
- Is the baseline trustworthy enough to compare before and after changes?
