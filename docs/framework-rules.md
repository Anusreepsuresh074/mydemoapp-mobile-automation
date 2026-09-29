# Framework Rules

The rules every skill follows and `review-automation-changes` checks.

## Layers

| Layer | Folder | Holds | May use |
| --- | --- | --- | --- |
| Screens | `src/screens/<app>/` | One class per screen: its locators and small `find_` helpers | The driver |
| Actions | `src/actions/<app>/` | What a user can do on one screen: tap, type, swipe | Screens |
| Flows | `src/flows/<app>/` | Journeys across screens: "sign in", "add to cart and check out" | Actions |
| Tests | `tests/<app>/` | The checks, one test per approved case | Flows (and actions for one-screen cases) |

Imports only point downwards: a screen never imports an action, an action
never imports a flow.

## Locators

- Defined only in screen classes.
- Priority: accessibility id, then resource-id / UiAutomator, then iOS
  predicate or class chain, then text, then XPath (with a written reason).
- Named with a type prefix: `btn_`, `input_`, `txt_`, `msg_`, `chk_`, `lnk_`,
  `icn_`, `tab_`, `card_`.
- Confirmed on a running app before use.

## Waiting

Wait for conditions (visible, clickable, text present) with explicit waits.
No `time.sleep` in tests, flows, actions or screens.

## Assertions

In tests, with a clear message. Screens and actions return elements and
values; they don't assert.

## Tests

- Named after the behaviour: `test_adding_a_product_updates_the_cart_badge`.
- Every test has a priority marker (`p0`, `p1`, `p2`) and a run marker
  (`smoke` or `regression`), and an Allure feature label.
- Every test maps to an approved case ID in `docs/context/`.

## Secrets and settings

Settings and credentials come from `.env` (git-ignored) or the CI secret store.
`.env.example` lists the names. Nothing secret is printed, logged or reported.

## Documents

Each app has `docs/<app>-flow.md` (screens, flows, sign-in and data, status),
and each feature has a context document and an approved test case list in
`docs/context/`.
