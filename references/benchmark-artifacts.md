# Benchmark Artifacts

All skills in this repository should treat `.build-benchmark/` as the canonical location for measured build evidence.

## Goals

- Keep build measurements reproducible.
- Make clean and incremental build data easy to compare.
- Preserve enough context for later specialist analysis without rerunning the benchmark.

## File Layout

Recommended outputs:

- `.build-benchmark/<timestamp>-<scheme>.json`
- `.build-benchmark/<timestamp>-<scheme>-clean-1.log`
- `.build-benchmark/<timestamp>-<scheme>-clean-2.log`
- `.build-benchmark/<timestamp>-<scheme>-clean-3.log`
- `.build-benchmark/<timestamp>-<scheme>-incremental-1.log`
- `.build-benchmark/<timestamp>-<scheme>-incremental-2.log`
- `.build-benchmark/<timestamp>-<scheme>-incremental-3.log`

Use an ISO-like UTC timestamp without spaces so the files sort naturally.

## Artifact Requirements

Each JSON artifact should include:

- schema version
- creation timestamp
- project context
- environment details when available
- the normalized build command
- separate `clean` and `incremental` run arrays
- summary statistics for each build type
- parsed timing-summary categories
- free-form notes for caveats or noise

## Clean And Incremental Separation

Do not merge clean and incremental measurements into a single list. They answer different questions:

- Clean builds show full build-system, package, and module setup cost.
- Incremental builds show edit-loop productivity and script or cache invalidation problems.

## Raw Logs

Store raw `xcodebuild` output beside the JSON artifact whenever possible. That allows later skills to:

- re-parse timing summaries
- inspect failed builds
- search for long type-check warnings
- correlate build-system phases with recommendations

## Shared Consumer Expectations

Any skill reading a benchmark artifact should be able to identify:

- what was measured
- how it was measured
- whether the run succeeded
- whether the results are stable enough to compare

For the authoritative field-level schema, see [../schemas/build-benchmark.schema.json](../schemas/build-benchmark.schema.json).
