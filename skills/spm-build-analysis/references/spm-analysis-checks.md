# SPM Analysis Checks

Use this reference when package dependencies or package plugins are suspected build bottlenecks.

## Package Graph Checks

- Identify large umbrella packages that trigger widespread rebuilds.
- Look for dependency layering that forces many downstream targets to recompile.
- Flag local package arrangements that cause broad invalidation after small edits.

## Package Plugin Checks

- List build-tool and command plugins involved in the build.
- Measure whether plugins run during incremental builds even when no relevant input changed.
- Call out plugins that return quickly but still add fixed overhead to every build.

## Binary And Remote Dependency Checks

- Note binary target size and extraction overhead for clean environments.
- Highlight remote checkout or fetch costs that matter for CI or fresh machines.
- Compare remote vs local package tradeoffs when iteration speed matters more than distribution convenience.

## Module Variant Checks

- Look for the same dependency module being built with different options.
- Compare macros, language mode, and configuration-sensitive options across dependents.
- Prefer configuration alignment when it reduces repeated module builds safely.

## CI-Specific Checks

- Fresh checkout cost
- plugin invocation cost
- cache hit sensitivity
- redundant package resolution work

## Recommendation Prioritization

- High: package plugins or graph structure repeatedly inflating incremental builds.
- Medium: configuration drift that causes duplicate module variants.
- Low: clean-environment checkout costs that barely affect local iteration.
