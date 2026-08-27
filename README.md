# harness-base

Agent-agnostic setup for AI coding tools. One set of markdown files that any agent tool (Claude Code, Codex, Cursor, …) can share: user-level rules, a five-phase delivery workflow, and templates for new projects.

## What's inside

- **`AGENTS.md`** — user-level rules: writing style, workflow discipline, production bar.
- **`skills/`** — the five workflow phases (`/research`, `/plan`, `/implement`, `/review`, `/address-pr`) plus `/sync` for closing out work.
- **`agents/`** — the six subagents the phases spawn: `codebase-explorer` and `external-researcher` (research), `plan-validator` (plan), `code-reviewer` and `doc-diagrammer` (review), `pr-comment-triager` (address-pr).
- **`templates/AGENTS.md`** — fill-in-the-blanks project file. Copy to a project root.
- **`templates/PROJECT_CLAUDE.md`** — optional Claude-only project notes.
- **`templates/project-agents/`** — skeleton for a project's `.agents/` folder (README + PR/ticket templates).
- **`patterns/`** — implementation preferences that steer the agent after every code edit. Plain markdown, readable by any tool.
- **`hooks/`** — the Claude Code adapter that delivers those patterns.
- **`pointers/CLAUDE.md`** — two-line file that makes Claude Code read `AGENTS.md`.

## Where each file goes

This repo mirrors `~/.agents/` one to one.

| Repo path | Destination | How |
|---|---|---|
| `AGENTS.md` | `~/.agents/AGENTS.md` | copy |
| `skills/` | `~/.agents/skills/` | copy |
| `agents/` | `~/.agents/agents/` | copy |
| `templates/` | `~/.agents/templates/` | copy |
| `patterns/` | `~/.agents/patterns/` | copy |
| `hooks/` | `~/.agents/hooks/` | copy |
| `pointers/CLAUDE.md` | `~/.claude/CLAUDE.md` | copy |
| `skills/<name>/` | `~/.claude/skills/<name>` | symlink |
| `agents/<name>.md` | `~/.claude/agents/<name>.md` | symlink |
| `templates/AGENTS.md` | `<project>/AGENTS.md` | copy per project, fill in |
| `templates/project-agents/` | `<project>/.agents/` | copy per project |

## Install

Clone and copy the mirror:

```bash
git clone https://github.com/jhonnyfmartinez/harness-base.git
mkdir -p ~/.agents
cp -R harness-base/AGENTS.md harness-base/skills harness-base/agents \
      harness-base/templates harness-base/patterns harness-base/hooks ~/.agents/
chmod +x ~/.agents/hooks/implementation-patterns.py
```

Point Claude Code at it:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp harness-base/pointers/CLAUDE.md ~/.claude/CLAUDE.md
for s in research plan implement review address-pr sync; do
  ln -sfn ../../.agents/skills/$s ~/.claude/skills/$s
done
for a in ~/.agents/agents/*.md; do
  ln -sfn "../../.agents/agents/$(basename "$a")" ~/.claude/agents/"$(basename "$a")"
done
```

Turn on the pattern nudges by adding this to `~/.claude/settings.json` (merge with any hooks already there):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$HOME/.agents/hooks/implementation-patterns.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
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

## How the pattern nudges work

Rules live in `patterns/` as plain markdown, split by language. Each rule is a name, a regex that decides when it applies, and two lines of advice:

```markdown
## prefer-composition
trigger: \bclass\s+\w+\s+extends\s+
Prefer composition over inheritance. Extract the shared behavior into a function
or injected dependency instead of a base class — it stays testable and swap-able.
```

After the agent edits a code file, the hook checks that file against the rules for its extension and feeds back only the ones that matched. Rules are judgment calls, never things a linter, formatter, compiler, or test already catches.

Three limits keep it from becoming noise:

- Silent when nothing matches.
- At most two nudges per edit.
- Each rule fires once per session.

The hook always exits 0, so it steers the agent without ever blocking or failing a turn. Edit the markdown to change your preferences — no code changes needed.
