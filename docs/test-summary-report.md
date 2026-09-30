# Test Summary Report — My Demo App (Android) Mobile Automation

## 1. Document control

| Version | Date | Author | Test design | Status |
|---|---|---|---|---|
| 1.0 | 2026-09-29 | Anusree P (drafted with the mobile-test-report skill) | Test cases v1: 19 cases, approved 2026-09-29 | Superseded by 2.0 |
| 2.0 | 2026-09-30 | Anusree P (drafted with the mobile-test-report skill) | [`context/mydemoapp-shopping-testcases.md`](context/mydemoapp-shopping-testcases.md) v2: 62 cases, approved 2026-09-30 | **Final**: adds six exploratory sessions, 43 new cases, 6 new defects, and the Page Object Model rebuild |

## 2. Executive summary

**Verdict: the main shopping journey works, but the app is not release-ready: 8 defects were found, including a crash (D-07) and two security issues (D-01, D-08).** The full regression ran 66 tests (62 cases; one case runs once per required field): **53 passed, 12 failed as expected because of known defects (strict xfail), and 1 was blocked by the crash.** No test was retried.

Key findings:

1. **The happy path is sound.** Browsing, all four sort orders across all 24 products, product details, the cart, sign-in and sign-out, checkout and placing an order behave as expected, and so do going to the background and the phone's Back button on most screens.
2. **D-07, critical: the app crashes** when a shopper opens a product, goes back and opens a different product. The device log shows a `NullPointerException` in the catalogue code. It also blocks testing a cart with two different products.
3. **Security: D-01** any username and password sign in (even the real user with a wrong password), and **D-08** the review shows the full card number.
4. **Validation gaps:** card details are not checked (D-06), usernames need not be email addresses (D-04), and the quantity can reach 0 (D-02), although Add to cart is then disabled.
5. **Smaller issues:** Back with the side menu open closes the app (D-03); the country error message is cut off (D-05).
6. **Exploratory testing paid off:** six chartered sessions found 6 of the 8 defects and 43 of the 62 cases, and showed that the old sort tests checked only 4 of 24 products.

**Recommendation:** do not release until D-07, D-01 and D-08 are fixed. Fix D-06 and D-04 next. Keep every defect test as a strict xfail, so the suite reports the moment one is fixed, and re-test the blocked two-product case after D-07.

## 3. Scope

| In scope | Out of scope |
|---|---|
| Catalogue, sorting, product details (quantity, colour, rating), cart, sign-in and sign-out, checkout (address, payment, review, complete); the phone's Back button, background, rotation and restart | WebView, QR code scanner, geo location, drawing, fingerprint, virtual USB, "crash app" menu items; the `visual@example.com` visual-testing user |

Because the app has no requirements document, the expected behaviour comes from walking the live app and from stated assumptions (marked *Assumption* in [`context/mydemoapp-shopping-context.md`](context/mydemoapp-shopping-context.md), 31 rules).

## 4. Test approach

| Activity | What was done |
|---|---|
| Scripted test design | 62 cases, each with an ID, priority, type (positive / negative / edge), steps, expected result and rule |
| Exploratory testing | Six chartered sessions with notes and evidence: [`exploratory/exploratory-sessions.md`](exploratory/exploratory-sessions.md) |
| Coverage audit | Every rule and screen mapped to cases: [`context/mydemoapp-coverage-audit.md`](context/mydemoapp-coverage-audit.md), no blocking gaps |
| Automation | Appium + pytest with the Page Object Model; every case automated (the blocked one is written and skipped) |

## 5. Test environment

| Item | Detail |
|---|---|
| App under test | [My Demo App](https://github.com/saucelabs/my-demo-app-android) by Sauce Labs, version 2.3.0 (build 27), package `com.saucelabs.mydemoapp.android` |
| Device | Android emulator `mydemo_api35`: Pixel 6 profile, Android 15 (API 35), x86_64, animations off |
| Automation | Appium 3.8.0 with the UiAutomator2 driver; Python 3.12, pytest 9.1, Appium Python Client 6.0 |
| Framework | Page Object Model: `BasePage`, one page object per screen, shared components, fixtures; every locator confirmed on the running app |
| Reporting | Allure (steps, plus a screenshot and page source attached on failure) |
| CI | GitHub Actions: the smoke tests on every push and pull request, the full regression nightly and on demand, on the same Pixel 6 / API 35 emulator |

## 6. Execution summary

Final local runs on 2026-09-30:

| Run | Suite | Test runs | Passed | Xfailed (known defect) | Skipped (blocked) | Failed | Duration |
|---|---|---|---|---|---|---|---|
| Full regression | `-m regression` | 66 | 53 | 12 | 1 | 0 | 1130 s |
| Smoke | `-m smoke` | 6 | 6 | 0 | 0 | 0 | 91 s |

{CI_RUNS}

### Results by feature (full regression)

| Feature | Cases | Test runs | Passed | Xfailed | Skipped |
|---|---|---|---|---|---|
| Catalogue | 6 | 6 | 6 | 0 | 0 |
| Product | 8 | 8 | 6 | 2 (D-02, D-07) | 0 |
| Cart | 10 | 10 | 9 | 0 | 1 (blocked by D-07) |
| Sign-in | 13 | 13 | 10 | 3 (D-01 ×2, D-04) | 0 |
| Checkout | 17 | 21 | 15 | 6 (D-05, D-06 ×4, D-08) | 0 |
| App and phone | 8 | 8 | 7 | 1 (D-03) | 0 |
| **Total** | **62** | **66** | **53** | **12** | **1** |

### Results by type and priority

| | Cases | Pass expected | Known defect | Blocked |
|---|---|---|---|---|
| Positive | 28 | 27 | 0 | 1 |
| Negative | 18 | 8 | 10 | 0 |
| Edge | 16 | 14 | 2 | 0 |
| P0 | 7 | 6 | 1 (D-07) | 0 |
| P1 | 31 | 24 | 6 | 1 |
| P2 | 24 | 19 | 5 | 0 |

Each case's status and test path are in the status table of [`mydemoapp-flow.md`](mydemoapp-flow.md#flow-status).

## 7. Defects

| ID | Severity | Case | Steps | Expected | Actual |
|---|---|---|---|---|---|
| D-07 | Critical | PRD-P0-08 (blocks CRT-P1-10) | Open a product, press Back, open a different product | The second product opens | The app closes; `NullPointerException` in `ProductCatalogFragment.java:156` ([log](exploratory/d07-crash-log.txt)) |
| D-01 | High (security) | LGN-P1-05, LGN-P1-06 | Sign in as `nobody@example.com` / `wrong-password`, or as the real user with a wrong password | Refused with an error | Signed in |
| D-08 | High (security) | CHK-P1-16 | Reach the review screen | The card number is masked | The full number is shown ([screenshot](exploratory/screenshots/d08-review-full-card-number.png)) |
| D-06 | High | CHK-P1-10 to CHK-P2-13 | Enter a 5-digit card number, an expired date (01/20), an incomplete date ("1") or a 1-digit security code | Refused with an error | Accepted; the review opens |
| D-03 | Medium | APP-P2-07 | Open the side menu, press the phone's Back button | The menu closes | The whole app closes |
| D-04 | Medium | LGN-P2-07 | Sign in as `bob` (not an email) | Refused with an error | Signed in |
| D-02 | Medium | PRD-P1-02 | On a product, tap + twice, then − three times | Quantity stops at 1 | Quantity reaches 0 (Add to cart is then disabled) |
| D-05 | Low | CHK-P2-06 | Leave Country empty, tap To Payment | "Please provide your country." | "Please provide your" ([screenshot](exploratory/screenshots/d05-country-error-cut-off.png)) |

Every defect test is marked **strict xfail**: it is expected to fail while the defect exists. If the app is fixed, the test "unexpectedly passes" and the run fails, prompting someone to remove the marker. The blocked case is **skipped** with the reason "Blocked by D-07".

## 8. Issues found and fixed during testing

| Symptom | Cause | Fix |
|---|---|---|
| After a cold boot, every test errored with "SplashActivity never started" | The app opened, but the splash screen handed over to `MainActivity` before Appium checked, and Appium only accepted the splash screen | `src/core/driver.py` sets `appWaitActivity` to any of the app's activities. Verified: 6 of 6 smoke tests pass straight after a cold boot. |
| The test run hung at the end with the Appium server still running | `scripts/run-tests.sh` started Appium through `npx` and stopped only `npx`, not the server | The script starts the Appium binary directly, so the exit trap stops the server. Verified after every run. |
| In CI, 4 smoke tests timed out on the product screen's quantity and Add to cart button | The CI emulator's default device profile is 320x640, so those elements were below the screen edge (seen in the CI failure screenshot) | The workflow runs the emulator as a Pixel 6 (`profile: pixel_6`), the same 1080x2400 screen as the local emulator |
| In CI, the sign-in tests failed with "TEST_USERNAME is not set" although the repository secrets existed | CI copies `.env.example` to `.env`, and `run-tests.sh` loaded it over the environment, replacing the secrets with empty placeholders | `run-tests.sh` loads `.env` only for keys not already set, so CI secrets win |
| One CI regression attempt stopped before any test ran: "emulator-5554 shows a 'not responding' dialog" | A system dialog on the freshly booted CI emulator; not reproduced on the second attempt | None needed: the health check stopped the run as designed instead of producing many misleading failures. Watched as an open item (section 8) |
| The sort tests passed while checking only 4 of 24 products | The catalogue scrolls; the tests read only the first screen (found in exploratory session S1) | The catalogue page object reads each card as a (name, price) pair and scrolls to the end; all four sort tests check all 24 products |
| "The review is open" was true while still on the payment screen | Review Order and Place Order share the resource id `paymentBtn` | `CheckoutReviewPage.is_open()` checks the review heading instead of the button |
| The quantity-0 test waited forever to tap Add to cart | The button is disabled at quantity 0, and the framework only taps clickable elements (correctly) | A separate page method presses a disabled button on purpose |
| After the rebuild, every CI smoke test errored at set-up: "the app did not open on the catalogue" | The new screen checks used the 3 s wait meant for absence checks; the CI emulator is slower | `is_open()` waits up to 15 s; absence checks pass a short timeout explicitly; "signed in" is decided by the menu alone |
| The test password appeared in the Allure results (checked before publishing the report) | A decorated `@allure.step` records every argument, and a failure traceback prints the credentials tuple | The login step is a `with allure.step(...)` block (no parameters); the password is a string that prints as `********`; a scan of 203 result files found it 0 times |
| A sort test once read 10 of 24 products | Reading stopped after two swipes found nothing new, and a swipe that does not move the grid ended it early | Reading stops when Appium reports the end of the list |
| CRT-P2-04 first expected the cart to survive a restart | A misread walkthrough note | The case was re-checked on the live app and updated to the observed behaviour (a restart empties the cart) |

## 9. Coverage and open items

The [coverage audit](context/mydemoapp-coverage-audit.md) found no blocking gaps: all 31 rules and all in-scope screens are covered, every feature has positive, negative and edge cases, and every passing P0 journey is in the smoke suite.

| # | Open item | Next step |
|---|---|---|
| 1 | A cart with two different products is blocked by D-07 | Re-run CRT-P1-10 once D-07 is fixed (remove the skip) |
| 2 | The payment rules (card length, a future expiry date, a 3–4 digit code) are assumptions | Confirm them with a product owner |
| 3 | Tested on one Android version (API 35) and one screen size | Add a second API level and a small-screen profile to CI |
| 4 | A freshly booted CI emulator occasionally shows a "not responding" dialog, and the health check stops the run | If it recurs in the nightly runs, dismiss boot-time system dialogs before the health check |
| 5 | Real-device behaviour (camera, battery, real networks) is not covered by an emulator | Run the smoke suite on a device cloud |

## 10. How to reproduce

```bash
scripts/fetch-build.sh             # download the pinned app build
scripts/run-tests.sh -m smoke      # 6 smoke tests
scripts/run-tests.sh -m regression # all 66 test runs
npx allure serve allure-results    # open the report
```

`run-tests.sh` starts Appium, runs the environment health check (`scripts/env-check.sh`), turns off animations, runs pytest, and stops Appium at the end.
