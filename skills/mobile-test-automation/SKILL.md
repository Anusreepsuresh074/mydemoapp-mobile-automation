---
name: mobile-test-automation
description: Confirms every locator on the running app (never from source code or designs), then builds each approved test case with the Page Object Model (page objects, shared components, fixtures, tests) with Appium and pytest, runs it, and updates the flow document's status. Also the skill for fixing a flaky or broken test. Use after mobile-test-design is approved.
---

# Mobile Test Automation

Builds and runs the approved cases.

## When to use

- After `mobile-test-design` has an approved list.
- To repair a failing or flaky test.

## Rules

- **Locators come from the live app.** Dump the screen (Appium page source or
  `uiautomator dump`) and confirm each locator; source code and designs only
  give hints.
- **No new case without a walkthrough** of its screens on a device.
- **Prerequisites first.** Sign-in must pass before any signed-in test is built.
- **No sleeps.** Wait for a condition (element visible, text present), never
  for a fixed time.

## Locator priority

1. Accessibility id (content-desc on Android, accessibilityIdentifier on iOS)
2. Android resource-id / UiAutomator selector
3. iOS predicate string or class chain
4. Visible text
5. XPath, only with a written reason

By app type: native apps usually expose resource-ids; React Native exposes
`testID` as the accessibility id; Flutter needs semantics labels.

## Naming

Locator fields start with a type prefix: `btn_`, `input_`, `txt_`, `msg_`,
`chk_`, `lnk_`, `icn_`, `tab_`, `card_` (for example `btn_add_to_cart`).

## Steps

1. Run `mobile-env-check`; install the build on the device.
2. Read the approved case.
3. Walk the journey on the device, dumping each screen; record the screens,
   their texts and the chosen locators in the flow document.
4. Implement, in order: the **page object** for each screen (locators as
   class attributes, plus methods for what a user does and reads there;
   a method that lands on another screen returns that page) → shared
   **components** (header, menu, dialogs) → **fixtures** for common
   starting points → the **test** and its `<feature>_td.py` data.
5. Lint, then run the tests by marker (`pytest -m smoke`).
6. Fix the usual problems: stale elements (find again), the keyboard covering
   a button (hide it), loading spinners (wait for them to go), webviews
   (switch context).
7. When green, mark the case Done in the flow document with its test path.
8. Hand off to `mobile-test-report`, then `mobile-teardown`.
