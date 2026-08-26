---
name: implement
description: Phase 3 — Execute the approved plan. Hard-stop on drift.
argument-hint: <feature-slug>
disable-model-invocation: true
model: sonnet
---

You are starting **Phase 3 (Implement)** of the delivery workflow.

Arguments: `$ARGUMENTS` (the feature-slug)

## Pre-flight

1. `.agents/work/<feature-slug>/plan.md` must exist and have been approved by me. If you have any doubt about approval, stop and ask.
2. Read `.agents/work/<feature-slug>/progress.md` to see where things stand — this session may be resuming someone else's work.
3. The working tree must be clean.
4. Verify you're on the correct feature branch. If not, create one named per the project's branch-naming convention (see `AGENTS.md`). Default: `feat/<feature-slug>`.
5. Re-read the plan in full and the user-level `~/.agents/AGENTS.md` discipline.

## The contract

The plan is binding. Execute the **commit sequence** in order. For each step:

1. Make **only** the changes that step describes. No drive-by edits, no opportunistic refactors.
2. Run the project's verify command (`AGENTS.md` → Commands), or type-check + lint + tests for the touched area if no single command is defined.
3. Commit with the **exact** conventional-commit message from the plan.
4. Append one line to `progress.md`: date, `implement`, which step just landed, next step.
5. Move to the next step.

## Drift gate (this is the whole point)

If at any point you find that the plan does not cover what you need to do — missing file, wrong signature, unanticipated failure, new dependency, changed data flow, anything **structural** — you MUST:

1. **Stop. Do not write a workaround.** Do not improvise.
2. Append an entry to `.agents/work/<feature-slug>/amendments.md`:

   ```markdown
   ## Amendment <N> — <ISO timestamp>

   **Plan step:** <step number / commit message>
   **What I hit:** <concrete details with file:line refs>
   **Why the plan doesn't cover it:** <one paragraph>
   **Proposed amendment:** <minimum change to the plan that would cover it; quote the section to change and the new text>
   ```

3. Surface the amendment to me. Wait for **explicit approval**.
4. Only after approval: update `plan.md` to reflect the amendment, note it in `progress.md`, then resume from where you stopped.

You may **not** batch amendments. One at a time, approved before the next.

Trivial corrections (renaming a local variable, fixing a typo in the plan, correcting an obviously wrong import path) do not require an amendment. Anything structural does. **When in doubt, stop and ask.**

## When all steps are done

- Run the project's verify command for the whole project. It must pass.
- Append a final line to `progress.md`: date, `implement`, done, next step `/review`.
- Tell me:
  - Branch name
  - The commits made (list of subject lines)
  - Any amendments applied (count + one-line summaries)
  - "Ready for `/review`."
- Do **not** run `/review` automatically.
