# Framework Rules

The rules every skill follows and `review-automation-changes` checks. The framework uses the **Page Object Model (POM)**, the same structure as the Playwright UI project in this portfolio.

## Structure

| Part | Folder | Holds | May use |
| --- | --- | --- | --- |
| Core | `src/core/` | Settings (`config.py`) and the Appium session (`driver.py`) | Nothing in `src/pages/` |
| Base page | `src/pages/base_page.py` | `BasePage`: explicit waits, tap, type, read, scroll, Back, keyboard; the locator helpers (`by_id`, `by_accessibility_id`, `by_text`, `by_id_and_text`, `by_android_id`) | The driver |
| Page objects | `src/pages/<screen>_page.py` | One class per screen: its locators as class attributes, and methods for what a user can do and read there | `BasePage`, components, other pages (a method that moves to another screen returns that screen's page) |
| Components | `src/pages/components/` | Parts shared by several screens: the header bar (menu, cart, badge), the side menu (and its Log Out dialog), the sort sheet | `BasePage`, pages |
| Utilities | `src/utils/` | Small helpers with no screen, such as reading a price | Nothing app-specific |
| Fixtures | `tests/conftest.py` | The session, a fresh app per test, and shared starting points (`catalog`, `signed_in`, `first_product_in_cart`, `address_page`, `payment_page`) | Pages |
| Tests | `tests/<feature>/test_<feature>.py` | The checks, one test per approved case (or one parametrised test for a family of cases) | Fixtures and pages |
| Test data | `tests/<feature>/<feature>_td.py` | The inputs and expected values for that feature | Nothing |

A test never uses a locator directly: it calls page methods. Only page objects know where things are on the screen.

## Locators

- Defined only in page objects and components, as class attributes.
- Priority: resource id (this app gives every element one), then accessibility id, then UiAutomator (id + text for rows that share an id), then text, then XPath (with a written reason; none are used).
- Named with a type prefix: `btn_`, `input_`, `txt_`, `msg_`, `chk_`, `lnk_`, `icn_`, `card_`.
- Confirmed on the running app (UI dumps) before use.
- When two screens share an id (Review Order and Place Order are both `paymentBtn`), `is_open()` checks something unique to the screen.

## Page methods

- Actions are verbs (`add_to_cart`, `log_in`, `sort_by`) and carry an `@allure.step`, so reports read as steps.
- Reads return values (`quantity()`, `errors()`, `cart_badge()`); `is_open()` says whether the screen is showing.
- A method that lands on another screen returns that screen's page object (`header.open_cart()` returns `CartPage`).
- Pages don't assert, except as a guard that a screen actually opened.

## Waiting

Wait for conditions (visible, clickable) with explicit waits, 15 s by default. No `time.sleep` anywhere. A disabled button is never "clickable", so a test that presses one on purpose uses a method made for that (`press_add_to_cart`).

## Assertions

In tests, with a clear message.

## Tests

- Named after the behaviour: `test_same_product_twice_makes_one_row`.
- Every test has a priority marker (`p0`, `p1`, `p2`), a run marker (`smoke` and/or `regression`), an Allure feature, and an Allure title that starts with its case ID.
- Known defects: `@pytest.mark.xfail(reason="D-xx: …", strict=True)`. Cases blocked by a defect: `@pytest.mark.skip(reason="Blocked by D-xx: …")`.
- Every test maps to an approved case ID in `docs/context/`.
- No retries: a flaky test is fixed at its cause.

## Secrets and settings

Settings and credentials come from `.env` (git-ignored) or the CI secret store; values already in the environment win over `.env`. `.env.example` lists the names. Nothing secret is printed, logged or reported.

## Documents

`docs/<app>-flow.md` (screens, locators, sign-in, data, status); `docs/context/` (the rules, the approved test cases, the coverage audit); `docs/exploratory/` (session notes and evidence); `docs/test-summary-report.md`.
