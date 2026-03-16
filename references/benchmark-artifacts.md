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

## Measurement Caveats

### COMPILATION_CACHING

`COMPILATION_CACHING = YES` stores compiled artifacts so that repeated compilations of identical inputs are served from cache. The standard benchmark methodology (clean + build) clears derived data before each clean run, which invalidates the compilation cache. As a result, the benchmark script does not capture the benefit of compilation caching.

The real benefit of compilation caching appears during:

- Repeat clean builds where source files have not changed (e.g., after switching branches and switching back).
- CI builds that share a persistent derived-data directory across runs.

When reporting on COMPILATION_CACHING, note that the standard clean-build benchmark cannot measure its impact. Recommend enabling it based on the well-documented benefit rather than requiring a measurable delta from the benchmark script.

### First-Run Variance

The first clean build after the warmup cycle often runs 20-40% slower than subsequent clean builds due to cold OS-level caches (disk I/O, dynamic linker cache, etc.). The benchmark script mitigates this by running a warmup clean+build cycle before measured runs. If variance between the first and later clean runs is still high, prefer the median or min over the mean, and note the variance in the artifact's `notes` field.

## Shared Consumer Expectations

Any skill reading a benchmark artifact should be able to identify:

- what was measured
- how it was measured
- whether the run succeeded
- whether the results are stable enough to compare

For the authoritative field-level schema, see [../schemas/build-benchmark.schema.json](../schemas/build-benchmark.schema.json).
