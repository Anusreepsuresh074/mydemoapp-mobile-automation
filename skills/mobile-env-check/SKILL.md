---
name: mobile-env-check
description: Decides whether the machine, the device (emulator, simulator or phone) and the Appium server are healthy enough to give a trustworthy test result right now, and prints a Healthy / Degraded / Broken verdict per check with the next action to take. Writes nothing. Use before a first run, after an unexplained failure, or whenever a device "feels slow".
---

# Mobile Env Check

A failing mobile test can mean a broken app, a broken test, or a broken
environment. This skill rules out the third before anyone debugs the first two.

## When to use

- Before the first run on a new machine or device.
- When a test fails in a way the report can't explain (timeouts everywhere,
  blank screenshots, "session not created").
- As the first step of every CI job (see `mobile-ci-integration`).

## Rules

- **Online is not the same as responsive.** A device listed by `adb devices`
  can still be frozen; prove it with a round trip (step 4).
- **Report, don't patch.** Never add retries or waits to make a check pass,
  and never downgrade a Broken result to a warning.
- **One cause per finding.** Memory pressure, CPU load and version clashes are
  reported separately, because each has a different fix.
- **Say what is unproven.** If a check can't run on this platform, say so
  instead of reporting it as passed.

## Checks

1. **Host resources.** Available memory (not swap usage) against a threshold
   from `.env`; CPU load against the number of cores.
2. **Appium server.** Call its status endpoint; list the installed drivers
   (UiAutomator2 for Android, XCUITest for iOS); read start-up warnings about
   version mismatches.
3. **Tool versions.** Python, Node.js, the Appium client and the test plugins
   (pytest, allure-pytest) are a supported combination.
4. **Device round trip (Android).** Press Home with `adb shell input keyevent`,
   read the focused window, dump the UI tree, and take a screenshot to spot a
   system "not responding" dialog.
5. **Device round trip (iOS).** `xcrun simctl list` shows the simulator
   booted; a simulator screenshot succeeds.
6. **Clean boot, if in doubt.** Cold-boot the emulator without its snapshot:
   if the problem disappears, it was the emulator, not the app.
7. **Platform prerequisites.** Android SDK path set; iOS needs macOS with
   Xcode command-line tools.

## Output

A table in chat: check, verdict (Healthy / Degraded / Broken), evidence, next
action. Nothing is written to disk.

## Connects to

Runs first, and any time. `mobile-test-report` sends environment failures
here. `mobile-teardown` is different: it resets state, this checks health.

## Pitfalls

| Symptom | Cause | Fix |
| --- | --- | --- |
| `adb: device offline` in the first minute after a cold boot, though `sys.boot_completed` is 1 | The emulator restarts its adb connection once while applying post-boot settings | Re-run the device round trip after the emulator log says boot finished; don't add retries to tests |
| Session start fails with `device offline` or "instrumentation process cannot be initialized", usually just after another session ended; the device is fine a moment later | The emulator's adb link drops briefly (its adb daemon shows one host connection replacing another) | Harden session **start-up** only: clear port forwards and the UiAutomator2 helper, allow a 60 s helper launch, and retry session creation once on these two errors. Never retry tests to hide it. |
| Straight after a cold boot, every session fails with "'...SplashActivity' never started", yet the app opens fine by hand | Not device health: the splash screen hands over to the main activity before Appium checks, and Appium waits only for the launch activity (the debug log repeats "None of the expected package/activity combinations matched", with the focus already on `MainActivity`) | Set `appWaitActivity` to the app's activities (e.g. `<package>.view.activities.*`) in the session options. A launch-and-wait warm-up in the run script does not help. |
