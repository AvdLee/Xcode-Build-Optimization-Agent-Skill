# Xcode Build Optimization Agent Skills

Open-source Agent Skills for benchmarking and optimizing Xcode build performance across clean builds, incremental builds, compile hotspots, project settings, and Swift Package Manager overhead.

This repository is the "analyze and improve now" toolkit:

- benchmark both clean and incremental builds
- identify the biggest code, project, and package bottlenecks
- prioritize measured improvements
- keep the workflow recommend-first until a developer explicitly approves changes

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

This repo ships six installable skills:

- `xcode-build-benchmark`
- `xcode-compilation-analyzer`
- `xcode-project-analyzer`
- `spm-build-analysis`
- `xcode-build-orchestrator`
- `xcode-build-fixer`

### What Each Skill Does

- `xcode-build-benchmark`: Runs repeatable clean and incremental build benchmarks and writes timestamped `.build-benchmark/` artifacts.
- `xcode-compilation-analyzer`: Uses timing summaries and Swift frontend diagnostics to rank compile hotspots and source-level improvements.
- `xcode-project-analyzer`: Audits schemes, target dependencies, scripts, and build settings for project-level wins.
- `spm-build-analysis`: Reviews package graph shape, build plugins, module variants, and CI-sensitive dependency overhead.
- `xcode-build-orchestrator`: Orchestrates the full workflow in two phases: analyze in plan mode (benchmark, run specialists, produce an optimization plan), then delegate approved fixes to the fixer in agent mode and re-benchmark.
- `xcode-build-fixer`: Applies approved optimization changes (build settings, script phases, source-level fixes, SPM restructuring) and re-benchmarks to verify improvement.

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

## How To Use These Skills

### Option A: Using skills.sh

Install a single skill:

```bash
npx skills add https://github.com/avdlee/xcode-build-optimization-agent-skill --skill xcode-build-benchmark
```

Swap the skill name for any of the six skills under `skills/`:

- `xcode-build-benchmark`
- `xcode-compilation-analyzer`
- `xcode-project-analyzer`
- `spm-build-analysis`
- `xcode-build-orchestrator`
- `xcode-build-fixer`

Start in plan mode and ask:

> Use the xcode build orchestrator skill and analyze the current project for clean and incremental build improvements.

The agent produces `.build-benchmark/optimization-plan.md`. Review it, check the approval boxes, then switch to agent mode to implement.

### Option B: Claude Code Plugin

Install the shared plugin to make all six skills available under one namespace.

#### Personal Usage

1. Add the marketplace:

```bash
/plugin marketplace add AvdLee/Xcode-Build-Optimization-Agent-Skill
```

2. Install the plugin:

```bash
/plugin install xcode-build-skills@xcode-build-skills
```

The installed skill names will be available under the `xcode-build-skills` namespace.

#### Project Configuration

To enable the plugin for everyone working in a repository:

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

Useful docs:

- [Codex Skills](https://developers.openai.com/codex/skills/#where-to-save-skills)
- [Claude Code Agent Skills](https://code.claude.com/en/skills)
- [Cursor Skills](https://cursor.com/docs/context/skills#enabling-skills)

## Recommend-First Workflow

The orchestrator uses a two-phase approach that separates analysis from implementation. This keeps the developer in control and produces a reviewable artifact before anything changes.

### Phase 1 -- Analyze in plan mode

Start the orchestrator in **plan mode** (read-only). The agent benchmarks your project, runs all specialist analyses, and produces a markdown optimization plan at `.build-benchmark/optimization-plan.md`.

The plan includes:

- baseline benchmark results with a full timing summary table
- a build settings audit with pass/fail indicators for Debug and Release
- compilation diagnostics showing type-checking hotspots (if any)
- prioritized recommendations with evidence, impact estimates, and risk levels
- an approval checklist where you check the items you want implemented

Example prompt for plan mode:

> Use the xcode build orchestrator skill and analyze the current project for clean and incremental build improvements.

The agent will benchmark, analyze, and stop after producing the plan. No project files are modified.

### Phase 2 -- Execute in agent mode

After reviewing the plan, switch to **agent mode** and ask the agent to implement the approved items. It reads the optimization plan, applies only the checked recommendations, re-benchmarks with the same inputs, and reports the measured improvement.

Example prompt for agent mode:

> Implement the approved items from the optimization plan at .build-benchmark/optimization-plan.md, then re-benchmark to verify the improvements.

This two-phase approach is suitable for real repositories where build settings, package manifests, and source changes should never be modified casually. The plan file becomes the evidence trail -- shareable with teammates, reviewable in pull requests, and diffable over time.

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

Real-world improvements reported by developers who used these skills. Add your own results by opening a pull request.

The `xcode-build-orchestrator` generates your table row at the end of every optimization run, so contributing is a single copy-paste.

| App | Incremental Before | Incremental After | Clean Before | Clean After |
|-----|-------------------:|------------------:|-------------:|------------:|

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
