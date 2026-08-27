# Implementation patterns — React

> Seed rules. Replace or extend with your own preferences.
> Same format as general.md. Nothing eslint-plugin-react-hooks already enforces.

## no-fetch-in-effect
trigger: useEffect\s*\(\s*(async|\(\)\s*=>)\s*\{[^}]*fetch\s*\(
Data fetching inside a bare useEffect brings races, no caching, and no cancellation. Use the project's data layer (query hook, loader, server component) instead.

## derive-dont-sync
trigger: useEffect\s*\([^)]*set[A-Z]\w*\(
A useEffect whose only job is to set state from other state is a sync bug waiting to happen. Derive the value during render, or use useMemo.

## lift-state-late
trigger: useState\s*<[^>]*\[\]\s*>\s*\(\s*\[\s*\]\s*\)
Before adding list state here, check whether a parent or the data layer already owns this data. Duplicate copies drift apart.
