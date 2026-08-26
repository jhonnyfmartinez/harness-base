# <Project name>

> Copy this file to the repository root as `AGENTS.md` and fill in every
> placeholder. Delete instruction blockquotes like this one when done.
> Keep this file under 150 lines. Push detail into linked files, not here.

<One paragraph: what this project is, main language and framework with versions.>

## Commands

- **Install:** `<command>`
- **Verify (run this before claiming anything works):** `<one command that runs type-check + lint + tests, e.g. npm run check>`
- **Test a single file:** `<command>`
- **Dev server:** `<command>`
- **Build:** `<command>`

If `verify` fails, the work is not done. Fix it or report the failure. Never report success without running it.

## Writing style

Every word you produce follows these rules: chat replies, markdown files, PR descriptions, tickets, issues, commit bodies, docs.

- Plain English. Write so an 8-year-old could follow the sentence.
- Short sentences. Short answers. One idea per sentence.
- No filler, no hedging, no caveats, no recap. Answer, then stop.
- Use the simple word: "use" not "utilize", "start" not "initialize" — unless the technical term is the precise one.
- Technical terms, file paths, and code names are fine when no simpler correct word exists.
- For PR descriptions and tickets, copy the matching template in `.agents/templates/`.

## Workflow

Work moves through five phases, each started by the user, never chained automatically:

`/research` → `/plan` → `/implement` → `/review` → `/address-pr`

The plan is a contract. If reality does not match the plan, stop and propose an amendment. Do not improvise.

## Workflow state

Per-feature state lives in `.agents/work/<feature-slug>/` (gitignored — add `.agents/work/` to `.gitignore`):

- `research.md` — what the codebase looks like, risks, open questions
- `plan.md` — the binding plan (includes goal, non-goals, steps, tests)
- `amendments.md` — append-only log of approved plan changes
- `progress.md` — one line per update: date, phase, where things stand, next step. Any agent resuming this feature reads this first.
- `review.md` — review checklist result
- `diff.patch` — diff snapshot for the reviewer
- `followups.md` — deferred PR comments and nice-to-haves

`.agents/templates/` and `.agents/README.md` are committed. Only `.agents/work/` is ignored.

## Boundaries

- Never read, log, or commit: `.env*`, `<other secret paths>`
- Never edit: `<generated folders, lockfiles unless asked, vendored code>`
- Never run: `<destructive commands, e.g. anything against production>`
- Secrets come from `<where>`. Never hardcode them.

## Conventions

- **Commits:** Conventional Commits. Scopes: `<list>`
- **Branches:** `<pattern, e.g. feat/<slug>>`
- **Tests live in:** `<location>`
