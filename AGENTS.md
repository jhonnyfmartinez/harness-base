# Global preferences

> Lives at `~/.agents/AGENTS.md` (user level). This file stays thin: agent-agnostic
> rules live in each project's `AGENTS.md`, which any agent tool reads.

- Keep explanations short and concise
- Use conventional commit format
- Prefer composition over inheritance
- **Writing style:** all output follows the "Writing style" section of the project's `AGENTS.md`. That means every artifact too: markdown files, PR descriptions, tickets, issues, commit bodies.

## Workflow Discipline

I work in a five-phase pipeline: `/research` → `/plan` → `/implement` → `/review` → `/address-pr`.

Phases are invoked **explicitly by me**. Never chain them automatically. Never skip a phase. If I ask for code without having run the prior phases, remind me which phase I'm skipping and ask for explicit confirmation before proceeding.

### The Plan Is a Contract

During `/implement`, the plan in `.agents/work/<feature-slug>/plan.md` is binding.

If you encounter anything the plan did not anticipate — a missing edge case, a function signature that doesn't fit, a failing test for an unforeseen reason, a new file required, a new dependency, a changed data flow — you MUST:

1. **Stop immediately.** Do not improvise a workaround.
2. Append a proposed amendment to `.agents/work/<feature-slug>/amendments.md`. The amendment must include:
   - The plan step you were on
   - What you hit (concrete details, file:line references)
   - Why the existing plan does not cover it
   - The smallest possible change to the plan that would cover it
3. Surface the amendment to me and **wait for explicit approval** before touching code further.
4. Only after approval: update `plan.md` to reflect the amendment, then resume from where you stopped.

You may NOT batch amendments. One at a time, approved before the next.

Renaming a local variable, fixing a typo in the plan, or correcting an obviously wrong import path does not require an amendment. **Anything structural does.**

### Production Bar (non-negotiable for any feature to be "done")

- The project's **verify command** (see `AGENTS.md` → Commands) passes. If none is defined, run type-check + lint + tests individually.
- `tsc` clean
- `eslint` clean
- No `any` types in new or touched code (use `unknown` + narrowing)
- No new `// @ts-ignore` or `// @ts-expect-error` without an issue link
- Conventional Commits format on every commit
- README and relevant docs updated
- Architectural diagram (Mermaid) added or updated when a feature changes module boundaries, data flow, or external integrations
- Accessibility checks pass for any UI change (axe / framework equivalent)
- Manual smoke test approved by me before opening a PR

### Project Conventions

Every project I work in has an `AGENTS.md` at its root with the project facts (stack, commands, verify command, writing style, boundaries) and may have a thin tool-specific notes file (scaffolded from `~/.agents/templates/PROJECT_CLAUDE.md` for Claude Code). **Read `AGENTS.md` at the start of every session.**

If a project's `AGENTS.md` is missing, offer to scaffold one from `~/.agents/templates/AGENTS.md` and stop until I've filled it in.

If a project file says something that contradicts this file (for example, a different commit-message convention), the project file wins for that project.

### Workflow State

Per-feature working state lives in `<project-root>/.agents/work/<feature-slug>/`:

- `research.md` — output of `/research`
- `plan.md` — output of `/plan` (the contract)
- `amendments.md` — append-only log of approved drift amendments
- `progress.md` — one line per update: date, phase, where things stand, next step. Update it at the end of every phase and after every amendment. A fresh session resumes from this file.
- `review.md` — output of `/review`
- `diff.patch` — diff snapshot used by the reviewer
- `followups.md` — deferred PR comments and nice-to-haves

Add `.agents/work/` to the project's `.gitignore` if not already present. The rest of `.agents/` (README, templates) is committed.

### Style

- Be concise. No filler, no recap unless I ask for one.
- Cite files as `path:line` so I can jump to them.
- When unsure, ask **one** focused question rather than guessing.
- Prefer small, atomic commits over large omnibus ones.
- Do not announce what you're about to do; do it, then summarize.
