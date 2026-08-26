---
name: address-pr
description: Phase 5 — Triage and address PR comments with explicit approval.
argument-hint: <pr-number>
disable-model-invocation: true
model: sonnet
---

You are starting **Phase 5 (Address PR Comments)** of the delivery workflow.

Arguments: `$ARGUMENTS` (the PR number)

## Pre-flight

1. `gh` CLI must be installed and authenticated. If `gh auth status` fails, stop and tell me.
2. You are on the feature branch for this PR. Verify with `gh pr view $ARGUMENTS --json headRefName -q .headRefName` matches your current branch.
3. The working tree is clean.

## Fetch comments

Pull all open review comments and inline thread comments:

```bash
gh pr view "$ARGUMENTS" --json reviews,comments,title,body,state > .agents/work/pr-$ARGUMENTS-meta.json
gh api "repos/{owner}/{repo}/pulls/$ARGUMENTS/comments" > .agents/work/pr-$ARGUMENTS-inline.json
```

(Adjust `{owner}/{repo}` if `gh` doesn't auto-resolve them.)

## Triage (no code changes yet)

Spawn the **`pr-comment-triager`** subagent with:

- The two JSON files above
- The diff for this PR
- The project `AGENTS.md`

Ask it to classify each comment:

- **must-fix** — clear bug, missed requirement, security issue, production-bar violation, or convention violation backed by the project `AGENTS.md`
- **push-back** — reviewer is mistaken or missing context; the triager drafts a polite, factual response that explains the trade-off or points to relevant code/docs
- **nice-to-have** — valid suggestion, can be deferred

## Present the triage to me

Show a table:

| ID | Author | One-line summary | Class | Recommended action | Draft response (if push-back) |
|----|--------|------------------|-------|---------------------|-------------------------------|

Ask me which items to action. **Do NOT touch code, post any comment, or push anything yet.**

## Action approved items

For approved **must-fix** items:

- Treat each as a mini Plan → Implement → Review cycle. For trivial fixes (typos, single-line corrections), inline. For anything structural, write a brief amendment to `.agents/work/<feature-slug>/amendments.md` and propose it before coding.
- Group related comments into one commit when sensible.
- Use conventional-commit messages: `fix(<scope>): ...`, `refactor(<scope>): ...`, `docs(<scope>): ...`.

For approved **push-back** items:

- Show me each draft response, written in the project's writing style (`AGENTS.md` → Writing style). Edit per my feedback.
- Post only after I explicitly approve. Use:

  ```bash
  gh api -X POST "repos/{owner}/{repo}/pulls/$ARGUMENTS/comments/<comment-id>/replies" -f body="<text>"
  ```

For **nice-to-have** items:

- Append to `.agents/work/<feature-slug>/followups.md` with the comment URL and a short description.
- Do not action now.

## After all approved actions

- Re-run the project's verify command (`AGENTS.md` → Commands).
- Push the new commits.
- Append one line to `.agents/work/<feature-slug>/progress.md`: date, `address-pr`, what was actioned, next step.
- Summarize for me: what was fixed, what was pushed back on (with the response posted), what was deferred to follow-ups.
- If any of the must-fix changes triggered an amendment, mention that explicitly.

Do **not** mark the PR as resolved or merge it. That stays my decision.
