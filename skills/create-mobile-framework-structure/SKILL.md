---
name: create-mobile-framework-structure
description: Adds a new app to the mobile test framework once - reads the build to find its identity and type, writes its settings, creates the empty layer folders and a flow document, and adds a fail-fast memory check at session start. Writes no locators, tests or credentials. Use once per app, before any feature work.
---

# Create Mobile Framework Structure

Sets up the shelves that the other skills fill. After this runs, the app has a
name, settings and empty folders, and nothing else.

## When to use

- Once, when an app is first brought into the framework.
- Never to add a feature: that starts at `get-mobile-context`.

## Rules

- **Stop if the app already exists.** Extend it instead.
- **No guessing from the build.** Reading the build gives the package name and
  app type only, never locators or behaviour.
- **No secrets, no tests.** Credentials belong to `get-mobile-auth`; tests to
  `mobile-test-automation`.

## Steps

1. **Check** the app isn't already registered.
2. **Get the build** (hand off to `mobile-build-fetch` if missing).
3. **Read its identity.**
   - Android: package and launch activity (`aapt dump badging`); detect the
     app type (native, Flutter, React Native, hybrid) from the libraries
     inside the package.
   - iOS: bundle id and executable from `Info.plist`.
4. **Write settings** to `.env` (and `.env.example` with empty values):
   app name, short name, type, package/activity or bundle id, build path,
   platform, Appium host and port, device name.
5. **Create the folders** for the Page Object Model (see `docs/framework-rules.md`):

```
src/core/                     # config.py (settings), driver.py (the Appium session)
src/pages/base_page.py        # BasePage: waits, tap, type, read, scroll, Back; locator helpers
src/pages/<screen>_page.py    # one page object per screen: locators + what a user does there
src/pages/components/         # parts shared by several screens (header, menu, dialogs)
src/utils/                    # helpers with no screen (e.g. reading prices)
tests/conftest.py             # session, fresh app per test, shared starting-point fixtures
tests/<feature>/test_<feature>.py
tests/<feature>/<feature>_td.py   # that feature's test data
docs/<app>-flow.md            # screens, locators and status (starts "Unconfirmed")
```

6. **Add a start-up guard** in `tests/conftest.py`: fail the session at once
   if available memory is below a configurable threshold.
7. **Hand off** to `mobile-env-check`, then `get-mobile-context`.
