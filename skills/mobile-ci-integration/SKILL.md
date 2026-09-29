---
name: mobile-ci-integration
description: Runs the mobile suite on GitHub Actions instead of a personal machine - checkout, Python and Node, Appium and its driver, a hardware-accelerated Android emulator, the environment check, a marker subset of tests, and the Allure results uploaded on every run. Secrets only from the CI secret store. Use once the suite passes locally, headless.
---

# Mobile CI Integration

A test that only passes on one laptop isn't a regression suite yet.

## When to use

- After the suite passes locally with no manual steps.
- Again when a new platform or marker is added.

## Rules

- **Headless and hands-free.** Tests marked `manual` never run in CI.
- **Secrets in the secret store only**, passed as environment variables.
- **Hardware acceleration first.** Android emulators need KVM on the runner;
  enable it rather than accept a software-rendered emulator that times out.
- **Watch the first real run.** A workflow that has never run is a draft.

## Pipeline

1. **Checkout** and set up Python and Node.js.
2. **Install** Python dependencies, Appium and the UiAutomator2 driver
   (XCUITest for iOS).
3. **Get the build** (`mobile-build-fetch`: an artifact or a release download).
4. **Start the emulator** with an emulator-runner action on an Ubuntu runner
   (Android), or a simulator on a macOS runner (iOS).
5. **Start Appium**, run `mobile-env-check`'s checks, then run the tests by
   marker (`smoke` on every push, `regression` nightly).
6. **Always upload** the Allure results and failure attachments, even when
   tests fail; optionally publish the report to GitHub Pages.

## Output

`.github/workflows/mobile-tests.yml` and a note in the flow document on what
CI runs and when.
