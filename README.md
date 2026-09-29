# My Demo App: Android Mobile Test Automation

![Mobile tests](https://github.com/Anusreepsuresh074/mydemoapp-mobile-automation/actions/workflows/mobile-tests.yml/badge.svg)

Automated end-to-end tests for Sauce Labs' [My Demo App](https://github.com/saucelabs/my-demo-app-android), a public practice shopping app for Android, written in **Python + pytest** with **Appium** (UiAutomator2) and reported in **Allure**. They cover the whole shopping journey: catalogue, sorting, product details, cart, sign-in, checkout (address, payment, review) and the app going to the background.

**19 test cases, designed and reviewed before any code was written, and built in four layers (screens → actions → flows → tests) from locators confirmed on the running app.** The smoke suite runs on every push and the full regression nightly, on an Android emulator in GitHub Actions. Two real app defects are kept visible as strict xfails.

```
smoke        6 tests:  6 passed                  (~80 s, straight after a cold emulator boot)
regression  19 tests: 17 passed, 2 xfailed        (~4 min; the 2 xfails are the known defects)
retries      none: every pass is a first-attempt pass
```

Full results, defects and open items: [`docs/test-summary-report.md`](docs/test-summary-report.md).

This is the mobile part of my QA portfolio, alongside my [UI tests in Playwright](https://github.com/Anusreepsuresh074/automationexercise-ui-tests-eCommerce), API tests in [pytest](https://github.com/Anusreepsuresh074/ecommerce-api-automation) and [Postman + Newman](https://github.com/Anusreepsuresh074/dummyjson-postman-newman), and [performance tests in JMeter](https://github.com/Anusreepsuresh074/ecommerce-performance-testing).

## What this project demonstrates

| Skill | Where to see it |
|---|---|
| **Test design before code:** 19 cases, each traced to a rule observed in the live app, audited for coverage and approved before automation | [`docs/context/mydemoapp-shopping-testcases.md`](docs/context/mydemoapp-shopping-testcases.md), [`docs/context/mydemoapp-coverage-audit.md`](docs/context/mydemoapp-coverage-audit.md) |
| **Layered framework:** screens hold only locators, actions are what a user does on one screen, flows cross screens, tests only arrange and assert | [`src/`](src/), [`docs/framework-rules.md`](docs/framework-rules.md) |
| **Locators from the real app:** every locator was confirmed from UI dumps of the running app, never from source code or designs | [`src/screens/mydemoapp/_ids.py`](src/screens/mydemoapp/_ids.py), [`docs/mydemoapp-flow.md`](docs/mydemoapp-flow.md) |
| **Independent tests:** each test starts from a cleared, relaunched app, so tests can run in any order | [`tests/conftest.py`](tests/conftest.py) |
| **Tagging:** every test carries its case ID, priority (`p0`–`p2`) and suite (`smoke`, `regression`) | [`pytest.ini`](pytest.ini), [`tests/mydemoapp/`](tests/mydemoapp/) |
| **Known defects handled honestly:** strict xfail, so the run flags it the moment the app is fixed | `test_wrong_credentials_are_refused`, `test_quantity_goes_up_and_not_below_one` |
| **Environment health first:** memory, CPU, Appium and device are checked before a run, so a bad machine fails clearly instead of as flaky tests | [`scripts/env-check.sh`](scripts/env-check.sh) |
| **Reporting:** Allure steps, with a screenshot and page source attached on failure | [`tests/conftest.py`](tests/conftest.py), [`docs/test-summary-report.md`](docs/test-summary-report.md) |
| **CI/CD:** an Android emulator with KVM on GitHub Actions; smoke on push, regression nightly; results uploaded as artifacts | [`.github/workflows/mobile-tests.yml`](.github/workflows/mobile-tests.yml) |
| **Root-causing, not retrying:** no test retries anywhere; framework problems were fixed at the cause | [Found while building it](#found-while-building-it) |

## Test cases

| Feature | Cases | What is covered |
|---|---|---|
| Catalogue and product | 5 | Products show a name and price; sort by price and by name; product details; quantity limits |
| Cart | 4 | Adding updates the badge and total; quantity 2; removing the only item; a restart empties the cart |
| Sign-in | 5 | Demo user signs in; empty username; missing password; locked-out user; wrong credentials |
| Checkout and app state | 5 | Placing an order; checkout while signed out asks for sign-in; required address fields; the cart is empty after an order; checkout survives the app going to the background |

6 cases are P0 (release-blocking) and form the smoke suite. The status of each case is in [`docs/mydemoapp-flow.md`](docs/mydemoapp-flow.md#flow-status).

## Defects found

| # | What happens | Should be |
|---|---|---|
| D-01 | Login accepts any username and password (`nobody@example.com` / `wrong-password` signs in) | Refused, with an error |
| D-02 | The minus button lowers the product quantity to 0 | Quantity stops at 1 |

## Found while building it

- **"SplashActivity never started" after a cold boot.** Every session failed right after the emulator booted, although the app opened fine by hand. Appium's debug log showed that the app *had* started: the splash screen had already handed over to `MainActivity`, and Appium was waiting only for the splash screen. The fix is one session option (`appWaitActivity`) that accepts any of the app's activities, not a longer wait. A warm-up step I tried first didn't help, so I removed it.
- **Appium kept running after the tests.** The run script started Appium through `npx` and stopped only `npx`, so the server was left behind and the run hung. The script now starts the Appium binary directly, so its exit trap stops the real server.
- **Passed locally, failed in CI.** 4 smoke tests couldn't find the Add to cart button in GitHub Actions. The CI failure screenshot showed why: the emulator's default screen is 320x640, so the button was below the edge. CI now runs the same Pixel 6 profile (1080x2400) as the local emulator.
- **CI secrets were being overwritten.** CI copies `.env.example` to `.env`, and the run script loaded it on top of the environment, replacing the login secrets with empty placeholders. Values already in the environment now win.
- **A test case was based on a misread note.** The cart-after-restart case first expected the cart to survive; I re-checked it on the live app and updated the case to the observed behaviour.
- **Brief adb drops on the emulator** right after a cold boot or between sessions. Only session **start-up** is hardened (cleaning up leftovers and one retry on those two exact errors); tests themselves are never retried.

## Running it

Requires Python 3.12, Node.js 22, Java 21, the Android SDK (platform-tools and an emulator image for API 35) and a running emulator.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
npm ci                                                         # Appium and the Allure CLI, pinned
APPIUM_HOME=$PWD/.appium npx appium driver install uiautomator2
cp .env.example .env                                           # add the demo login shown on the app's login screen

scripts/fetch-build.sh                 # download the pinned app build (2.3.0, build 27)
scripts/run-tests.sh -m smoke          # the 6 smoke tests
scripts/run-tests.sh -m regression     # all 19 tests
npx allure serve allure-results        # open the report
```

`run-tests.sh` starts Appium, runs the health check, turns off animations, runs pytest and stops Appium at the end.

## CI

[`.github/workflows/mobile-tests.yml`](.github/workflows/mobile-tests.yml) runs on pushes to `main`, pull requests, on demand, and nightly at 03:00 UTC:

1. **Lint:** ruff on the code.
2. **Mobile tests:** installs the dependencies and Appium, downloads the app build, boots an API 35 emulator with KVM acceleration, and runs the smoke tests (on push and pull request) or the full regression (nightly and on demand).
3. **Artifacts:** the Allure results and the Appium log are uploaded on every run, pass or fail.

Repository secrets needed: `TEST_USERNAME`, `TEST_PASSWORD` (the app's public demo login).

## Project structure

| Path | What it is |
|---|---|
| `src/core/` | Settings, the Appium session and the base screen |
| `src/screens/` | Locators and small reads, one class per screen |
| `src/actions/` | What a user does on each screen |
| `src/flows/` | Journeys across screens, such as "add to cart and check out" |
| `src/constants/` | Test data (no credentials) |
| `tests/` | One test per approved case, plus shared fixtures in `conftest.py` |
| `docs/context/` | The app's observed rules, the test design and the coverage audit |
| `docs/mydemoapp-flow.md` | Screens, confirmed locators and each case's status |
| `docs/test-summary-report.md` | The results, defects and open items |
| `scripts/` | `run-tests.sh` (the one way to run), `env-check.sh`, `fetch-build.sh` |
| `skills/`, `agents/` | The reusable skills this project was built with, and the agent that orders them |

## How it was built

Through the same reusable, AI-assisted workflow as my other projects: written [Claude Code](https://claude.com/claude-code) skills run in order by [`agents/mobile-automation-agent.md`](agents/mobile-automation-agent.md).

1. `mobile-env-check` and `mobile-build-fetch`: a healthy machine and emulator, and the pinned app build.
2. `create-mobile-framework-structure`: the four-layer framework, config and scripts.
3. `get-mobile-context` and `get-mobile-auth`: every screen walked on the live app, and its rules written down with their source.
4. `mobile-test-design`: the 19 cases, then a stop for review; `mobile-coverage-audit` checked them against every rule and screen.
5. `mobile-test-automation`: locators confirmed on the running app, then screens, actions, flows and tests, each run until stable.
6. `mobile-test-report` and `mobile-teardown`: the Allure report, the summary report and clean-up.
7. `mobile-ci-integration`: the GitHub Actions pipeline.

Every result was run and checked, not assumed.

## License

[MIT](LICENSE)
