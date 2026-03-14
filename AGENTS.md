# Agent Guidance

This is a multi-skill Xcode build optimization repository.

## Layout

- `skills/` contains five installable Agent Skills, each with a `SKILL.md` entrypoint.
- `references/`, `schemas/`, and `scripts/` at the repo root are shared support files used by the skills.
- `.claude-plugin/` contains plugin and marketplace metadata.

## Skills

| Skill | Purpose |
|-------|---------|
| `xcode-build-benchmark` | Repeatable clean and incremental build benchmarking |
| `xcode-code-compilation-optimizer` | Swift compile hotspot analysis and source-level recommendations |
| `xcode-project-optimizer` | Build settings, scheme, script phase, and target dependency auditing |
| `spm-build-analysis` | Package graph, plugin overhead, and module variant review |
| `xcode-build-optimizer` | Orchestrator: benchmark, analyze, prioritize, approve, implement, re-benchmark |

## Rules

- Recommend-first by default. Never apply project, source, or package changes without explicit developer approval.
- Benchmark before optimizing. Use `.build-benchmark/` artifacts as evidence.
- Treat clean and incremental builds as separate metrics.
- The orchestrator (`xcode-build-optimizer`) is the primary entrypoint for end-to-end work.
- Shared references and schemas live at the repo root, not inside individual skills.

## Handoff Between Skills

When one skill identifies an issue outside its scope, read the target skill's `SKILL.md` under `skills/` and apply its workflow to the same project context. Pass along any benchmark artifacts or timing evidence already collected.
