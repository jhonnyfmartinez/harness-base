# .agents/

Working folder for AI agents. Any agent tool (Claude Code, Codex, Cursor, …) uses the same layout.

## Layout

- `work/<feature-slug>/` — per-feature state (research, plan, amendments, progress, review, diff, followups). **Gitignored.**
- `work/backlog.md` — the project backlog, if this project keeps one here.
- `templates/` — copy-paste templates for PR descriptions and tickets. **Committed.**

## Setup

Add this line to the project's `.gitignore`:

```
.agents/work/
```

Everything else in `.agents/` is committed.
