---
name: mobile-common-scenarios
description: Reference patterns for situations outside the app's own screens - system and permission dialogs, killing and relaunching the app, background and resume, deep links, and push notifications - each marked Confirmed or Unverified for the app under test. Consulted by mobile-test-automation; it does not run on its own.
---

# Mobile Common Scenarios

Mobile tests meet things a web test never does: the operating system itself.
These patterns keep those moments deliberate instead of accidental.

## How to use

Look up the situation, apply the pattern, and record in the flow document
whether it is **Confirmed** (seen working on this app) or **Unverified**.

## Patterns

**System and permission dialogs.** First find out who owns the dialog: dump
the screen and check the element's package (for example Android's permission
controller, not the app). Tap the button through that package's elements.
Appium's `autoGrantPermissions` capability grants runtime permissions at
install, but does not handle account pickers or other system sheets.

**Clean start.** Terminate and relaunch the app (`terminate_app`,
`activate_app`), then wait for the first screen's key element, not a fixed
time: a relaunch can finish before the screen is drawn.

**Background and resume.** `background_app(seconds)` sends the app to the
background and brings it back; assert the screen and its data survived.

**Rotation.** Set the orientation, assert the layout still shows the key
elements, set it back.

**Deep links.** Android: `adb shell am start -W -a android.intent.action.VIEW
-d "<scheme>://<path>" <package>`. iOS simulator: `xcrun simctl openurl
booted "<scheme>://<path>"`. Assert the app lands on the right screen.

**Push notifications.** Decide what is under test. The app's reaction to
tapping a notification can be tested by opening its deep link. Real delivery
needs a backend trigger, which is a `mobile-test-data` question.

## Rule

Diagnose before retrying: a dialog that "sometimes" blocks a tap is a missing
pattern, not a reason to add retries.
