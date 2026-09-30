# Exploratory Testing Sessions: My Demo App (Android)

_Session-based exploratory testing on 2026-09-30, by Anusree P, on the local emulator `mydemo_api35` (Pixel 6, Android 15 / API 35), app 2.3.0 (build 27). The app was driven through Appium, with screenshots, UI dumps and the device crash log as evidence._

Exploratory testing is unscripted: each session has a **charter** (a mission) and notes on what was tried and found. Every important finding became a test case in [`../context/mydemoapp-shopping-testcases.md`](../context/mydemoapp-shopping-testcases.md) (the "Found in" column).

## Summary

| Session | Charter | Bugs found |
|---|---|---|
| S1 | Catalogue: how many products, and does every sort order hold across the whole list? | none (a gap in the old sort tests) |
| S2 | Product page: rating, colours, quantity limits | D-02 re-confirmed |
| S3 | Cart: same product twice, two products, cart +/−, emptying | D-07 (crash) |
| S4 | Sign-in and sign-out with unusual input | D-04; D-01 extended |
| S5 | Checkout: every required field, payment validation, review | D-05, D-06, D-08 |
| S6 | Phone behaviour: Back button, background, rotation, restart | D-03 |

## S1: Catalogue

**Charter:** explore the product list to learn how many products exist and whether sorting holds for the whole list, not only the first screen.

- The grid shows 4 products per screen; scrolling to the end finds **24 products** (Backpacks, Bike Light, Bolt T-Shirts, Fleece Jackets, Onesie, Test.allTheThings() T-Shirts), prices from $7.99 to $49.99.
- All 4 sort orders (name A–Z, name Z–A, price low–high, price high–low) are correct across all 24 products.
- **Test gap found:** the existing sort tests only checked the 4 products on screen. The name and price of a card can also be on different sides of the screen edge, so lists of names and prices read separately can get out of step. The new catalogue page object reads each card as a (name, price) pair and scrolls to the end.

## S2: Product page

**Charter:** explore every control on the product page.

- Tapping a rating star shows "Thank you for submitting your review!" with a **Continue** button that closes it ([screenshot](screenshots/rating-thank-you-dialog.png)).
- Four colours (black, blue, gray, green); tapping one moves the selection ring to it.
- There is no upper quantity limit (13 was accepted and priced correctly in the cart).
- **D-02 re-confirmed:** the minus button lowers the quantity to 0. At 0, **Add to cart is disabled**, so nothing can be added ([screenshot](screenshots/quantity-zero-add-disabled.png)).

## S3: Cart

**Charter:** explore the cart with more than one item.

- Adding the same product twice gives **one row with quantity 2** and the right total ($59.98).
- The cart's own + and − update the quantity, the "N Items" count, the total and the badge; − from 1 removes the item and empties the cart.
- "Go Shopping" on the empty cart returns to the catalogue.
- **D-07, crash:** open a product, go back to the catalogue (phone Back), then open a **different** product: the app closes. Reproduced 2 of 2 times; via Menu → Catalog it crashed 1 of 3 times; re-opening the **same** product does not crash. The device crash log shows a `NullPointerException` in `ProductCatalogFragment.java:156` ([log](d07-crash-log.txt), [screenshot](screenshots/d07-crash-home-screen.png)).
- Because of D-07, a cart with **two different products** cannot be reached reliably; that case is recorded as **blocked**.

## S4: Sign-in and sign-out

**Charter:** explore the login form with unusual input, and the sign-out path.

- The login screen lists 3 demo users that fill the form when tapped (`bod@example.com` with its password, `alice@example.com (locked out)`, `visual@example.com`). The password field is masked.
- **D-01 extended:** besides an unknown user, the app also accepts the real user with a **wrong password**, the username in UPPERCASE, and the username with spaces around it.
- **D-04:** a username that is not an email (`bob`), a 300-character username and one with special characters (`<script>'";--@x.com`) are all accepted and sign the user in. The app did not crash on any of them.
- An empty username with a password shows "Username is required".
- Log Out asks "Are you sure you want to logout" with **CANCEL** (stays signed in) and **LOGOUT** (signs out and opens Login; the menu then shows Log In).
- A signed-in shopper goes straight from the cart to the address form.
- A restart signs the user out.

## S5: Checkout

**Charter:** find every validation rule in checkout and check what the review shows.

- Address: **Full Name, Address Line 1, City, Zip Code and Country are required** (marked `*`); Address Line 2 and State/Region are optional. Leaving any one required field empty blocks To Payment and shows its own error.
- **D-05:** the country error reads "Please provide your", with the word "country" missing on screen too ([screenshot](screenshots/d05-country-error-cut-off.png)). The zip error ("Please provide your zip") also has no full stop, unlike the others.
- Payment: submitting it empty shows "Value looks invalid." under the name, expiry and security code, and stays on payment. A missing card holder name is refused. The card number field refuses letters.
- **D-06:** a 5-digit card number, a 1-digit security code, an expired date (01/20) and an incomplete date ("1") are all accepted and lead to the review.
- The review shows the item, "N Items", the delivery address, the card holder, **DHL Standard Delivery $5.99**, and a total equal to the cart total plus $5.99 ($59.98 + $5.99 = $65.97).
- **D-08, security:** the review shows the **full card number** in plain text ([screenshot](screenshots/d08-review-full-card-number.png)); it should be masked, e.g. `**** 1111`.
- "Billing address is the same as shipping" is ticked by default; unticking it shows a second address form.
- The review's Place Order button shares its resource id (`paymentBtn`) with the payment screen's Review Order button, so "the review is open" is checked with the review heading, not the button.

## S6: Phone behaviour

**Charter:** explore what the phone itself can do to the app.

- Back from a product or from the cart returns to the catalogue; Back from the catalogue leaves the app (normal Android behaviour).
- **D-03:** Back while the side menu is open **closes the whole app** instead of the menu (3 of 3 times) ([screenshot of the open menu](screenshots/side-menu-open.png)).
- Sending the app to the background for 3 s keeps the product quantity, the cart badge and a half-filled address form.
- The app is **locked to portrait** (`screenOrientation=portrait` in its manifest); a rotation request is refused and the app stays upright.

## Bugs found

| ID | Severity | Summary | Session |
|---|---|---|---|
| D-07 | **Critical** | Opening a second product after returning to the catalogue crashes the app | S3 |
| D-08 | High (security) | The review screen shows the full card number | S5 |
| D-06 | High | Card details are not validated (short number, 1-digit code, expired or incomplete date) | S5 |
| D-04 | Medium | Any text is accepted as a username (no email format check) | S4 |
| D-03 | Medium | Back with the side menu open closes the app | S6 |
| D-05 | Low | The country error message is cut off ("Please provide your") | S5 |

D-01 (any credentials accepted) and D-02 (quantity reaches 0) were found earlier and re-confirmed.
