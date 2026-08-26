---
name: plan
description: Phase 2 — Convert the research brief into a binding implementation plan.
argument-hint: <feature-slug>
disable-model-invocation: true
model: opus
---

You are starting **Phase 2 (Plan)** of the delivery workflow.

Arguments: `$ARGUMENTS` (the feature-slug from `/research`)

## Pre-flight

1. `.agents/work/<feature-slug>/research.md` must exist. If not, **stop** and ask me to run `/research` first.
2. Read the project `AGENTS.md` and the user-level `~/.agents/AGENTS.md`. The production bar is non-negotiable.
3. Read the research brief in full.

## Draft the plan

Produce `.agents/work/<feature-slug>/plan.md`, in the project's writing style (`AGENTS.md` → Writing style), with **all** of these sections. A plan that is missing any of them is not ready.

- **Goal** — one sentence, testable.
- **Non-goals / Out of scope** — explicit list of what we are deliberately not doing. Be generous here. This section stops scope creep; treat it as load-bearing.
- **Files to create or modify** — explicit list. One line per file describing its purpose and what changes.
- **Function / component signatures** — written out with full TypeScript types. No `any`. Include exported types, interfaces, and component prop shapes.
- **Data flow** — Mermaid `flowchart` or `sequenceDiagram` if anything new crosses a module boundary, hits an external service, or changes how state moves through the app.
- **Test cases** — name + one-line description each. Cover happy path, at least one error path, and any edge case from the research brief. Note which file each test will live in.
- **Commit sequence** — ordered list of conventional-commit messages. Each commit must map to one logical step and leave the repo in a working state (the project's verify command passes).
- **Smoke test recipe** — exact steps I will run to manually verify. Be precise: which URL, which inputs, what to look for.
- **Production bar checklist** — copy the list from `~/.agents/AGENTS.md` so the reviewer phase has a per-feature checklist to grade against.

## Validate

1. Spawn the **`plan-validator`** subagent with the draft plan. It will check the plan against the actual codebase and flag:
   - Signatures that conflict with existing code
   - Missing dependencies
   - Test gaps
   - Steps that would violate the production bar
   - Commits that wouldn't leave the repo in a working state
2. Incorporate validator feedback. If the validator surfaces something that requires a research question, **stop** and ask me — don't guess.
3. Save the final plan to `.agents/work/<feature-slug>/plan.md`.
4. Create an empty `.agents/work/<feature-slug>/amendments.md` with this header:

   ```markdown
   # Amendments to plan.md

   Append-only log of drift amendments approved during /implement.
   Each entry: timestamp, plan step, what was hit, the approved change.
   ```

5. Append one line to `.agents/work/<feature-slug>/progress.md`: date, `plan`, one-line status, next step (`/implement` after approval).

## Hard stop

After saving the plan:

- Surface a **plan summary** (Goal + commit sequence in 5 lines or fewer)
- Surface the validator's findings, separated into BLOCKING / WARNING / NIT
- Ask me explicitly: "Approve this plan?" Wait for explicit approval before `/implement`
