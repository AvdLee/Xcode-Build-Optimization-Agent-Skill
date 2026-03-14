# GitHub Copilot Instructions: Xcode Build Optimization Skills

Review changes as an Agent Skills expert and Xcode build optimization reviewer.

## Repository Mission

Keep this repository focused on:

- Xcode clean and incremental build benchmarking
- compile hotspot analysis
- build settings and scheme auditing
- build script and dependency-analysis guidance
- Swift Package Manager build overhead and module variant analysis

Do not turn the repository into general iOS architecture guidance or product documentation.

## Agent Skill Requirements

- Every skill directory must contain a `SKILL.md` with valid `name` and `description` frontmatter.
- Descriptions must state both what the skill does and when to use it.
- Keep `SKILL.md` concise and delegate deeper material to one-level-deep reference files.
- Reference files should be discoverable from the matching `SKILL.md`.

## Behavior Constraints

- Default to recommend-first behavior.
- Never introduce instructions that apply project, build-setting, or source changes without explicit developer approval.
- Preserve evidence-driven workflows: command used, build type, target or package affected, and measured impact.
- Prefer deterministic shell commands and structured artifacts over ad hoc prose.

## Build Optimization Focus Areas

When reviewing changes, prioritize:

1. Benchmark correctness
   - clean vs incremental builds are treated separately
   - warm-up and repetition rules are explicit
   - output artifacts are stored in `.build-benchmark/`

2. Evidence quality
   - recommendations cite timing summaries, script phases, compiler diagnostics, or dependency data
   - estimated impact and confidence are separated from observed evidence

3. Apple-aligned guidance
   - target dependencies and build order accuracy
   - script input/output declarations and `.xcfilelist` usage
   - `DEFINES_MODULE`, module maps, and framework-qualified imports
   - explicit module dependency and module variant reduction guidance
   - explicit type information and simpler expressions for Swift compile efficiency

4. Safety
   - scripts should analyze and format data, not mutate user projects
   - workflows should avoid surprising side effects

## Common Issues to Flag

- Vague skill descriptions with no trigger conditions
- Overlong `SKILL.md` files that duplicate reference content
- Advice that skips measuring before optimizing
- Guidance that ignores incremental builds
- Destructive automation or auto-fix behavior without approval
- Inconsistent benchmark or recommendation fields across files

## Useful References

- `references/build-optimization-sources.md`
- `references/benchmark-artifacts.md`
- `references/recommendation-format.md`
- `schemas/build-benchmark.schema.json`
