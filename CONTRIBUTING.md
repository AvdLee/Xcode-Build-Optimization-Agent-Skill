# Contributing to Xcode Build Optimization Agent Skills

Thanks for helping improve this repository. Contributions are welcome when they keep the repo focused on Xcode build analysis, deterministic benchmarking, and recommend-first optimization guidance.

## About This Repository

This is a multi-skill repository that follows the Agent Skills open format:

- Skills live under `skills/`, each with a `SKILL.md` entrypoint. Each skill bundles its own scripts, references, and schemas so it works after standalone installation.
- Canonical copies of shared files live in `references/`, `schemas/`, and `scripts/` at the repo root. When a root-level file changes, update the copies inside every skill that bundles it (see "Keeping shared files in sync" below).
- The skills are intentionally recommend-first. They should not make project or source changes without explicit developer approval.

## Recommended Workflow

### Use skill-authoring assistance

If you have access to a skill-authoring assistant such as `skill-creator`, use it when updating any `SKILL.md` or reference file. That helps preserve:

- valid YAML frontmatter
- concise, trigger-oriented descriptions
- progressive disclosure into reference files
- consistent terminology across the six skills

### Keep the repo on mission

Contributions should stay within Xcode build optimization topics:

- benchmark design and interpretation
- compile hotspot analysis
- project and scheme build settings
- build script behavior
- Swift Package Manager build overhead
- explicit module dependency and module variant analysis

Avoid broad iOS architecture guidance, CI platform evangelism, or product documentation unrelated to build optimization.

## Quality Standards

### Skill quality

- Every `SKILL.md` must include valid `name` and `description` frontmatter.
- Descriptions must clearly state what the skill does and when to use it.
- Keep `SKILL.md` concise; push deep details into nearby reference files.
- Preserve recommend-first behavior, especially in `xcode-build-orchestrator`.

### Technical quality

- Prefer deterministic instructions over vague advice.
- Cite Apple guidance, the SwiftLee article, or RocketSim docs when changing shared source summaries.
- Keep benchmark and recommendation formats consistent with `schemas/build-benchmark.schema.json` and `references/recommendation-format.md`.
- Avoid destructive automation. Scripts should gather evidence or format reports, not rewrite user projects.

### Scripts and automation

- Keep helper scripts dependency-light and portable.
- Use standard library tooling when possible.
- Avoid network calls in scripts and GitHub Actions unless they are clearly required.
- If you add or rename reference files, update the README structure block or let the sync workflow do it.

### Keeping shared files in sync

Each skill bundles copies of the scripts and references it needs. The root-level `scripts/`, `references/`, and `schemas/` directories hold the canonical versions. When you change a root-level file, copy the updated version into every skill folder that includes it:

| Root file | Bundled in skills |
|-----------|-------------------|
| `scripts/benchmark_builds.py` | xcode-build-benchmark, xcode-build-orchestrator, xcode-build-fixer |
| `scripts/diagnose_compilation.py` | xcode-compilation-analyzer, xcode-build-orchestrator |
| `scripts/generate_optimization_report.py` | xcode-build-orchestrator |
| `scripts/check_spm_pins.py` | spm-build-analysis |
| `references/benchmark-artifacts.md` | xcode-build-benchmark, xcode-build-orchestrator |
| `references/build-settings-best-practices.md` | xcode-project-analyzer, xcode-build-orchestrator, xcode-build-fixer |
| `references/recommendation-format.md` | xcode-compilation-analyzer, xcode-project-analyzer, spm-build-analysis, xcode-build-orchestrator, xcode-build-fixer |
| `references/build-optimization-sources.md` | xcode-compilation-analyzer, xcode-project-analyzer, spm-build-analysis |
| `schemas/build-benchmark.schema.json` | xcode-build-benchmark |

## Typical Contribution Types

- Improve one of the six skill entrypoints.
- Add a focused reference file for a missing Xcode build topic.
- Improve the benchmark schema or helper scripts.
- Clarify README installation or usage guidance.
- Update the stored source summaries as Apple or RocketSim docs evolve.
- Add your optimization results to the Community Results table in the README.

## Pull Request Process

1. Create a focused branch.
2. Keep related changes grouped together.
3. Verify the changed markdown still reads well as an Agent Skill.
4. If you touched scripts or workflows, run a quick sanity check locally.
5. Open a PR with a short summary, rationale, and any validation notes.

## Development Notes

- The README structure block is maintained by `.github/scripts/sync-readme.js`.
- Release automation bumps the shared plugin metadata version in `.claude-plugin/`.
- `.agents/product-marketing-context.md` is an internal draft aid and is intentionally ignored by Git.

## Resources

- Agent Skills format: <https://agentskills.io/home>
- Claude Code Agent Skills docs: <https://code.claude.com/en/skills>
- Apple Xcode build optimization docs: see `references/build-optimization-sources.md`
- SwiftLee build performance article: <https://www.avanderlee.com/optimization/analysing-build-performance-xcode/>

## Code of Conduct

Be respectful, specific, and evidence-driven. Favor measurable build improvements over subjective preferences.
