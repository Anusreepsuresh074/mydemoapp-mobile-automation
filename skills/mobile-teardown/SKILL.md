---
name: mobile-teardown
description: Resets the device, the Appium session and the app to a known state for the next run, in a way that matches the recorded sign-in strategy (clearing data where sign-in is cheap, keeping it where a signed-in session is reused). Touches only local device state, never code or documents. Use after a run, or before one that must start clean.
---

# Mobile Teardown

The next run should start from the same place every time.

## When to use

- After a test run or a failed debugging session.
- Before a run that must start from a fresh install.

## Rules

- **Follow the sign-in strategy.** If tests reuse a signed-in session, never
  wipe it; if sign-in is cheap, reset fully.
- **Unknown strategy means stop.** Don't guess and wipe.
- **Local state only.** Never edit code, test data files or documents.

## Steps

1. **Read** the sign-in strategy (`get-mobile-auth`) and the `noReset` setting.
2. **End sessions.** Make sure the last Appium session was closed, and no
   second session is holding the device.
3. **Reset the app**, by strategy:
   - cheap sign-in: `adb shell pm clear <package>` (or reinstall);
   - reused session: keep the data, close any dialogs, return to the home screen.
4. **Close** anything left half-open (keyboards, sheets, other apps).
5. **Confirm** the device responds (a quick `mobile-env-check` round trip).
6. **Report** what was reset and what was kept on purpose.

## Pitfalls

| Symptom | Cause | Fix |
| --- | --- | --- |
| New session fails with "instrumentation process cannot be initialized", and the Appium log shows `ECONNREFUSED 127.0.0.1:8200` while the helper's own log says its server started | A previous session was aborted and left a stale port forward and a half-running UiAutomator2 helper | `adb -s <device> forward --remove-all`, then force-stop `io.appium.uiautomator2.server` and `io.appium.uiautomator2.server.test`, then start a new session |
| The run script hangs at the end, or the next run finds port 4723 in use, because the Appium server is still running | The script started Appium through `npx` and its exit trap stopped only `npx`, not the server it launched | Start `node_modules/.bin/appium` directly, so `$!` is the server; in the trap, `kill` it and then `wait` for it |
