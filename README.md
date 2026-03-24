# Xcode Build Optimization Agent Skills

Open-source Agent Skills for benchmarking and optimizing Xcode build performance across clean builds, incremental builds, compile hotspots, project settings, and Swift Package Manager overhead.

## Quick Start

Install the orchestrator skill:

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill --skill xcode-build-orchestrator
```

Then open your Xcode project in your AI coding tool and say:

> Use the Xcode build orchestrator to analyze build performance and come up with a plan for improvements.

The agent will benchmark your clean and incremental builds, audit build settings, find compile hotspots, and produce an optimization plan at `.build-benchmark/optimization-plan.md`. No project files are modified until you explicitly approve changes.

[See results of projects that used this skill →](#community-results)

For long-term monitoring across days, machines, Xcode versions, and teams, use [RocketSim Build Insights](https://www.rocketsim.app/docs/features/build-insights/build-insights/) and [Team Build Insights](https://www.rocketsim.app/docs/features/build-insights/team-build-insights/).

## See Also My Other Skills

- [Swift Concurrency Expert](https://github.com/AvdLee/Swift-Concurrency-Agent-Skill)
- [SwiftUI Expert](https://github.com/AvdLee/SwiftUI-Agent-Skill)
- [Core Data Expert](https://github.com/AvdLee/Core-Data-Agent-Skill)
- [Swift Testing Expert](https://github.com/AvdLee/Swift-Testing-Agent-Skill)

## Who This Is For

- iOS and macOS teams with slow local build loops
- developers investigating a recent build-time regression
- teams that want evidence-backed Xcode build optimization instead of guesswork
- developers who want a reusable Agent Skills package, not a one-off script

## Included Skills

| Skill | Purpose |
|-------|---------|
| `xcode-build-orchestrator` | End-to-end workflow: benchmark, analyze, prioritize, approve, fix, re-benchmark |
| `xcode-build-benchmark` | Repeatable clean and incremental build benchmarks with timestamped artifacts |
| `xcode-compilation-analyzer` | Swift compile hotspot analysis and source-level recommendations |
| `xcode-project-analyzer` | Build settings, scheme, script phase, and target dependency auditing |
| `spm-build-analysis` | Package graph, plugin overhead, and module variant review |
| `xcode-build-fixer` | Apply approved optimization changes and verify with benchmarks |

The orchestrator is the recommended starting point -- it coordinates the other five skills automatically.

## Installation Options

### Option A: Using skills.sh

Install a single skill:

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill --skill xcode-build-orchestrator
```

Or install any of the six skills individually: `xcode-build-benchmark`, `xcode-compilation-analyzer`, `xcode-project-analyzer`, `spm-build-analysis`, `xcode-build-orchestrator`, `xcode-build-fixer`.

### Option B: Claude Code Plugin

1. Add the marketplace:

```bash
/plugin marketplace add AvdLee/Xcode-Build-Optimization-Agent-Skill
```

2. Install the plugin:

```bash
/plugin install xcode-build-skills@xcode-build-skills
```

To enable for everyone in a repository, add to your project configuration:

```json
{
  "enabledPlugins": {
    "xcode-build-skills@xcode-build-skills": true
  },
  "extraKnownMarketplaces": {
    "xcode-build-skills": {
      "source": {
        "source": "github",
        "repo": "AvdLee/Xcode-Build-Optimization-Agent-Skill"
      }
    }
  }
}
```

### Option C: Manual Install

1. Clone this repository.
2. Install or symlink the specific skill folder from `skills/` that you want.
3. Ask your AI coding tool to use the corresponding skill.

Useful docs: [Codex Skills](https://developers.openai.com/codex/skills/#where-to-save-skills) | [Claude Code Agent Skills](https://code.claude.com/en/skills) | [Cursor Skills](https://cursor.com/docs/context/skills#enabling-skills)

## How It Works

The orchestrator uses a two-phase recommend-first workflow that separates analysis from implementation.

**Phase 1 -- Analyze.** The agent benchmarks your project, runs all specialist analyses, and produces a markdown optimization plan at `.build-benchmark/optimization-plan.md`. The plan includes baseline benchmarks, a build settings audit, compilation diagnostics, and prioritized recommendations with an approval checklist. No project files are modified.

> Use the Xcode build orchestrator to analyze build performance and come up with a plan for improvements.

**Phase 2 -- Fix.** After reviewing the plan, check the approval boxes for the recommendations you want and ask the agent to implement them. It applies only the approved changes, re-benchmarks, and reports the measured improvement.

> Implement the approved items from the optimization plan at .build-benchmark/optimization-plan.md, then re-benchmark to verify the improvements.

The plan file becomes the evidence trail -- shareable with teammates, reviewable in pull requests, and diffable over time.

## Why Clean And Incremental Builds Both Matter

Clean builds expose:

- package and module setup cost
- full project graph overhead
- target structure and explicit-module issues

Incremental builds expose:

- edit-loop pain
- run script bottlenecks
- cache invalidation problems
- repeated package-plugin overhead

That distinction is central to this repo and follows both Apple's Xcode guidance and the SwiftLee workflow in [Build performance analysis for speeding up Xcode builds](https://www.avanderlee.com/optimization/analysing-build-performance-xcode/).

## Shared Support Layer

The skills share:

- a common `.build-benchmark/` artifact contract
- a shared JSON schema for benchmark output
- helper scripts for benchmarking, timing-summary parsing, compilation diagnostics, report generation, and recommendation rendering
- a build settings best practices reference for the pass/fail audit
- a single source summary file so README and skill guidance stay aligned

## Skill Structure
<!-- BEGIN SKILL STRUCTURE -->
```text
xcode-build-optimization-agent-skill/
  .claude-plugin/
    marketplace.json
    plugin.json
  references/
    benchmark-artifacts.md
    build-optimization-sources.md
    build-settings-best-practices.md
    recommendation-format.md
  schemas/
    build-benchmark.schema.json
  scripts/
    benchmark_builds.py
    diagnose_compilation.py
    generate_optimization_report.py
    render_recommendations.py
    summarize_build_timing.py
  skills/
    xcode-build-benchmark/
      SKILL.md
      references/
        benchmarking-workflow.md - Benchmark contract, clean vs incremental rules, and artifact expectations
    xcode-compilation-analyzer/
      SKILL.md
      references/
        code-compilation-checks.md - Swift compile hotspot checks and code-level heuristics
    xcode-project-analyzer/
      SKILL.md
      references/
        project-audit-checks.md - Build setting, script phase, and dependency audit checklist
    spm-build-analysis/
      SKILL.md
      references/
        spm-analysis-checks.md - Package graph, plugin overhead, and module variant review guide
    xcode-build-orchestrator/
      SKILL.md
      references/
        orchestration-report-template.md - Prioritization, approval, and verification report template
    xcode-build-fixer/
      SKILL.md
      references/
        fix-patterns.md - Concrete before/after patterns for each fix category
```
<!-- END SKILL STRUCTURE -->

## Research Basis

This repo deliberately aligns with:

- Apple's incremental-build guidance: accurate target dependencies, script input/output declarations, module maps, and parallel-friendly project structure
- Apple's compile-efficiency guidance: explicit type information, simpler expressions, narrower bridging surfaces, and framework-qualified imports
- Apple's explicit module dependency guidance: reducing duplicate module variants caused by configuration drift
- the SwiftLee workflow for measuring with Build Timeline, Build Timing Summary, and Swift frontend diagnostics

The stored reference summaries live in `references/build-optimization-sources.md`.

## RocketSim Positioning

This repo helps you optimize point-in-time build performance with an agent-guided workflow.

RocketSim complements it by monitoring build performance over time:

- automatic clean vs incremental build tracking
- duration trends and percentile metrics
- machine, Xcode, and macOS comparisons
- team-wide visibility without custom build scripts

If you want to catch regressions earlier and see whether your build times are improving over weeks or months, use [RocketSim Build Insights](https://www.rocketsim.app/docs/features/build-insights/build-insights/) after you apply the improvements from this repo.

## Community Results

Real-world improvements reported by developers who used these skills. Add your own by opening a pull request.

The `xcode-build-orchestrator` generates your table row at the end of every optimization run, so contributing is a single copy-paste.

| App | Clean Build | Incremental Build |
|-----|------------|-------------------|
| [StockAnalyzer](https://www.avanderlee.com) | 41.5s → 33.2s (-8.3s / 20% faster) | 5.3s → 3.6s (-1.7s / 32% faster) |
| [Enchanted](https://github.com/gluonfield/enchanted/pull/216) | 19.4s → 16.6s (-2.8s / 14% faster) | 2.5s → 2.2s (-0.3s / 12% faster) |
| [Wikipedia iOS](https://github.com/wikimedia/wikipedia-ios/pull/5740) | 48.7s → 46.5s (-2.2s / 5% faster) | 12.9s → 12.2s (-0.7s / 5% faster) |
| [Kickstarter iOS](https://github.com/kickstarter/ios-oss/pull/2808) | 83.4s → 83.5s (~0s / within noise) | 10.9s → 10.6s (-0.3s / 3% faster) |

## Contributing

Contributions are welcome when they keep the repo focused on Xcode build optimization and Agent Skills format quality.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- skill-authoring guidance
- repo scope and quality standards
- workflow notes for scripts and README sync

## About The Author

Created by [Antoine van der Lee](https://www.avanderlee.com), creator of SwiftLee and RocketSim. The practical build workflow in this repository is informed by the SwiftLee article [Build performance analysis for speeding up Xcode builds](https://www.avanderlee.com/optimization/analysing-build-performance-xcode/) and ongoing work on RocketSim Build Insights.

## License

This repository is available under the MIT License. See [LICENSE](LICENSE) for details.
