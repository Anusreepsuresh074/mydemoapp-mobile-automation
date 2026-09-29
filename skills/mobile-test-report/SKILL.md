---
name: mobile-test-report
description: Builds the Allure HTML report from the latest run's results, then triages every failure from its attachments (screenshot, page source, device log) and routes it to the skill that owns the fix. Never re-runs tests and never "fixes" a failure with a wait. Use after a test run.
---

# Mobile Test Report

Makes a run readable, and makes sure no failure is left unexplained.

## When to use

- After `mobile-test-automation` or a CI run.
- Standalone, whenever someone asks for the report.

## Rules

- **Report, don't re-run.** This skill reads results; it never starts tests.
- **Every failure gets an owner** (table below).
- **No sleep-based fixes**, and no changes to the reporter set-up here.

## Steps

1. **Check** `allure-results/` exists and holds the latest run.
2. **Generate** the report: `allure generate allure-results -o allure-report --clean`,
   then `allure open allure-report` (or `allure serve allure-results`).
3. **Triage** each failure from its attachments: the step that failed, the
   screenshot, the page source, and the device log.
4. **Route** it:

| Symptom | Likely cause | Owner |
| --- | --- | --- |
| Element not found, wrong element | Locator or wait | `mobile-test-automation` |
| Signed out, wrong screen at start | Session or leftover state | `mobile-teardown`, `get-mobile-auth` |
| Timeouts everywhere, blank screenshots | Device or server health | `mobile-env-check` |
| Missing data | Data plan | `mobile-test-data` |
| A rule nobody tested | Coverage | `mobile-coverage-audit` |

5. **Record the lesson** as a Symptom / Cause / Fix note in the owning skill's
   pitfalls, so it isn't debugged twice.
6. **Hand off** to `mobile-teardown`.
