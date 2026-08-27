# Implementation patterns — TypeScript

> Seed rules. Replace or extend with your own preferences.
> Same format as general.md. Nothing here that tsc or eslint already enforces.

## narrow-unknown-at-boundary
trigger: JSON\.parse\s*\(|\bas\s+[A-Z]\w+\b
Data crossing a boundary (JSON, network, storage) is `unknown` until validated. Narrow it with a type guard or schema, not a cast.

## discriminated-union-over-flags
trigger: \bstatus\s*:\s*string\b|\btype\s*:\s*string\b
A stringly-typed status invites impossible states. Model it as a union of literal types (or a discriminated union) so the compiler tracks the cases.

## export-types-next-to-values
trigger: ^export\s+(interface|type)\s+\w+Props\b
Keep a component's Props type exported next to the component and named `<Component>Props` — consumers and tests import it, so don't inline or hide it.
