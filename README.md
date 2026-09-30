# My Demo App: Android Mobile Test Automation

![Mobile tests](https://github.com/Anusreepsuresh074/mydemoapp-mobile-automation/actions/workflows/mobile-tests.yml/badge.svg) · **[Live Allure report](https://anusreepsuresh074.github.io/mydemoapp-mobile-automation/)** · **[Test Summary Report](docs/test-summary-report.md)**

Automated end-to-end tests for Sauce Labs' [My Demo App](https://github.com/saucelabs/my-demo-app-android), a public practice shopping app for Android, written in **Python + pytest** with **Appium** (UiAutomator2) and reported in **Allure**. They cover the whole shopping journey (catalogue, sorting, product details, cart, sign-in and sign-out, checkout with address, payment and review) and how the app behaves on a phone (Back button, background, rotation, restart).

**62 test cases (28 positive, 18 negative, 16 edge), 43 of them found through six exploratory testing sessions, built with the Page Object Model from locators confirmed on the running app.** The smoke suite runs on every push and the full regression nightly, on an Android emulator in GitHub Actions. **8 real app defects** were found, including a crash and two security issues, and are kept visible as strict xfails.

```
smoke        6 tests:  6 passed                              (~90 s)
regression  66 tests: 53 passed, 12 xfailed, 1 skipped        (~19 min; xfailed = known defects, skipped = blocked by the crash)
retries      none: every pass is a first-attempt pass
```

Full results, defects and open items: [`docs/test-summary-report.md`](docs/test-summary-report.md). Exploratory session notes and evidence: [`docs/exploratory/`](docs/exploratory/exploratory-sessions.md).

This is the mobile part of my QA portfolio, alongside my [UI tests in Playwright](https://github.com/Anusreepsuresh074/automationexercise-ui-tests-eCommerce), API tests in [pytest](https://github.com/Anusreepsuresh074/ecommerce-api-automation) and [Postman + Newman](https://github.com/Anusreepsuresh074/dummyjson-postman-newman), and [performance tests in JMeter](https://github.com/Anusreepsuresh074/ecommerce-performance-testing).

## What this project demonstrates

| Skill | Where to see it |
|---|---|
| **Test design before code:** 62 cases, each traced to one of 31 rules, typed positive / negative / edge, audited for coverage and approved before automation | [`docs/context/mydemoapp-shopping-testcases.md`](docs/context/mydemoapp-shopping-testcases.md), [`docs/context/mydemoapp-coverage-audit.md`](docs/context/mydemoapp-coverage-audit.md) |
| **Exploratory testing:** six chartered sessions with notes, screenshots and a device crash log; every finding became a test case | [`docs/exploratory/exploratory-sessions.md`](docs/exploratory/exploratory-sessions.md) |
| **Page Object Model:** a `BasePage` with explicit waits, one page object per screen, shared components (header, side menu, sort sheet), methods that return the next page | [`src/pages/`](src/pages/), [`docs/framework-rules.md`](docs/framework-rules.md) |
| **Locators from the real app:** every locator was confirmed from UI dumps of the running app, never from source code or designs | [`src/pages/`](src/pages/), [`docs/mydemoapp-flow.md`](docs/mydemoapp-flow.md) |
| **Independent tests:** each test starts from a cleared, relaunched app, so tests can run in any order | [`tests/conftest.py`](tests/conftest.py) |
| **Fixtures and test data:** shared starting points (`catalog`, `signed_in`, `first_product_in_cart`, `address_page`, `payment_page`); each feature's data in its own `*_td.py`; parametrised families of cases | [`tests/conftest.py`](tests/conftest.py), [`tests/checkout/checkout_td.py`](tests/checkout/checkout_td.py) |
| **Tagging:** every test carries its case ID, priority (`p0`–`p2`) and suite (`smoke`, `regression`) | [`pytest.ini`](pytest.ini), [`tests/`](tests/) |
| **Known defects handled honestly:** strict xfail, so the run flags it the moment the app is fixed; a case blocked by a defect is skipped with its reason, not faked | e.g. `test_review_hides_the_card_number`, `test_two_different_products_add_up` |
| **Mobile-specific checks:** the phone's Back button, background and resume, rotation, app restart, the soft keyboard, disabled buttons | [`tests/app_state/`](tests/app_state/test_app_state.py) |
| **Environment health first:** memory, CPU, Appium and device are checked before a run, so a bad machine fails clearly instead of as flaky tests | [`scripts/env-check.sh`](scripts/env-check.sh) |
| **Reporting:** Allure steps, with a screenshot and page source attached on failure; the password is never recorded (the login step takes no parameters, and it prints as `********` in tracebacks) | [`tests/conftest.py`](tests/conftest.py), [`docs/test-summary-report.md`](docs/test-summary-report.md) |
| **CI/CD:** an Android emulator with KVM on GitHub Actions; smoke on push, regression nightly; results uploaded as artifacts | [`.github/workflows/mobile-tests.yml`](.github/workflows/mobile-tests.yml) |
| **Root-causing, not retrying:** no test retries anywhere; framework problems were fixed at the cause | [Found while building it](#found-while-building-it) |

## Test cases

| Feature | Cases | Positive | Negative | Edge | What is covered |
|---|---|---|---|---|---|
| Catalogue | 6 | 5 | 0 | 1 | Name and price on every card; all 4 sort orders across all 24 products; every product listed |
| Product | 8 | 4 | 0 | 4 | Details; + and −; Add to cart disabled at 0; quantity 13; colours; rating; the crash (D-07) |
| Cart | 10 | 7 | 0 | 3 | Badge, count and total; same product twice; the cart's + and −; removing; Go Shopping; restart; two products (blocked) |
| Sign-in | 13 | 5 | 6 | 2 | Demo user; empty, missing, locked-out, unknown, wrong password, not an email; 300 characters; special characters; masked password; tap-to-fill; Log Out and Cancel |
| Checkout | 17 | 5 | 11 | 1 | Placing an order; sign-in gate; every required address field; payment validation; review total with delivery; masked card; billing address |
| App and phone | 8 | 2 | 1 | 5 | Background (3 screens); portrait lock; the Back button (3 screens); restart signs out |
| **Total** | **62** | **28** | **18** | **16** | 7 P0, 31 P1, 24 P2; 43 found by exploratory testing |

The P0 cases that pass form the smoke suite. Every case's status and test is in [`docs/mydemoapp-flow.md`](docs/mydemoapp-flow.md#flow-status).

## Defects found

| # | Severity | What happens | Should be |
|---|---|---|---|
| D-07 | Critical | Opening a product, going back and opening a **different** product **crashes the app** (`NullPointerException` in `ProductCatalogFragment`, [log](docs/exploratory/d07-crash-log.txt)) | The second product opens |
| D-01 | High, security | Login accepts any username and password, including the real user with a wrong password | Refused, with an error |
| D-08 | High, security | The review screen shows the full card number | Masked, e.g. `**** 1111` |
| D-06 | High | Card details are not validated: a 5-digit number, a 1-digit security code, an expired or half-typed date are accepted | Refused, with an error |
| D-03 | Medium | The phone's Back button with the side menu open closes the whole app | Closes the menu |
| D-04 | Medium | Any text is accepted as a username (`bob`, 300 characters, special characters) | An email address is required |
| D-02 | Medium | The minus button lowers the product quantity to 0 | Quantity stops at 1 |
| D-05 | Low | The country error reads "Please provide your" | "Please provide your country." |

## Found while building it

- **"SplashActivity never started" after a cold boot.** Every session failed right after the emulator booted, although the app opened fine by hand. Appium's debug log showed that the app *had* started: the splash screen had already handed over to `MainActivity`, and Appium was waiting only for the splash screen. The fix is one session option (`appWaitActivity`) that accepts any of the app's activities, not a longer wait. A warm-up step I tried first didn't help, so I removed it.
- **Appium kept running after the tests.** The run script started Appium through `npx` and stopped only `npx`, so the server was left behind and the run hung. The script now starts the Appium binary directly, so its exit trap stops the real server.
- **Passed locally, failed in CI.** 4 smoke tests couldn't find the Add to cart button in GitHub Actions. The CI failure screenshot showed why: the emulator's default screen is 320x640, so the button was below the edge. CI now runs the same Pixel 6 profile (1080x2400) as the local emulator.
- **CI secrets were being overwritten.** CI copies `.env.example` to `.env`, and the run script loaded it on top of the environment, replacing the login secrets with empty placeholders. Values already in the environment now win.
- **The old sort tests only checked 4 of 24 products.** Exploratory testing showed the catalogue scrolls; the catalogue page object now reads each card as a (name, price) pair and scrolls to the end, because a name and its price can sit on different sides of the screen edge.
- **Two screens share a button id.** Review Order (payment) and Place Order (review) are both `paymentBtn`, so a check on the button said "the review is open" while still on payment. `is_open()` now checks each screen's own heading.
- **A disabled button is never "clickable".** The quantity-0 test waited forever to tap Add to cart; the page object has a separate method for pressing a disabled button on purpose.
- **A short wait passed locally but failed in CI.** After the rebuild, the new "is this screen open?" checks used the 3-second wait meant for "is it gone?" checks, and GitHub's slower emulator needed longer. Screen checks now wait up to 15 s, and absence checks pass a short wait on purpose.
- **A test case was based on a misread note.** The cart-after-restart case first expected the cart to survive; I re-checked it on the live app and updated the case to the observed behaviour.
- **Brief adb drops on the emulator** right after a cold boot or between sessions. Only **set-up** is hardened: session start-up (cleaning up leftovers and one retry on those exact errors) and the per-test app reset (waiting for the device and one retry); tests themselves are never retried.

## Running it

Requires Python 3.12, Node.js 22, Java 21, the Android SDK (platform-tools and an emulator image for API 35) and a running emulator.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
npm ci                                                         # Appium and the Allure CLI, pinned
APPIUM_HOME=$PWD/.appium npx appium driver install uiautomator2
cp .env.example .env                                           # add the demo login shown on the app's login screen

scripts/fetch-build.sh                 # download the pinned app build (2.3.0, build 27)
scripts/run-tests.sh -m smoke          # the 6 smoke tests
scripts/run-tests.sh -m regression     # all 66 test runs
npx allure serve allure-results        # open the report
```

`run-tests.sh` starts Appium, runs the health check, turns off animations, runs pytest and stops Appium at the end.

## CI

[`.github/workflows/mobile-tests.yml`](.github/workflows/mobile-tests.yml) runs on pushes to `main`, pull requests, on demand, and nightly at 03:00 UTC:

1. **Lint:** ruff on the code.
2. **Mobile tests:** installs the dependencies and Appium, downloads the app build, boots an API 35 emulator with KVM acceleration, and runs the smoke tests (on push and pull request) or the full regression (nightly and on demand).
3. **Artifacts:** the Allure results and the Appium log are uploaded on every run, pass or fail.
4. **Live report:** nightly and manual runs publish the full regression's Allure report, with history, to [GitHub Pages](https://anusreepsuresh074.github.io/mydemoapp-mobile-automation/).

Repository secrets needed: `TEST_USERNAME`, `TEST_PASSWORD` (the app's public demo login).

## Project structure

| Path | What it is |
|---|---|
| `src/core/` | Settings (`config.py`) and the Appium session (`driver.py`) |
| `src/pages/base_page.py` | `BasePage`: explicit waits, tap, type, read, scroll, Back, keyboard; locator helpers |
| `src/pages/*_page.py` | One page object per screen: catalogue, product, cart, login, and the four checkout steps |
| `src/pages/components/` | Parts shared by several screens: header bar, side menu (with its Log Out dialog), sort sheet |
| `src/utils/` | Small helpers, such as reading a price |
| `tests/conftest.py` | The session, a fresh app per test, shared starting-point fixtures, failure screenshots |
| `tests/<feature>/` | `test_<feature>.py` and its test data `<feature>_td.py`: catalog, product, cart, login, checkout, app_state |
| `docs/exploratory/` | Exploratory session notes, screenshots and the crash log |
| `docs/context/` | The app's observed rules, the test design and the coverage audit |
| `docs/mydemoapp-flow.md` | Screens, confirmed locators and each case's status |
| `docs/test-summary-report.md` | The results, defects and open items |
| `scripts/` | `run-tests.sh` (the one way to run), `env-check.sh`, `fetch-build.sh` |
| `skills/`, `agents/` | The reusable skills this project was built with, and the agent that orders them |

## How it was built

Through the same reusable, AI-assisted workflow as my other projects: written [Claude Code](https://claude.com/claude-code) skills run in order by [`agents/mobile-automation-agent.md`](agents/mobile-automation-agent.md).

1. `mobile-env-check` and `mobile-build-fetch`: a healthy machine and emulator, and the pinned app build.
2. `create-mobile-framework-structure`: the framework (first in four layers, then rebuilt as a Page Object Model), config and scripts.
3. `get-mobile-context` and `get-mobile-auth`: every screen walked on the live app, and its rules written down with their source.
4. `mobile-test-design`: the first 19 cases, then a stop for review; `mobile-coverage-audit` checked them against every rule and screen.
5. Six exploratory sessions on the live app, then a second, approved test design (62 cases).
6. `mobile-test-automation`: locators confirmed on the running app, then page objects, components, fixtures and tests, each run until stable.
7. `mobile-test-report` and `mobile-teardown`: the Allure report, the summary report and clean-up.
8. `mobile-ci-integration`: the GitHub Actions pipeline.

Every result was run and checked, not assumed.

## License

[MIT](LICENSE)
