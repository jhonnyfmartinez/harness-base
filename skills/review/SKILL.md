---
name: review
description: Phase 4 — Independent review against the production bar, ending with a smoke-test gate.
argument-hint: <feature-slug>
disable-model-invocation: true
model: sonnet
---

You are starting **Phase 4 (Self-Review)** of the delivery workflow.

Arguments: `$ARGUMENTS` (the feature-slug)

## Pre-flight

1. `.agents/work/<feature-slug>/plan.md` exists.
2. The feature branch is checked out and all implementation commits are in.
3. The working tree is clean.

## Capture the diff

Generate the diff against the base branch (default `origin/main`, but check the project `AGENTS.md` for overrides):

```bash
git fetch origin
git diff $(git merge-base HEAD origin/main)..HEAD > .agents/work/<feature-slug>/diff.patch
```

## Independent review (the whole point of this phase)

Spawn the **`code-reviewer`** subagent with **fresh context**. Pass it:

- The plan (`.agents/work/<feature-slug>/plan.md`)
- The amendments log (`.agents/work/<feature-slug>/amendments.md`)
- The diff (`.agents/work/<feature-slug>/diff.patch`)
- The project `AGENTS.md`
- The user-level `~/.agents/AGENTS.md` production bar

**Do NOT pass it the implementation conversation, your reasoning, or any defense of the choices made.** The reviewer reads the diff cold. That's the whole point.

## Run the automated bar in parallel

While the reviewer works, run the project's verify command (`AGENTS.md` → Commands) first, then anything it doesn't cover:

- `tsc --noEmit` (or the project's type-check command)
- `eslint` on touched files (or the project's lint command)
- The full test suite (or scoped to touched areas if the project `AGENTS.md` says so)
- `git grep -nE ': any\b|as any\b' -- $(git diff --name-only $(git merge-base HEAD origin/main)..HEAD)` — must be empty
- Conventional Commits lint on the new commits (use commitlint if installed, otherwise pattern-match)
- For UI changes: the project's accessibility check (axe-core for React/Vue, Angular's a11y rules, etc.)

## Docs and diagrams

- Was the README touched? If the feature changes API or behavior and README wasn't updated, that's a FAIL.
- Did the feature change module boundaries, data flow, or external integrations? If yes, an architectural diagram (Mermaid) must be present and current. If missing or stale, spawn the **`doc-diagrammer`** subagent to produce or update one.

## Compile the review

Write `.agents/work/<feature-slug>/review.md` as a checklist, in the project's writing style (`AGENTS.md` → Writing style). Each item: PASS / FAIL / NEEDS ATTENTION + specific `file:line` references.

Sections:

1. **Plan adherence** — does the diff implement the plan? Surface any deviation not authorized by `amendments.md`.
2. **Production bar** — each item from the user-level `~/.agents/AGENTS.md` list, graded.
3. **Reviewer findings** — verbatim from the `code-reviewer` subagent.
4. **Docs & diagrams** — touched, current, accurate.
5. **Tests** — coverage of plan's test cases, plus reviewer's view on test quality.

Then append one line to `progress.md`: date, `review`, verdict, next step.

## Smoke test gate (the final gate before PR)

After all of the above:

- Surface the smoke-test recipe from the plan, verbatim
- Ask me explicitly: **"Please run the smoke test and reply `approved` or describe what failed."**
- Wait.

If I reply approved AND every other item is PASS:

- Tell me the feature is ready to push and open a PR. When writing the PR description, copy `.agents/templates/pr-description.md`.
- Do **not** push or open a PR yourself unless I explicitly ask

If anything fails:

- **Cosmetic / local** issues (typo, missing test, missing JSDoc): describe and offer to fix with my approval. After fixing, re-run `/review`.
- **Structural** issues (wrong abstraction, missing requirement, plan didn't cover something): recommend dropping back to `/plan` with an amendment. Do not patch around structural issues here.

Never declare the feature done without my smoke-test approval.
