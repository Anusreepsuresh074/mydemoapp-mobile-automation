# Test Summary Report — My Demo App (Android) Mobile Automation

## 1. Document control

| Version | Date | Author | Test design | Status |
|---|---|---|---|---|
| 1.0 | 2026-09-29 | Anusree P (drafted with the mobile-test-report skill) | [`context/mydemoapp-shopping-testcases.md`](context/mydemoapp-shopping-testcases.md), 19 cases, approved 2026-09-29 | **Final** |

## 2. Executive summary

**Verdict: the shopping journey works end to end, with 2 real defects found.** In the full regression, all 19 automated cases ran: **17 passed and 2 failed as expected (xfail)**, because of the two known defects in the app. No test was retried. The 6 smoke tests also passed straight after a cold boot of the emulator.

Key findings:

1. **The main journey is sound.** Browsing the catalogue, sorting, opening a product, adding to the cart, signing in, checking out and placing an order all behave as observed and expected. The same holds for the validation messages and for going to the background during checkout.
2. **Defect D-01: login accepts any credentials** (P1, case LGN-P1-05). An unknown username with a wrong password signs the user in. In a real shop this would be a security defect.
3. **Defect D-02: quantity can go down to 0** (P1, case PRD-P1-02). The minus button on the product screen goes below 1, so a product can be added to the cart with quantity 0.
4. **The suite is stable.** The full regression gave the same result (17 passed, 2 xfailed) on two earlier runs and again on the final run. Two framework problems found on 2026-09-29 were fixed before the final runs (section 7).

**Recommendation:** raise D-01 and D-02 with the app's owners. Keep both tests as strict xfail, so the suite reports the moment either defect is fixed. Add payment validation cases once the field rules are known (section 8).

## 3. Scope

| In scope | Out of scope |
|---|---|
| Catalogue, sorting, product details, cart, sign-in, checkout (address, payment, review, complete), app going to the background | WebView, QR code scanner, geo location, drawing, fingerprint, virtual USB, "crash app" menu items |

Because the app has no requirements document, the expected behaviour comes from walking the live app. Each rule and its source is in [`context/mydemoapp-shopping-context.md`](context/mydemoapp-shopping-context.md).

## 4. Test environment

| Item | Detail |
|---|---|
| App under test | [My Demo App](https://github.com/saucelabs/my-demo-app-android) by Sauce Labs, version 2.3.0 (build 27), package `com.saucelabs.mydemoapp.android` |
| Device | Android emulator `mydemo_api35`: Android 15 (API 35), x86_64, animations off |
| Automation | Appium 3.8.0 with the UiAutomator2 driver; Python 3.12, pytest 9.1, Appium Python Client 6.0 |
| Framework | Four layers: screens (locators) → actions → flows → tests; every locator was confirmed on the running app |
| Reporting | Allure (steps, plus a screenshot and page source attached on failure) |
| CI | GitHub Actions: the smoke tests on every push and pull request, the full regression nightly and on demand |

## 5. Execution summary

Final runs on 2026-09-29, local emulator:

| Run | Suite | Tests | Passed | Xfailed (known defect) | Failed | Duration |
|---|---|---|---|---|---|---|
| Smoke, straight after a cold boot | `-m smoke` | 6 | 6 | 0 | 0 | 83 s |
| Full regression | `-m regression` | 19 | 17 | 2 | 0 | 250 s |

CI runs on GitHub Actions (Android emulator, Pixel 6, API 35) on 2026-09-29:

| Run | Suite | Result | Duration |
|---|---|---|---|
| [36606150334](https://github.com/Anusreepsuresh074/mydemoapp-mobile-automation/actions/runs/36606150334) (push) | smoke | 6 passed | 143 s |
| [36606749256](https://github.com/Anusreepsuresh074/mydemoapp-mobile-automation/actions/runs/36606749256) (manual) | regression | 17 passed, 2 xfailed (second attempt; the first stopped at the health check, see section 7) | 339 s |

### Results by feature (full regression)

| Feature | Cases | Passed | Xfailed |
|---|---|---|---|
| Catalogue and product | 5 | 4 | 1 (D-02) |
| Cart | 4 | 4 | 0 |
| Sign-in | 5 | 4 | 1 (D-01) |
| Checkout and app state | 5 | 5 | 0 |
| **Total** | **19** | **17** | **2** |

### Results by priority

| Priority | Cases | Passed | Xfailed |
|---|---|---|---|
| P0 (release-blocking) | 6 | 6 | 0 |
| P1 | 11 | 9 | 2 |
| P2 | 2 | 2 | 0 |

Each case's status and test path are in the status table of [`mydemoapp-flow.md`](mydemoapp-flow.md#flow-status).

## 6. Defects

| ID | Case | Severity | Steps | Expected | Actual |
|---|---|---|---|---|---|
| D-01 | LGN-P1-05 | P1 (security) | Menu → Log In, sign in as `nobody@example.com` / `wrong-password` | Stays on Login with an error | Signed in; the menu shows "Log Out" |
| D-02 | PRD-P1-02 | P1 | Open a product, tap + twice, then − three times | Quantity stops at 1 | Quantity reaches 0 |

Both are marked **strict xfail**: the test is expected to fail while the defect exists. If the app is fixed, the test "unexpectedly passes" and the run fails, prompting someone to remove the marker.

## 7. Issues found and fixed during testing

| Symptom | Cause | Fix |
|---|---|---|
| After a cold boot, every test errored with "SplashActivity never started" | The app opened, but the splash screen handed over to `MainActivity` before Appium checked, and Appium only accepted the splash screen | `src/core/driver.py` sets `appWaitActivity` to any of the app's activities. Verified: 6 of 6 smoke tests pass straight after a cold boot. |
| The test run hung at the end with the Appium server still running | `scripts/run-tests.sh` started Appium through `npx` and stopped only `npx`, not the server | The script starts the Appium binary directly, so the exit trap stops the server. Verified after every run. |
| In CI, 4 smoke tests timed out on the product screen's quantity and Add to cart button | The CI emulator's default device profile is 320x640, so those elements were below the screen edge (seen in the CI failure screenshot) | The workflow runs the emulator as a Pixel 6 (`profile: pixel_6`), the same 1080x2400 screen as the local emulator |
| In CI, the sign-in tests failed with "TEST_USERNAME is not set" although the repository secrets existed | CI copies `.env.example` to `.env`, and `run-tests.sh` loaded it over the environment, replacing the secrets with empty placeholders | `run-tests.sh` loads `.env` only for keys not already set, so CI secrets win |
| One CI regression attempt stopped before any test ran: "emulator-5554 shows a 'not responding' dialog" | A system dialog on the freshly booted CI emulator; not reproduced on the second attempt | None needed: the health check stopped the run as designed instead of producing 19 misleading failures. Watched as an open item (section 8) |
| CRT-P2-04 first expected the cart to survive a restart | A misread walkthrough note | The case was re-checked on the live app and updated to the observed behaviour (a restart empties the cart) |

## 8. Coverage and open items

The [coverage audit](context/mydemoapp-coverage-audit.md) found no blocking gaps: all 15 rules and all 11 in-scope screens are covered, and every P0 journey is in the smoke suite.

| # | Open item | Next step |
|---|---|---|
| 1 | Payment details (R12) are only tested on the happy path | Add validation cases once the field rules are known |
| 2 | Sorting covers 2 of the 4 orders | Add price high-to-low and name A-to-Z if sorting changes |
| 3 | Tested on one Android version (API 35) | Add a second API level to CI for broader device coverage |
| 4 | A freshly booted CI emulator occasionally shows a "not responding" dialog, and the health check stops the run | If it recurs in the nightly runs, dismiss boot-time system dialogs before the health check |

## 9. How to reproduce

```bash
scripts/fetch-build.sh             # download the pinned app build
scripts/run-tests.sh -m smoke      # 6 smoke tests
scripts/run-tests.sh -m regression # all 19 tests
npx allure serve allure-results    # open the report
```

`run-tests.sh` starts Appium, runs the environment health check (`scripts/env-check.sh`), turns off animations, runs pytest, and stops Appium at the end.
