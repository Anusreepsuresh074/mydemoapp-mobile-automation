# Test cases: shopping journey (My Demo App, Android)

_Version 2, 2026-09-30, by mobile-test-design, from `docs/context/mydemoapp-shopping-context.md` and the exploratory sessions in `docs/exploratory/exploratory-sessions.md`. Version 1 (19 cases, 2026-09-29) is kept in git history._

**Readiness check: passed.** Starting state: a fresh app (signed out, empty cart). Sign-in: the demo account from `.env` / CI secrets. Every expected result below was observed on the live app or is a stated rule.

## How to read this

- **ID:** feature, priority, number. `CAT` catalogue, `PRD` product, `CRT` cart, `LGN` sign-in, `CHK` checkout, `APP` app state and phone behaviour.
- **Priority:** P0 = release-blocking, P1 = important, P2 = minor or unusual.
- **Type:** **Positive** (the right thing works), **Negative** (a wrong input or action is refused), **Edge** (limits, unusual states, the phone itself).
- **Found in:** `Design` = the first test design; `S1`–`S6` = the exploratory session that found it.
- **Status:** what the run should show today. A known defect is a strict xfail; a blocked case is skipped with its reason.
- Every case runs in `regression`; the P0 cases that pass also run in `smoke`.

## Catalogue (6)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAT-P0-01 | Positive | The catalogue shows products with a name and price | Fresh app | Open the app | "Products" title; products with a name and a price starting with "$" | R1 | Design | Pass expected |
| CAT-P1-02 | Positive | Sort by price, low to high, across all products | Fresh app | Sort → Price - Ascending, scroll to the end | All 24 prices in ascending order | R6 | Design; strengthened in S1 | Pass expected |
| CAT-P1-03 | Positive | Sort by name, Z to A, across all products | Fresh app | Sort → Name - Descending, scroll to the end | All 24 names in descending order | R6 | Design; strengthened in S1 | Pass expected |
| CAT-P1-04 | Positive | Sort by price, high to low, across all products | Fresh app | Sort → Price - Descending, scroll to the end | All 24 prices in descending order | R6 | S1 | Pass expected |
| CAT-P1-05 | Positive | Sort by name, A to Z, across all products | Fresh app | Sort → Name - Ascending, scroll to the end | All 24 names in ascending order | R6 | S1 | Pass expected |
| CAT-P2-06 | Edge | Scrolling to the end shows every product | Fresh app | Scroll the grid to the end | 24 different products, each with a price from $7.99 to $49.99 | R16 | S1 | Pass expected |

## Product (8)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRD-P0-01 | Positive | Opening a product shows its details | Fresh app | Tap the first product image | Same name and price as the catalogue; quantity 1 | R1, R2 | Design | Pass expected |
| PRD-P1-02 | Edge | Quantity can go up but not below 1 | Product open | Tap + twice, then − three times | Quantity 3, then 1 (never 0) | R2 | Design | Known defect D-02 (strict xfail) |
| PRD-P1-03 | Positive | + raises the quantity | Product open | Tap + three times | Quantity reads 4 | R2 | S2 | Pass expected |
| PRD-P2-04 | Edge | At quantity 0, Add to cart is disabled | Product open | Tap − once (reaches 0 because of D-02), tap Add to cart | Add to cart is disabled; no cart badge | R17 | S2 | Pass expected |
| PRD-P2-05 | Edge | A large quantity is accepted and priced right | Product open | Tap + 12 times, add to cart, open the cart | 13 Items; total = 13 × price | R2, R4 | S2 | Pass expected |
| PRD-P2-06 | Positive | Choosing a colour selects it | Product open | Tap Blue | The selection ring moves to Blue | R18 | S2 | Pass expected |
| PRD-P2-07 | Positive | Rating a product shows a thank-you message | Product open | Tap the 3rd star, then Continue | "Thank you for submitting your review!"; Continue closes it and the product stays open | R19 | S2 | Pass expected |
| PRD-P0-08 | Edge | Opening a second product after going back does not crash | Fresh app | Open product 1, press Back, open product 2 | Product 2's details open; the app keeps running | R1 | S3 | Known defect D-07 (strict xfail) |

## Cart (10)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CRT-P0-01 | Positive | Adding a product updates the cart | Product open | Add to cart, open the cart | Badge 1; the product, its price, "1 Items"; total = price | R3, R4 | Design | Pass expected |
| CRT-P1-02 | Positive | Adding quantity 2 updates count and total | Product open | Tap +, add to cart, open the cart | "2 Items"; total = 2 × price | R3, R4 | Design | Pass expected |
| CRT-P1-03 | Positive | Removing the only item empties the cart | One item in the cart | Remove Item | "No Items" and "Go Shopping"; no badge | R5 | Design | Pass expected |
| CRT-P2-04 | Edge | A restart empties the cart (observed behaviour) | One item in the cart | Kill and relaunch the app | No cart badge | R15 | Design | Pass expected |
| CRT-P1-05 | Edge | Adding the same product twice makes one row | Product open | Add to cart twice, open the cart | One row, quantity 2, "2 Items", total = 2 × price | R20 | S3 | Pass expected |
| CRT-P1-06 | Positive | + in the cart raises count, total and badge | One item in the cart | Tap + in the cart | Quantity 2, "2 Items", total = 2 × price, badge 2 | R21 | S3 | Pass expected |
| CRT-P1-07 | Positive | − in the cart lowers count, total and badge | Quantity 2 in the cart | Tap − in the cart | Quantity 1, "1 Items", total = price, badge 1 | R21 | S3 | Pass expected |
| CRT-P2-08 | Edge | − from 1 in the cart removes the item | One item in the cart | Tap − in the cart | "No Items"; no badge | R21 | S3 | Pass expected |
| CRT-P2-09 | Positive | Go Shopping returns to the catalogue | Empty cart open | Tap Go Shopping | The catalogue is shown | R5 | S3 | Pass expected |
| CRT-P1-10 | Positive | Two different products add up in the cart | Fresh app | Add product 1, go back, add product 2, open the cart | 2 rows; "2 Items"; total = both prices | R4 | S3 | **Blocked** by D-07 (skipped) |

## Sign-in (13)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LGN-P0-01 | Positive | The demo user can sign in | Login open | Sign in with TEST_USERNAME / TEST_PASSWORD | The menu shows Log Out | R7 | Design | Pass expected |
| LGN-P1-02 | Negative | Empty username is refused | Login open | Tap Login with both fields empty | "Username is required" | R8 | Design | Pass expected |
| LGN-P1-03 | Negative | Missing password is refused | Login open | Username only, tap Login | "Enter Password" | R8 | Design | Pass expected |
| LGN-P1-04 | Negative | The locked-out user is refused | Login open | Sign in as alice@example.com | "Sorry this user has been locked out."; still on Login | R9 | Design | Pass expected |
| LGN-P1-05 | Negative | An unknown user is refused | Login open | Sign in as nobody@example.com / wrong-password | Still on Login; not signed in | R10 | Design | Known defect D-01 (strict xfail) |
| LGN-P1-06 | Negative | The real user with a wrong password is refused | Login open | Sign in as TEST_USERNAME / wrong-password | Still on Login; not signed in | R10 | S4 | Known defect D-01 (strict xfail) |
| LGN-P2-07 | Negative | A username that is not an email is refused | Login open | Sign in as "bob" with the demo password | Still on Login with an error | R22 | S4 | Known defect D-04 (strict xfail) |
| LGN-P2-08 | Edge | A 300-character username does not crash the app | Login open | Sign in with a 300-character username | The app keeps running and shows a screen | R22 | S4 | Pass expected |
| LGN-P2-09 | Edge | Special characters in the username do not crash the app | Login open | Sign in as <script>'";--@x.com | The app keeps running and shows a screen | R22 | S4 | Pass expected |
| LGN-P1-10 | Positive | The password is hidden while typing | Login open | Look at the password field | It is a password (masked) field | R23 | S4 | Pass expected |
| LGN-P1-11 | Positive | Tapping a demo username fills the form | Login open | Tap bod@example.com, then Login | Both fields filled; signed in | R23 | S4 | Pass expected |
| LGN-P1-12 | Positive | Cancelling Log Out keeps you signed in | Signed in | Menu → Log Out → CANCEL | Still signed in (menu shows Log Out) | R24 | S4 | Pass expected |
| LGN-P1-13 | Positive | Log Out signs you out | Signed in | Menu → Log Out → LOGOUT | Login opens; the menu shows Log In | R24 | S4 | Pass expected |

## Checkout (17)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-P0-01 | Positive | A signed-in shopper can place an order | One item in the cart | Checkout → sign in → address → payment → review → Place Order | Review shows the product, name and address; "Checkout Complete" | R7, R11–R14 | Design | Pass expected |
| CHK-P0-02 | Negative | Checkout while signed out asks for sign-in | One item in the cart, signed out | Proceed To Checkout | The Login screen opens | R7 | Design | Pass expected |
| CHK-P1-03 | Negative | The empty address form shows every required error | Signed in, address form | Tap To Payment with nothing typed | An error under Full Name, Address Line 1, City, Zip Code and Country; still on the form | R11 | Design; strengthened in S5 | Pass expected |
| CHK-P1-04 | Positive | After an order the cart is empty | Order placed | Continue Shopping → open the cart | "No Items" | R14 | Design | Pass expected |
| CHK-P1-05 | Negative | Each required address field is needed (5 runs: name, address, city, zip, country) | Signed in, address form | Fill every field except one, tap To Payment | That field's error; still on the form | R11 | S5 | Pass expected |
| CHK-P2-06 | Negative | The country error message is complete | Signed in, address form | Leave Country empty, tap To Payment | "Please provide your country." | R11 | S5 | Known defect D-05 (strict xfail) |
| CHK-P1-07 | Positive | A signed-in shopper goes straight to the address form | Signed in, one item in the cart | Open the cart, Proceed To Checkout | The address form opens; no Login | R25 | S4 | Pass expected |
| CHK-P1-08 | Negative | An empty payment form is refused | Payment form | Tap Review Order with nothing typed | "Value looks invalid." errors; still on payment | R12 | S5 | Pass expected |
| CHK-P1-09 | Negative | A missing card holder name is refused | Payment form | Fill all but the name, tap Review Order | Name error; still on payment | R12 | S5 | Pass expected |
| CHK-P1-10 | Negative | A too-short card number is refused | Payment form | Card number 41111, rest valid | Error; still on payment | R12 | S5 | Known defect D-06 (strict xfail) |
| CHK-P1-11 | Negative | An expired card is refused | Payment form | Expiry 01/20, rest valid | Error; still on payment | R12 | S5 | Known defect D-06 (strict xfail) |
| CHK-P2-12 | Negative | An incomplete expiry date is refused | Payment form | Expiry "1", rest valid | Error; still on payment | R12 | S5 | Known defect D-06 (strict xfail) |
| CHK-P2-13 | Negative | A 1-digit security code is refused | Payment form | Security code 1, rest valid | Error; still on payment | R12 | S5 | Known defect D-06 (strict xfail) |
| CHK-P2-14 | Edge | The card number field refuses letters | Payment form | Type abcdabcdabcdabcd as the card number | The field stays empty | R12 | S5 | Pass expected |
| CHK-P1-15 | Positive | The review shows the order and a correct total | Quantity 2 in the cart, address and card filled | Reach the review | Address, card holder, DHL Standard Delivery $5.99, "2 Items", total = cart total + $5.99 | R13, R26 | S5 | Pass expected |
| CHK-P1-16 | Negative | The review hides the card number | At the review | Look at the payment method | The card number is masked (e.g. **** 1111) | R27 | S5 | Known defect D-08 (strict xfail) |
| CHK-P2-17 | Positive | The billing address can differ from shipping | Payment form | Untick "billing address is the same" | A second address form appears (it was ticked by default) | R28 | S5 | Pass expected |

## App state and phone behaviour (8)

| ID | Type | Scenario | Preconditions | Steps | Expected | Rule | Found in | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APP-P2-01 | Edge | Checkout survives going to the background | Address partly typed | Background the app for 3 s | Still on the address form, typed name kept | R29 | Design | Pass expected |
| APP-P2-02 | Edge | The product quantity survives going to the background | Product open, quantity 3 | Background the app for 3 s | Quantity still 3 | R29 | S6 | Pass expected |
| APP-P2-03 | Edge | The cart badge survives going to the background | One item in the cart | Background the app for 3 s | Badge still 1 | R29 | S6 | Pass expected |
| APP-P2-04 | Edge | The app stays upright when the phone is turned | Fresh app | Request landscape | The request is refused; the app stays in portrait and working | R30 | S6 | Pass expected |
| APP-P2-05 | Positive | Back from a product returns to the catalogue | Product open | Press the phone's Back button | The catalogue is shown | R31 | S6 | Pass expected |
| APP-P2-06 | Positive | Back from the cart returns to the catalogue | Cart open | Press the phone's Back button | The catalogue is shown | R31 | S6 | Pass expected |
| APP-P2-07 | Negative | Back with the menu open only closes the menu | Side menu open | Press the phone's Back button | The menu closes; the app stays open on the catalogue | R31 | S6 | Known defect D-03 (strict xfail) |
| APP-P2-08 | Edge | A restart signs the user out (observed behaviour) | Signed in | Kill and relaunch the app | The menu shows Log In | R24 | S4 | Pass expected |

## Totals

| | Count |
| --- | --- |
| Cases | **62** (CHK-P1-05 runs 5 times, once per required field, so 66 test runs) |
| By priority | P0 7 · P1 31 · P2 24 |
| By type | Positive 28 · Negative 18 · Edge 16 |
| Found by exploratory testing | 43 |
| Expected today | 49 pass · 12 known-defect xfails · 1 blocked |
| Smoke suite | 6: CAT-P0-01, PRD-P0-01, CRT-P0-01, LGN-P0-01, CHK-P0-01, CHK-P0-02 |

## Not automated

- Other menu features (WebView, QR code scanner, geo location, drawing, fingerprint, virtual USB, crash app): out of scope.
- The `visual@example.com` demo user: its purpose (a visual-testing user) needs screenshot comparison, not functional checks.
- Rating the product on the catalogue cards: the same stars as the product page (PRD-P2-07).

---
**Reviewed and approved on 2026-09-30** by the project owner, after the exploratory sessions. Handed to `mobile-test-automation`.
