# My Demo App (Android): flow document

_Created by create-mobile-framework-structure on 2026-09-29; screens and locators confirmed live by mobile-test-automation's walkthrough on 2026-09-29 (emulator `mydemo_api35`, Android 15, API 35); extended by the exploratory sessions and the Page Object Model rebuild on 2026-09-30._

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
| Product details | Tap a product image (`productIV`); tapping the name does not open it | `productTV` name, `priceTV`, `start1IV`–`start5IV` rating (then `sortTV` thank-you, `closeBt` Continue), `colorIV` colours (accessibility ids "Black color", "Blue color"…; `aroundIV` ring on the selected one), `minusIV` / `noTV` / `plusIV` quantity, `cartBt` "Add to cart" (disabled at quantity 0) |
| Cart | Tap `cartRL` | `productTV` "My Cart", `titleTV`, `priceTV`, `noTV` quantity, `plusIV` / `minusIV`, `removeBt` "Remove Item", `itemsTV` "1 Items", `totalPriceTV`, `cartBt` "Proceed To Checkout" |
| Empty cart | Cart with no items | `noItemTitleTV` "No Items", "Oh no! Your cart is empty…", `shoppingBt` "Go Shopping" |
| Menu | Tap `menuIV` (Log Out opens an Android dialog: `android:id/message`, `button2` CANCEL, `button1` LOGOUT) | `itemTV` rows: Catalog, WebView, QR Code Scanner, Geo Location, Drawing, About, Reset App State, FingerPrint, Virtual USB, Crash app (debug), Log In / Log Out |
| Login | Menu → Log In, or Proceed To Checkout while signed out | `nameET`, `passwordET`, `loginBtn`; errors `nameErrorTV`, `passwordErrorTV`; demo accounts listed (`username1TV` ...) |
| Checkout: address | Proceed To Checkout while signed in | `fullNameET`, `address1ET`, `address2ET`, `cityET`, `zipET`, `stateET`, `countryET`, `paymentBtn` "To Payment"; errors `fullNameErrorTV`, `address1ErrorTV`, `cityErrorTV`, `zipErrorTV`, `countryErrorTV` |
| Checkout: payment | "To Payment" with a valid address | `nameET`, `cardNumberET`, `expirationDateET`, `securityCodeET`, errors `nameErrorTV`, `expirationDateErrorTV`, `securityCodeErrorTV` ("Value looks invalid."), `billingAddressCB` (unticking shows a billing form with the address ids), `paymentBtn` "Review Order" |
| Checkout: review | "Review Order" with valid payment | "Review your order", `placeOrderRV` items, `fullNameTV`, `addressTV`, `cardHolderTV`, `itemNumberTV`, `totalAmountTV`, further down `cardNumberTV`, `dhlTV` "DHL Standard Delivery", `amountTV` "$5.99"; `paymentBtn` "Place Order" (same id as Review Order, so the heading identifies the screen) |
| Checkout: complete | "Place Order" | `completeTV` "Checkout Complete", `thankYouTV`, `shoopingBt` "Continue Shopping" |

**Quirks found in the walkthrough**

- Empty text fields report their **hint** as text (for example `fullNameET` reads "Rebecca Winter" when empty). Assertions on typed values must compare what was typed, and "empty" is checked with the `hint` attribute.
- Killing and relaunching the app **empties the cart** (an early note said the opposite; corrected after the first test run).
- The product quantity can be lowered to **0** with the − button (defect, see PRD-P1-02).
- The cart badge still shows the old count on the Checkout Complete screen, and clears once the catalogue opens.
- The review total adds **DHL Standard Delivery, $5.99**, shown further down the review (found in exploratory session S5).
- The catalogue shows 4 of its **24 products** per screen; a card's name and price can be split by the screen edge, so cards are read as (name, price) pairs while scrolling.
- Opening a product, going back and opening a **different** product **crashes the app** (D-07).
- The app is **locked to portrait**.

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
| CAT-P0-01 | The catalogue shows products with a name and price | Done: passing | `tests/catalog/test_catalog.py::test_catalog_shows_products_with_name_and_price` |
| CAT-P1-02 | Sort by price, low to high, across all products | Done: passing | `tests/catalog/test_catalog.py::test_sort_by_price_ascending` |
| CAT-P1-03 | Sort by name, Z to A, across all products | Done: passing | `tests/catalog/test_catalog.py::test_sort_by_name_descending` |
| CAT-P1-04 | Sort by price, high to low, across all products | Done: passing | `tests/catalog/test_catalog.py::test_sort_by_price_descending` |
| CAT-P1-05 | Sort by name, A to Z, across all products | Done: passing | `tests/catalog/test_catalog.py::test_sort_by_name_ascending` |
| CAT-P2-06 | Scrolling to the end shows every product | Done: passing | `tests/catalog/test_catalog.py::test_scrolling_shows_every_product` |
| PRD-P0-01 | Opening a product shows its details | Done: passing | `tests/product/test_product.py::test_opening_a_product_shows_its_details` |
| PRD-P1-02 | Quantity can go up but not below 1 | Done: known defect D-02, strict xfail | `tests/product/test_product.py::test_quantity_goes_up_and_not_below_one` |
| PRD-P1-03 | + raises the quantity | Done: passing | `tests/product/test_product.py::test_plus_raises_the_quantity` |
| PRD-P2-04 | At quantity 0, Add to cart is disabled | Done: passing | `tests/product/test_product.py::test_add_to_cart_is_disabled_at_quantity_zero` |
| PRD-P2-05 | A large quantity is accepted and priced right | Done: passing | `tests/product/test_product.py::test_large_quantity_is_priced_right` |
| PRD-P2-06 | Choosing a colour selects it | Done: passing | `tests/product/test_product.py::test_choosing_a_colour_selects_it` |
| PRD-P2-07 | Rating a product shows a thank-you message | Done: passing | `tests/product/test_product.py::test_rating_a_product_shows_thanks` |
| PRD-P0-08 | Opening a second product after going back does not crash | Done: known defect D-07, strict xfail | `tests/product/test_product.py::test_opening_a_second_product_after_going_back` |
| CRT-P0-01 | Adding a product updates the cart | Done: passing | `tests/cart/test_cart.py::test_adding_a_product_updates_the_cart` |
| CRT-P1-02 | Adding quantity 2 updates count and total | Done: passing | `tests/cart/test_cart.py::test_quantity_two_updates_count_and_total` |
| CRT-P1-03 | Removing the only item empties the cart | Done: passing | `tests/cart/test_cart.py::test_removing_the_only_item_empties_the_cart` |
| CRT-P2-04 | A restart empties the cart (observed behaviour) | Done: passing | `tests/cart/test_cart.py::test_restart_empties_the_cart` |
| CRT-P1-05 | Adding the same product twice makes one row | Done: passing | `tests/cart/test_cart.py::test_same_product_twice_makes_one_row` |
| CRT-P1-06 | + in the cart raises count, total and badge | Done: passing | `tests/cart/test_cart.py::test_plus_in_cart_raises_count_total_and_badge` |
| CRT-P1-07 | − in the cart lowers count, total and badge | Done: passing | `tests/cart/test_cart.py::test_minus_in_cart_lowers_count_total_and_badge` |
| CRT-P2-08 | − from 1 in the cart removes the item | Done: passing | `tests/cart/test_cart.py::test_minus_from_one_removes_the_item` |
| CRT-P2-09 | Go Shopping returns to the catalogue | Done: passing | `tests/cart/test_cart.py::test_go_shopping_returns_to_the_catalogue` |
| CRT-P1-10 | Two different products add up in the cart | Blocked by D-07 (skipped) | `tests/cart/test_cart.py::test_two_different_products_add_up` |
| LGN-P0-01 | The demo user can sign in | Done: passing | `tests/login/test_login.py::test_demo_user_can_sign_in` |
| LGN-P1-02 | Empty username is refused | Done: passing | `tests/login/test_login.py::test_empty_username_is_refused` |
| LGN-P1-03 | Missing password is refused | Done: passing | `tests/login/test_login.py::test_missing_password_is_refused` |
| LGN-P1-04 | The locked-out user is refused | Done: passing | `tests/login/test_login.py::test_locked_out_user_is_refused` |
| LGN-P1-05 | An unknown user is refused | Done: known defect D-01, strict xfail | `tests/login/test_login.py::test_unknown_user_is_refused` |
| LGN-P1-06 | The real user with a wrong password is refused | Done: known defect D-01, strict xfail | `tests/login/test_login.py::test_wrong_password_is_refused` |
| LGN-P2-07 | A username that is not an email is refused | Done: known defect D-04, strict xfail | `tests/login/test_login.py::test_username_that_is_not_an_email_is_refused` |
| LGN-P2-08 | A 300-character username does not crash the app | Done: passing | `tests/login/test_login.py::test_long_username_does_not_crash` |
| LGN-P2-09 | Special characters in the username do not crash the app | Done: passing | `tests/login/test_login.py::test_special_characters_username_does_not_crash` |
| LGN-P1-10 | The password is hidden while typing | Done: passing | `tests/login/test_login.py::test_password_is_masked` |
| LGN-P1-11 | Tapping a demo username fills the form | Done: passing | `tests/login/test_login.py::test_tapping_a_demo_username_fills_the_form` |
| LGN-P1-12 | Cancelling Log Out keeps you signed in | Done: passing | `tests/login/test_login.py::test_cancelling_log_out_keeps_you_signed_in` |
| LGN-P1-13 | Log Out signs you out | Done: passing | `tests/login/test_login.py::test_log_out_signs_you_out` |
| CHK-P0-01 | A signed-in shopper can place an order | Done: passing | `tests/checkout/test_checkout.py::test_signed_in_shopper_can_place_an_order` |
| CHK-P0-02 | Checkout while signed out asks for sign-in | Done: passing | `tests/checkout/test_checkout.py::test_checkout_while_signed_out_asks_for_sign_in` |
| CHK-P1-03 | The empty address form shows every required error | Done: passing | `tests/checkout/test_checkout.py::test_empty_address_form_shows_every_required_error` |
| CHK-P1-04 | After an order the cart is empty | Done: passing | `tests/checkout/test_checkout.py::test_cart_is_empty_after_an_order` |
| CHK-P1-05 | Each required address field is needed (5 runs: name, address, city, zip, country) | Done: passing | `tests/checkout/test_checkout.py::test_each_required_address_field_is_needed` |
| CHK-P2-06 | The country error message is complete | Done: known defect D-05, strict xfail | `tests/checkout/test_checkout.py::test_country_error_message_is_complete` |
| CHK-P1-07 | A signed-in shopper goes straight to the address form | Done: passing | `tests/checkout/test_checkout.py::test_signed_in_shopper_goes_straight_to_the_address_form` |
| CHK-P1-08 | An empty payment form is refused | Done: passing | `tests/checkout/test_checkout.py::test_empty_payment_form_is_refused` |
| CHK-P1-09 | A missing card holder name is refused | Done: passing | `tests/checkout/test_checkout.py::test_missing_card_holder_name_is_refused` |
| CHK-P1-10 | A too-short card number is refused | Done: known defect D-06, strict xfail | `tests/checkout/test_checkout.py::test_invalid_card_details_are_refused` [CHK-P1-10-…] |
| CHK-P1-11 | An expired card is refused | Done: known defect D-06, strict xfail | `tests/checkout/test_checkout.py::test_invalid_card_details_are_refused` [CHK-P1-11-…] |
| CHK-P2-12 | An incomplete expiry date is refused | Done: known defect D-06, strict xfail | `tests/checkout/test_checkout.py::test_invalid_card_details_are_refused` [CHK-P2-12-…] |
| CHK-P2-13 | A 1-digit security code is refused | Done: known defect D-06, strict xfail | `tests/checkout/test_checkout.py::test_invalid_card_details_are_refused` [CHK-P2-13-…] |
| CHK-P2-14 | The card number field refuses letters | Done: passing | `tests/checkout/test_checkout.py::test_card_number_field_refuses_letters` |
| CHK-P1-15 | The review shows the order and a correct total | Done: passing | `tests/checkout/test_checkout.py::test_review_shows_the_order_and_a_correct_total` |
| CHK-P1-16 | The review hides the card number | Done: known defect D-08, strict xfail | `tests/checkout/test_checkout.py::test_review_hides_the_card_number` |
| CHK-P2-17 | The billing address can differ from shipping | Done: passing | `tests/checkout/test_checkout.py::test_billing_address_can_differ_from_shipping` |
| APP-P2-01 | Checkout survives going to the background | Done: passing | `tests/app_state/test_app_state.py::test_checkout_survives_going_to_the_background` |
| APP-P2-02 | The product quantity survives going to the background | Done: passing | `tests/app_state/test_app_state.py::test_product_quantity_survives_the_background` |
| APP-P2-03 | The cart badge survives going to the background | Done: passing | `tests/app_state/test_app_state.py::test_cart_badge_survives_the_background` |
| APP-P2-04 | The app stays upright when the phone is turned | Done: passing | `tests/app_state/test_app_state.py::test_app_stays_in_portrait` |
| APP-P2-05 | Back from a product returns to the catalogue | Done: passing | `tests/app_state/test_app_state.py::test_back_from_a_product_returns_to_the_catalogue` |
| APP-P2-06 | Back from the cart returns to the catalogue | Done: passing | `tests/app_state/test_app_state.py::test_back_from_the_cart_returns_to_the_catalogue` |
| APP-P2-07 | Back with the menu open only closes the menu | Done: known defect D-03, strict xfail | `tests/app_state/test_app_state.py::test_back_with_the_menu_open_only_closes_the_menu` |
| APP-P2-08 | A restart signs the user out (observed behaviour) | Done: passing | `tests/app_state/test_app_state.py::test_restart_signs_the_user_out` |

Last full run on 2026-09-30: 53 passed, 12 xfailed (known defects), 1 skipped (blocked by D-07), in 1130 s; smoke: 6 passed in 91 s.
