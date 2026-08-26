# harness-base

Agent-agnostic setup for AI coding tools. One set of markdown files that any agent tool (Claude Code, Codex, Cursor, …) can share: user-level rules, a five-phase delivery workflow, and templates for new projects.

## What's inside

- **`AGENTS.md`** — user-level rules: writing style, workflow discipline, production bar.
- **`skills/`** — the five workflow phases (`/research`, `/plan`, `/implement`, `/review`, `/address-pr`) plus `/sync` for closing out work.
- **`agents/`** — subagent definitions (currently the cold-context `code-reviewer`).
- **`templates/AGENTS.md`** — fill-in-the-blanks project file. Copy to a project root.
- **`templates/PROJECT_CLAUDE.md`** — optional Claude-only project notes.
- **`templates/project-agents/`** — skeleton for a project's `.agents/` folder (README + PR/ticket templates).
- **`pointers/CLAUDE.md`** — two-line file that makes Claude Code read `AGENTS.md`.

## Where each file goes

This repo mirrors `~/.agents/` one to one.

| Repo path | Destination | How |
|---|---|---|
| `AGENTS.md` | `~/.agents/AGENTS.md` | copy |
| `skills/` | `~/.agents/skills/` | copy |
| `agents/` | `~/.agents/agents/` | copy |
| `templates/` | `~/.agents/templates/` | copy |
| `pointers/CLAUDE.md` | `~/.claude/CLAUDE.md` | copy |
| `skills/<name>/` | `~/.claude/skills/<name>` | symlink |
| `agents/code-reviewer.md` | `~/.claude/agents/code-reviewer.md` | symlink |
| `templates/AGENTS.md` | `<project>/AGENTS.md` | copy per project, fill in |
| `templates/project-agents/` | `<project>/.agents/` | copy per project |

## Install

Clone and copy the mirror:

```bash
git clone https://github.com/<you>/harness-base.git
mkdir -p ~/.agents
cp -R harness-base/AGENTS.md harness-base/skills harness-base/agents harness-base/templates ~/.agents/
```

Point Claude Code at it:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp harness-base/pointers/CLAUDE.md ~/.claude/CLAUDE.md
for s in research plan implement review address-pr sync; do
  ln -sfn ../../.agents/skills/$s ~/.claude/skills/$s
done
ln -sfn ../../.agents/agents/code-reviewer.md ~/.claude/agents/code-reviewer.md
```

Other tools: point them at `~/.agents/AGENTS.md` the way that tool loads global rules, and link `~/.agents/skills/` into its skills folder if it has one.

## Set up a new project

```bash
cp ~/.agents/templates/AGENTS.md <project>/AGENTS.md   # fill in the placeholders
cp -R ~/.agents/templates/project-agents <project>/.agents
echo ".agents/work/" >> <project>/.gitignore
```

## How the workflow runs

1. `/research <slug> "<description>"` — maps the codebase, writes `research.md`.
2. `/plan <slug>` — turns research into a binding plan with goals, non-goals, and tests.
3. `/implement <slug>` — executes the plan commit by commit. Any surprise stops the work and needs an approved amendment.
4. `/review <slug>` — a fresh-context reviewer reads the diff cold, then a manual smoke test gates the PR.
5. `/address-pr <number>` — triages PR comments into must-fix, push-back, and deferred.

Each phase writes its state to `.agents/work/<slug>/` in the project, including a `progress.md` any tool can resume from.
