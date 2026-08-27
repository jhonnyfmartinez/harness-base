# Implementation patterns — general

> Seed rules. Replace or extend with your own preferences.
> Format per rule: `## <kebab-name>`, a `trigger:` regex tested against the
> edited file, then the nudge text (keep it to two lines: rule + why).
> These are judgment calls only — anything a linter, formatter, compiler, or
> test can catch does NOT belong here.

## prefer-composition
trigger: \bclass\s+\w+\s+extends\s+(?!React\.Component|Component|Error)
Prefer composition over inheritance. Extract the shared behavior into a function or injected dependency instead of a base class — it stays testable and swap-able.

## options-object
trigger: \b\w+\s*\([^)]*\b(bool|boolean)\b[^)]*,\s*[^)]*\b(bool|boolean)\b
A function taking multiple booleans is unreadable at the call site. Use a single options object with named fields.

## no-deep-relative-imports
trigger: from\s+['"](\.\./){3,}
Three or more `../` levels means the import path will break on the next move. Use the project's path alias instead.

## rethrow-with-context
trigger: catch\s*\((\w+)\)\s*\{\s*throw\s+\1\s*;?\s*\}
A bare rethrow adds nothing. Either let the error propagate or wrap it with context about what was being attempted.

## no-timeout-syncing
trigger: setTimeout\s*\(\s*[^,]+,\s*\d{1,4}\s*\)
A short setTimeout usually papers over a race. Find the event or promise to await instead of guessing a delay.
