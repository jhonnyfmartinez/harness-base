---
name: research
description: Phase 1 — Research a feature. Maps codebase, surveys external deps, produces a research brief. Does not plan or write code.
argument-hint: <feature-slug> "<one-line description>"
disable-model-invocation: true
model: opus
---

You are starting **Phase 1 (Research)** of the delivery workflow.

Arguments: `$ARGUMENTS`

The first token is the feature-slug (kebab-case). The rest is a one-line description of the feature.

## Pre-flight

1. Read the project's `AGENTS.md` at the repository root. If it does not exist, offer to scaffold one from `~/.agents/templates/AGENTS.md` and **stop**. Do not continue research until the project file exists.
2. Verify the working tree is clean. If it isn't, stop and surface what's uncommitted before continuing.
3. Create `.agents/work/<feature-slug>/` if it doesn't exist. Ensure `.agents/work/` is in `.gitignore`.

## Research

1. Spawn the **`codebase-explorer`** subagent. Brief it with the feature description. Ask for:
   - Relevant files (with `path:line` citations)
   - Existing patterns I should match
   - Modules likely to be touched
   - Tests already covering nearby behavior
   - Landmines, gotchas, conventions that aren't obvious from the code
2. If the feature involves external libraries, frameworks, or APIs **not already in this repo**, spawn the **`external-researcher`** subagent in parallel. Brief it with: which dependency, what the feature needs from it, and the project's existing dependency context.
3. Synthesize findings into `.agents/work/<feature-slug>/research.md`, written in the project's writing style (`AGENTS.md` → Writing style), with these sections:
   - **Feature description** — one paragraph, in your own words, demonstrating you understood it
   - **Relevant files** — paths with one-line purpose each, cited as `path:line`
   - **Existing patterns to follow** — short snippets (≤ 5 lines) with citations
   - **External dependencies** — current vs. proposed, with version notes
   - **Risks and unknowns** — concrete, not generic
   - **Open questions for me** — things you can't resolve without my input
4. Create `.agents/work/<feature-slug>/progress.md` with its first line: date, `research`, one-line status, next step (`/plan` after review).

## Hard stop

After writing `research.md`:

- Do **not** start drafting a plan
- Do **not** write or modify any source code
- Tell me where the brief is, summarize the top 3 risks/unknowns in one line each, and ask me to review before invoking `/plan`
