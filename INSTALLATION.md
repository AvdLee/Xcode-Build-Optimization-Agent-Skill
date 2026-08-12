# All Installation Options

The [README](README.md) covers the recommended installation paths: [skills.sh](README.md#option-a-using-skillssh-recommended), the OpenAI Plugins Directory (ChatGPT & Codex), Claude Code, and Cursor. This file lists every other supported client.

> Note: this plugin contains six skills. The orchestrator (`xcode-build-orchestrator`) depends on the five specialist skills, so install all of them unless you only need a single specialist standalone.

## pi package manager

Install via [pi](https://github.com/mariozechner/pi-mono):
```bash
pi install https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill
```

The skills will be available automatically in pi sessions.

## Gemini CLI

Install globally (user-level skills available in all Gemini CLI sessions):
```bash
gemini skills install https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill
```

Or install at workspace level so the skills are shared with your team via version control:
```bash
gemini skills install https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill --scope workspace
```

You can verify the installation with:
```bash
gemini skills list
```

For more information, see the [Gemini CLI Agent Skills documentation](https://geminicli.com/docs/cli/skills/).

## Autohand Code

Install the skills globally:
```bash
git clone https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill.git
mkdir -p ~/.autohand/skills
cp -R Xcode-Build-Optimization-Agent-Skill/skills/* ~/.autohand/skills/
```

Or install them only for the current project:
```bash
git clone https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill.git
mkdir -p .autohand/skills
cp -R Xcode-Build-Optimization-Agent-Skill/skills/* .autohand/skills/
```

Autohand Code discovers skills from `~/.autohand/skills/` and `.autohand/skills/`.

## Manual install

1) **Clone** this repository.
2) **Install or symlink** the skill folders from `skills/` following your tool's official skills installation docs (see links below). Install all six for the full orchestrated workflow.
3) **Use your AI tool** as usual and ask it to benchmark or optimize your Xcode builds.

> Note: the skill folders moved from the repository root to `skills/` when adopting the Agent Plugins format. Symlinks at the old paths keep existing local clones and scripts working; they will be removed in the next major version.

### Where to Save Skills

Follow your tool's official documentation, here are a few popular ones:
- **Codex:** [Where to save skills](https://developers.openai.com/codex/skills/#where-to-save-skills)
- **Claude:** [Using Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- **Cursor:** [Plugins documentation](https://cursor.com/docs/plugins) or [Enabling Skills](https://cursor.com/docs/context/skills#enabling-skills)
- **Gemini CLI:** [Agent Skills](https://geminicli.com/docs/cli/skills/)
- **Autohand Code:** `~/.autohand/skills/` or `.autohand/skills/`

## Trigger the skills

After installing through any of these options, use the skills in your AI agent, for example:
> Use the xcode build orchestrator skill to benchmark my build and propose optimizations
