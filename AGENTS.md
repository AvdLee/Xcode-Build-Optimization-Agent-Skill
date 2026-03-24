# Agent Guidance

This is a multi-skill Xcode build optimization repository.

## Layout

- `skills/` contains six installable Agent Skills, each with a `SKILL.md` entrypoint. Each skill bundles its own scripts, references, and schemas so it works after standalone installation.
- `references/`, `schemas/`, and `scripts/` at the repo root are canonical copies of the shared support files. Changes to these must be synced into the skill folders that use them (see CONTRIBUTING.md).
- `.claude-plugin/` contains plugin and marketplace metadata.

## Skills

| Skill | Purpose |
|-------|---------|
| `xcode-build-benchmark` | Repeatable clean and incremental build benchmarking |
| `xcode-compilation-analyzer` | Swift compile hotspot analysis and source-level recommendations |
| `xcode-project-analyzer` | Build settings, scheme, script phase, and target dependency auditing |
| `spm-build-analysis` | Package graph, plugin overhead, and module variant review |
| `xcode-build-orchestrator` | Orchestrator: benchmark, analyze, prioritize, approve, delegate fixes, re-benchmark |
| `xcode-build-fixer` | Apply approved optimization changes and verify with benchmarks |

## Rules

- Wall-clock build time (how long the developer waits) is the primary success metric. Every recommendation must state its expected impact on wall-clock time. If the impact cannot be predicted, say so.
- Cumulative task time from the Build Timing Summary is diagnostic evidence, not proof of wall-time impact. Xcode parallelizes aggressively, so reducing parallel task time may produce zero wait-time improvement.
- Recommend-first by default. Never apply project, source, or package changes without explicit developer approval.
- Benchmark before optimizing. Use `.build-benchmark/` artifacts as evidence.
- Treat clean and incremental builds as separate metrics.
- The orchestrator (`xcode-build-orchestrator`) is the primary entrypoint for end-to-end work.
- Each skill bundles its own copies of scripts, references, and schemas for standalone installation. Root-level `scripts/`, `references/`, and `schemas/` are the canonical copies; keep both layers in sync.

## Handoff Between Skills

When one skill identifies an issue outside its scope, read the target skill's `SKILL.md` under `skills/` and apply its workflow to the same project context. Pass along any benchmark artifacts or timing evidence already collected.

## Documentation Sync

- When a skill adds, removes, or changes an optimization check, update the matching row in the "What It Checks" table in `README.md` and the corresponding section in `OPTIMIZATION-CHECKS.md`.
- When a new external reference (Apple doc, WWDC session, article) is used by a check, add it to the relevant section in `OPTIMIZATION-CHECKS.md` and to `references/build-optimization-sources.md`.
- When a skill is added or removed, update the "Included Skills" table in `README.md`, the Skills table in this file, and the Skill Structure tree (between the `<!-- BEGIN SKILL STRUCTURE -->` / `<!-- END SKILL STRUCTURE -->` markers in `README.md`).
- `OPTIMIZATION-CHECKS.md` is the single source of truth for what the agent checks and why. Skill-internal reference docs (under `skills/*/references/`) contain implementation detail; `OPTIMIZATION-CHECKS.md` is the developer-facing summary. Keep both layers consistent but do not duplicate implementation detail into `OPTIMIZATION-CHECKS.md`.
