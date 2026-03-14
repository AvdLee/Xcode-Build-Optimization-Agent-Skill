# Build Optimization Sources

This file stores the external sources that the README and skill docs should cite consistently.

## Apple: Improving the speed of incremental builds

Source:

- <https://developer.apple.com/documentation/xcode/improving-the-speed-of-incremental-builds>

Key takeaways:

- Measure first with `Build With Timing Summary` or `xcodebuild -showBuildTimingSummary`.
- Accurate target dependencies improve correctness and parallelism.
- Run scripts should declare inputs and outputs so Xcode can skip unnecessary work.
- `.xcfilelist` files are appropriate when scripts have many inputs or outputs.
- Custom frameworks and libraries benefit from module maps, typically by enabling `DEFINES_MODULE`.
- Module reuse is strongest when related sources compile with consistent options.
- Breaking monolithic targets into better-scoped modules can reduce unnecessary rebuilds.

## Apple: Improving build efficiency with good coding practices

Source:

- <https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices>

Key takeaways:

- Use framework-qualified imports when module maps are available.
- Keep Objective-C bridging surfaces narrow.
- Prefer explicit type information when inference becomes expensive.
- Use explicit delegate protocols instead of overly generic delegate types.
- Simplify complex expressions that are hard for the compiler to type-check.

## Apple: Building your project with explicit module dependencies

Source:

- <https://developer.apple.com/documentation/xcode/building-your-project-with-explicit-module-dependencies>

Key takeaways:

- Explicit module builds make module work visible in the build log and improve scheduling.
- Repeated builds of the same module often point to avoidable module variants.
- Inconsistent build options across targets can force duplicate module builds.
- Timing summaries can reveal option drift that prevents module reuse.

## SwiftLee: Build performance analysis for speeding up Xcode builds

Source:

- <https://www.avanderlee.com/optimization/analysing-build-performance-xcode/>

Key takeaways:

- Clean and incremental builds should both be measured because they reveal different problems.
- Build Timeline and Build Timing Summary are practical starting points for build optimization.
- Build scripts often produce large incremental-build wins when guarded correctly.
- `-warn-long-function-bodies` and `-warn-long-expression-type-checking` help surface compile hotspots.
- Typical debug and release build setting mismatches are worth auditing, especially in older projects.

## Apple: Xcode Release Notes -- Compilation Caching

Source:

- Xcode Release Notes (149700201)

Key takeaways:

- Compilation caching is an opt-in feature for Swift and C-family languages.
- It caches prior compilation results and reuses them when the same source inputs are recompiled.
- Branch switching and clean builds benefit the most.
- Can be enabled via the "Enable Compilation Caching" build setting or per-user project settings.

## RocketSim Docs: Build Insights

Sources:

- <https://www.rocketsim.app/docs/features/build-insights/build-insights/>
- <https://www.rocketsim.app/docs/features/build-insights/team-build-insights/>

Key takeaways:

- RocketSim automatically tracks clean vs incremental builds over time without build scripts.
- It reports build counts, duration trends, and percentile-based metrics such as p75 and p95.
- Team Build Insights adds machine, Xcode, and macOS comparisons for cross-team visibility.
- This repository is best positioned as the point-in-time analyze-and-improve toolkit, while RocketSim is the monitor-over-time companion.
