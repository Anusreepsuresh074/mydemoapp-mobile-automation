# My Demo App (Android): flow document

_Created by create-mobile-framework-structure on 2026-09-29; screens and locators confirmed live by mobile-test-automation's walkthrough on 2026-09-29 (emulator `mydemo_api35`, Android 15, API 35)._

## Build

| Field | Value |
| --- | --- |
| Source | GitHub release of [saucelabs/my-demo-app-android](https://github.com/saucelabs/my-demo-app-android/releases) (`scripts/fetch-build.sh`) |
| File | `builds/mydemoapp-2.3.0-27.apk` (git-ignored) |
| Package | `com.saucelabs.mydemoapp.android` (checked with `aapt dump badging`) |
| Version | 2.3.0 (version code 27), min SDK 21 |
| Launch activity | `.view.activities.SplashActivity` |
| App type | Native Android (resource ids on every key element) |
| Fetched | 2026-09-29 |

## Screens (confirmed live)

All ids are `com.saucelabs.mydemoapp.android:id/<id>`.

| Screen | How you get there | Key elements (id) |
| --- | --- | --- |
| Catalogue | App start | `productTV` "Products", `productRV` list, `productIV` image, `titleTV` name, `priceTV` price, `sortIV` sort, `cartRL` cart, `cartTV` cart badge, `menuIV` menu |
| Sort sheet | Tap `sortIV` | `nameAscCL`, `nameDesCL`, `priceAscCL`, `priceDesCL` |
| Product details | Tap a product image (`productIV`); tapping the name does not open it | `productTV` name, `priceTV`, `colorIV` colours, `minusIV` / `noTV` / `plusIV` quantity, `cartBt` "Add to cart" |
| Cart | Tap `cartRL` | `productTV` "My Cart", `titleTV`, `priceTV`, `noTV` quantity, `plusIV` / `minusIV`, `removeBt` "Remove Item", `itemsTV` "1 Items", `totalPriceTV`, `cartBt` "Proceed To Checkout" |
| Empty cart | Cart with no items | `noItemTitleTV` "No Items", "Oh no! Your cart is empty…", `shoppingBt` "Go Shopping" |
| Menu | Tap `menuIV` | `itemTV` rows: Catalog, WebView, QR Code Scanner, Geo Location, Drawing, About, Reset App State, FingerPrint, Virtual USB, Crash app (debug), Log In / Log Out |
| Login | Menu → Log In, or Proceed To Checkout while signed out | `nameET`, `passwordET`, `loginBtn`; errors `nameErrorTV`, `passwordErrorTV`; demo accounts listed (`username1TV` ...) |
| Checkout: address | Proceed To Checkout while signed in | `fullNameET`, `address1ET`, `address2ET`, `cityET`, `zipET`, `stateET`, `countryET`, `paymentBtn` "To Payment"; errors `fullNameErrorTV`, `address1ErrorTV`, `cityErrorTV`, icons `zipIV`, `countryIV` |
| Checkout: payment | "To Payment" with a valid address | `nameET`, `cardNumberET`, `expirationDateET`, `securityCodeET`, `billingAddressCB`, `paymentBtn` "Review Order" |
| Checkout: review | "Review Order" with valid payment | "Review your order", `placeOrderRV` items, `fullNameTV`, `addressTV`, `cardHolderTV`, `itemNumberTV`, `totalAmountTV`, `paymentBtn` "Place Order" |
| Checkout: complete | "Place Order" | `completeTV` "Checkout Complete", `thankYouTV`, `shoopingBt` "Continue Shopping" |

**Quirks found in the walkthrough**

- Empty text fields report their **hint** as text (for example `fullNameET` reads "Rebecca Winter" when empty). Assertions on typed values must compare what was typed, and "empty" is checked with the `hint` attribute.
- Killing and relaunching the app **empties the cart** (an early note said the opposite; corrected after the first test run).
- The product quantity can be lowered to **0** with the − button (defect, see PRD-P1-02).
- The cart badge still shows the old count on the Checkout Complete screen, and clears once the catalogue opens.
- The review total was $35.98 for one $29.99 item; the $5.99 difference is not shown on the review screen.

## Sign-in and data

| Topic | Decision (get-mobile-auth, mobile-test-data) |
| --- | --- |
| Sign-in method | Username + password only (no one-time code, no single sign-on) |
| Test account | The app's own demo account `bod@example.com`, shown on its login screen. Still read from `TEST_USERNAME` / `TEST_PASSWORD` (`.env` locally, GitHub secrets in CI), never hardcoded |
| Other accounts | `alice@example.com` (locked out, for the negative case) |
| Test data | Built into the app: the catalogue and accounts ship with it; there is no backend to seed |
| Reset | Every test clears app data (`mobile: clearApp`) and relaunches, so each test starts signed out with an empty cart |

## Flow status

| Case ID | Flow | Status | Test |
| --- | --- | --- | --- |
| CAT-P0-01 | The catalogue shows products with a name and price | Done: passing | `tests/mydemoapp/test_catalog.py::test_catalog_shows_products_with_name_and_price` |
| CAT-P1-02 | Sort by price, low to high | Done: passing | `tests/mydemoapp/test_catalog.py::test_sort_by_price_ascending` |
| CAT-P1-03 | Sort by name, Z to A | Done: passing | `tests/mydemoapp/test_catalog.py::test_sort_by_name_descending` |
| PRD-P0-01 | Opening a product shows its details | Done: passing | `tests/mydemoapp/test_catalog.py::test_opening_a_product_shows_its_details` |
| PRD-P1-02 | Quantity can go up and not below 1 | Done: known defect, strict xfail | `tests/mydemoapp/test_catalog.py::test_quantity_goes_up_and_not_below_one` |
| CRT-P0-01 | Adding a product updates the cart | Done: passing | `tests/mydemoapp/test_cart.py::test_adding_a_product_updates_the_cart` |
| CRT-P1-02 | Adding quantity 2 updates count and total | Done: passing | `tests/mydemoapp/test_cart.py::test_quantity_two_updates_count_and_total` |
| CRT-P1-03 | Removing the only item empties the cart | Done: passing | `tests/mydemoapp/test_cart.py::test_removing_the_only_item_empties_the_cart` |
| CRT-P2-04 | A restart empties the cart (observed behaviour) | Done: passing | `tests/mydemoapp/test_cart.py::test_restart_empties_the_cart` |
| LGN-P0-01 | The demo user can sign in | Done: passing | `tests/mydemoapp/test_login.py::test_demo_user_can_sign_in` |
| LGN-P1-02 | Empty username is refused | Done: passing | `tests/mydemoapp/test_login.py::test_empty_username_is_refused` |
| LGN-P1-03 | Missing password is refused | Done: passing | `tests/mydemoapp/test_login.py::test_missing_password_is_refused` |
| LGN-P1-04 | The locked-out user is refused | Done: passing | `tests/mydemoapp/test_login.py::test_locked_out_user_is_refused` |
| LGN-P1-05 | Wrong credentials are refused | Done: known defect, strict xfail | `tests/mydemoapp/test_login.py::test_wrong_credentials_are_refused` |
| CHK-P0-01 | A signed-in shopper can place an order | Done: passing | `tests/mydemoapp/test_checkout.py::test_signed_in_shopper_can_place_an_order` |
| CHK-P0-02 | Checkout while signed out asks for sign-in | Done: passing | `tests/mydemoapp/test_checkout.py::test_checkout_while_signed_out_asks_for_sign_in` |
| CHK-P1-03 | The address form requires its fields | Done: passing | `tests/mydemoapp/test_checkout.py::test_address_form_requires_its_fields` |
| CHK-P1-04 | After an order the cart is empty | Done: passing | `tests/mydemoapp/test_checkout.py::test_cart_is_empty_after_an_order` |
| APP-P2-01 | Checkout survives going to the background | Done: passing | `tests/mydemoapp/test_checkout.py::test_checkout_survives_going_to_the_background` |

Last full run on 2026-09-29: 17 passed, 2 xfailed (the known defects), twice in a row.
