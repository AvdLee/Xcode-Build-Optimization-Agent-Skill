<a href="https://www.rocketsim.app"><img src="assets/xcode-build-optimization-banner.jpg" alt="Xcode Build Optimization Agent Skills - Monitor your build performance with RocketSim" /></a>

# Xcode Build Optimization Agent Skills

Open-source Agent Skills for benchmarking and optimizing Xcode build performance across clean builds, incremental builds, compile hotspots, project settings, and Swift Package Manager overhead.

## Quick Start

Install all six skills (the orchestrator needs the specialist skills to work):

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill
```

Then open your Xcode project in your AI coding tool and say:

> Use the /xcode-build-orchestrator skill to analyze build performance and come up with a plan for improvements.

The agent will benchmark your clean and incremental builds, audit build settings, find compile hotspots, and produce an optimization plan at `.build-benchmark/optimization-plan.md`. No project files are modified until you explicitly approve changes.

For long-term monitoring across days, machines, Xcode versions, and teams, use [RocketSim Build Insights](https://www.rocketsim.app/docs/features/build-insights/build-insights/) and [Team Build Insights](https://www.rocketsim.app/docs/features/build-insights/team-build-insights/).

## Every Second Counts

A 1-second improvement on a 30-second incremental build sounds small. At 50 builds a day, that adds up to **3.5 hours per developer per year** -- or **35 hours across a team of ten**.

Most projects have several seconds of easy wins hiding in build settings, script phases, and compiler flags. This skill finds them.

## How It Works

The orchestrator coordinates five specialist skills in a recommend-first workflow. Nothing is modified until you approve.

```mermaid
flowchart LR
    Orchestrator --> Benchmark["Benchmark\n(clean + incremental)"]
    Benchmark --> Compilation["Compilation\nAnalyzer"]
    Benchmark --> Project["Project\nAnalyzer"]
    Benchmark --> SPM["SPM\nAnalyzer"]
    Compilation --> Plan["Optimization\nPlan"]
    Project --> Plan
    SPM --> Plan
    Plan --> You{{"You review\n& approve"}}
    You --> Fixer["Build\nFixer"]
    Fixer --> ReBenchmark["Re-benchmark\n& verify"]
```

**Phase 1 -- Analyze.** The orchestrator benchmarks your project, runs the three specialist analyzers, and produces a prioritized optimization plan at `.build-benchmark/optimization-plan.md`. No project files are modified.

> Use the Xcode build orchestrator to analyze build performance and come up with a plan for improvements.

**Phase 2 -- Fix.** Review the plan, check the approval boxes for the items you want, and ask the agent to apply them. The fixer implements only approved changes and re-benchmarks to verify.

> Implement the approved items from the optimization plan at .build-benchmark/optimization-plan.md, then re-benchmark to verify the improvements.

The plan file is your evidence trail -- shareable with teammates, reviewable in PRs, and diffable over time.

## What It Checks

The agent runs [over 40 individual checks](OPTIMIZATION-CHECKS.md) across build settings, project configuration, source code, and package dependencies.

| Check | What the agent looks for | |
|-------|--------------------------|---|
| Build settings audit | Debug/Release/General settings against best practices (compilation mode, optimization level, eager linking, compilation caching) | [Details](OPTIMIZATION-CHECKS.md#build-settings-audit) |
| Script phase analysis | Missing input/output declarations, scripts running unnecessarily, debug/simulator guards | [Details](OPTIMIZATION-CHECKS.md#script-phase-analysis) |
| Compile hotspot detection | Long type-checks, complex expressions, compiler diagnostic flags | [Details](OPTIMIZATION-CHECKS.md#compile-hotspot-detection) |
| Zero-change build overhead | Fixed-cost phases (codesign, validation, scripts) inflating incremental builds | [Details](OPTIMIZATION-CHECKS.md#zero-change-build-overhead) |
| Target dependency review | Accuracy, parallelism blockers, monolithic targets | [Details](OPTIMIZATION-CHECKS.md#target-dependency-review) |
| Module variant detection | Config drift across targets causing duplicate module builds | [Details](OPTIMIZATION-CHECKS.md#module-variant-detection) |
| SPM graph analysis | Plugin overhead, branch pins, package layering, circular dependencies | [Details](OPTIMIZATION-CHECKS.md#spm-graph-analysis) |
| Swift macro impact | Cascading rebuilds, swift-syntax universal builds | [Details](OPTIMIZATION-CHECKS.md#swift-macro-impact) |
| SwiftUI view decomposition | Monolithic body properties, result builder complexity | [Details](OPTIMIZATION-CHECKS.md#swiftui-view-decomposition) |
| Asset catalog parallelism | Single-threaded compilation bottleneck, splitting for parallel builds | [Details](OPTIMIZATION-CHECKS.md#asset-catalog-parallelism) |
| Access control optimization | Missing `final`, overly broad visibility inflating compiler work | [Details](OPTIMIZATION-CHECKS.md#access-control-optimization) |
| Incremental build diagnostics | Planning Swift module, SwiftEmitModule, Task Backtraces | [Details](OPTIMIZATION-CHECKS.md#incremental-build-diagnostics) |

## Community Results

Real-world improvements reported by developers who used these skills. Add your own by opening a pull request.

The `xcode-build-orchestrator` generates your table row at the end of every optimization run, so contributing is a single copy-paste.

| App | Clean Build | Incremental Build |
|-----|------------|-------------------|
| [Stock Analyzer](https://www.stock-analyzer.app) | 41.5s → 33.2s (-8.3s / 20% faster) | 5.3s → 3.6s (-1.7s / 32% faster) |
| [Enchanted](https://github.com/gluonfield/enchanted/pull/216) | 19.4s → 16.6s (-2.8s / 14% faster) | 2.5s → 2.2s (-0.3s / 12% faster) |
| [Wikipedia iOS](https://github.com/wikimedia/wikipedia-ios/pull/5740) | 48.7s → 46.5s (-2.2s / 5% faster) | 12.9s → 12.2s (-0.7s / 5% faster) |
| [Kickstarter iOS](https://github.com/kickstarter/ios-oss/pull/2808) | 83.4s → 83.5s (~0s / within noise) | 10.9s → 10.6s (-0.3s / 3% faster) |

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

The orchestrator is the recommended starting point -- it coordinates the other five skills automatically. Install all six skills so the orchestrator can access each specialist.

## Installation Options

### Option A: Using skills.sh

Install all six skills (required -- the orchestrator depends on the specialist skills):

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill
```

To install a single skill for standalone use, add the `--skill` flag:

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill --skill xcode-project-analyzer
```

Available individual skills: `xcode-build-benchmark`, `xcode-compilation-analyzer`, `xcode-project-analyzer`, `spm-build-analysis`, `xcode-build-orchestrator`, `xcode-build-fixer`. Note that the orchestrator requires all other skills to be installed.

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

### Option C: Cursor Plugin (coming soon)

This repository is packaged for Cursor plugin submission, but the marketplace listing is not live yet.

Once approved, you'll be able to install it from the Cursor Marketplace.

### Option D: Codex / OpenAI-compatible tools

This repository includes an `agents/openai.yaml` manifest. Copy or symlink the skill folders into your Codex skills directory:

```bash
cp -R skills/ "$CODEX_HOME/skills/"
```

See [Codex skills documentation](https://developers.openai.com/codex/skills/#where-to-save-skills) for details on where to save skills.

### Option E: Manual Install

1. Clone this repository.
2. Install or symlink the specific skill folder from `skills/` that you want.
3. Ask your AI coding tool to use the corresponding skill.

Useful docs: [Codex Skills](https://developers.openai.com/codex/skills/#where-to-save-skills) | [Claude Code Agent Skills](https://code.claude.com/en/skills) | [Cursor Skills](https://cursor.com/docs/context/skills#enabling-skills)

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

## See Also My Other Skills

- [Swift Concurrency Expert](https://github.com/AvdLee/Swift-Concurrency-Agent-Skill)
- [SwiftUI Expert](https://github.com/AvdLee/SwiftUI-Agent-Skill)
- [Core Data Expert](https://github.com/AvdLee/Core-Data-Agent-Skill)
- [Swift Testing Expert](https://github.com/AvdLee/Swift-Testing-Agent-Skill)

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
skills/
  xcode-build-benchmark/
    SKILL.md
    references/
      benchmarking-workflow.md
  xcode-compilation-analyzer/
    SKILL.md
    references/
      code-compilation-checks.md
  xcode-project-analyzer/
    SKILL.md
    references/
      project-audit-checks.md
  spm-build-analysis/
    SKILL.md
    references/
      spm-analysis-checks.md
  xcode-build-orchestrator/
    SKILL.md
    references/
      orchestration-report-template.md
  xcode-build-fixer/
    SKILL.md
    references/
      fix-patterns.md
```
<!-- END SKILL STRUCTURE -->

## Research Basis

All checks are grounded in Apple documentation, WWDC sessions, and proven community practices. See [OPTIMIZATION-CHECKS.md](OPTIMIZATION-CHECKS.md) for the full list of checks with references to each source.

The stored reference summaries live in `references/build-optimization-sources.md`.

## RocketSim Positioning

This repo helps you optimize point-in-time build performance with an agent-guided workflow.

RocketSim complements it by monitoring build performance over time:

- automatic clean vs incremental build tracking
- duration trends and percentile metrics
- machine, Xcode, and macOS comparisons
- team-wide visibility without custom build scripts

If you want to catch regressions earlier and see whether your build times are improving over weeks or months, use [RocketSim Build Insights](https://www.rocketsim.app/docs/features/build-insights/build-insights/) after you apply the improvements from this repo.

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
