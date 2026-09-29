---
name: review-automation-changes
description: Reviews a branch's changes against the framework rules in docs/framework-rules.md - layer boundaries, locator placement, waits, assertions, markers, secrets - and against traceability (every test maps to an approved case with live-confirmed locators), then lists findings as Blocker, Should fix or Nit. Use before opening or merging a pull request.
---

# Review Automation Changes

A second pair of eyes that knows the framework's rules.

## When to use

- Before a pull request is opened or merged.

## Checks

1. **Layers.** Each changed file sits in the right layer; imports only point
   downwards (tests → flows → actions → screens).
2. **Locators** live only in screen classes and follow the naming prefixes.
3. **Waits** are conditions, never sleeps.
4. **Assertions** live in tests (or flows that return a checked result),
   never in screens or actions.
5. **Markers and report labels** are present on every test.
6. **No secrets or hardcoded app names**; no bare `except:`.
7. **Traceability.** Every new test maps to an approved case ID; its locators
   were confirmed on a device; the flow document was updated.
8. **Run** the linter in check mode and the changed tests.

## Output

In chat: findings grouped as **Blocker** (must fix), **Should fix** and
**Nit**, each citing the rule it breaks. Coverage gaps are passed to
`mobile-coverage-audit`, not listed here.
