---
name: sync
description: Close out a just-finished piece of work and surface what's next.
argument-hint: [feature-slug or description, optional]
disable-model-invocation: true
---

You are closing out a piece of work that was just merged or finished, and telling me what's next.

Arguments: `$ARGUMENTS` (optional — a slug or short description of what just finished; if omitted, infer it from the recent conversation: the branch just merged, the PR just closed, the feature just discussed as done)

## 1. Identify the finished item

If `$ARGUMENTS` is given, use it. Otherwise look at what we were just doing in this conversation — the branch name, PR title, commit messages — to name the item. If it's genuinely ambiguous (e.g., we finished two unrelated things and you can't tell which I mean), ask me one focused question rather than guessing.

## 2. Find the backlog

Find the repo root with `git rev-parse --show-toplevel`, then look for `.agents/work/backlog.md` there.

- **Not found**: say so plainly and stop — don't invent a backlog structure or write one. Skip straight to telling me there's nothing to report next (or, if you can tell from context what I'd logically work on next, say that instead — but be clear it's a guess, not a backlog read).
- **Found**: continue.

## 3. Update the backlog

Read the file's actual structure before editing — don't assume section names or table columns match a previous run. In practice this repo uses a `## ✅ Completed` table followed by numbered priority sections, but treat that as this file's convention, not a hardcoded template.

Find the finished item's entry in whichever open section currently holds it (match by slug or by content — the item may not be named exactly what `$ARGUMENTS` says). Then:

- Move it into the Completed table with today's date.
- Write the summary in the same voice as the existing completed rows: concrete mechanisms and file-level specifics, not a restatement of the original ticket. Pull the real details from what we actually did in this conversation — implementation choices, what changed from the original scope, bugs the review caught, deviations, follow-up fixes. A completed-row summary that just repeats the open item's description is a sign you didn't look at what actually happened.
- Remove the entry from its old section entirely — don't leave a stub behind.

Check whether the backlog file is tracked by git (`git ls-files <path>` — empty output means untracked). If it's gitignored/untracked, there's nothing to commit, don't mention it. If it IS tracked, the edit leaves uncommitted changes — mention that in passing, but do not commit or push it yourself unless I explicitly ask.

## 4. Report what's next

Starting from the top of the highest-priority section that still has open items (skip any section that's now empty because everything in it shipped), surface the first item: its slug and a one-line summary of what it needs. Keep this short — a couple of lines, not the full backlog entry. If nothing is left anywhere, say so.

## Output

Keep the whole response tight: confirm what moved to Completed (one line), then what's next (one line, maybe two). No preamble, no restating what I already know from the conversation.
