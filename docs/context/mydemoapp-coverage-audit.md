# Coverage audit: My Demo App (Android)

_Version 2, 2026-09-30, by mobile-coverage-audit, comparing `docs/context/mydemoapp-shopping-context.md` (31 rules), `docs/context/mydemoapp-shopping-testcases.md` (62 cases) and `docs/exploratory/exploratory-sessions.md`._

## Summary

**No blocking gaps.** 31 of 31 rules have at least one case; every in-scope screen appears in a case; every P0 journey that passes is in `smoke`. Case types: positive 28, negative 18, edge 16; 43 cases came from exploratory testing.

Known limits: a cart with two **different** products (R4) can't be reached because of the crash D-07, so CRT-P1-10 is blocked; totals are covered with one product at quantities 2 and 13.

## Rules

| Rule | What it says | Cases | Result |
| --- | --- | --- | --- |
| R1 | The catalogue lists products with name and price; tapping the image op… | CAT-P0-01, PRD-P0-01, PRD-P0-08 | covered (defects D-07) |
| R2 | A product opens with quantity 1; + and − change it. Assumption: it can… | PRD-P0-01, PRD-P1-02, PRD-P1-03, PRD-P2-05 | covered (defects D-02) |
| R3 | Adding to cart sets the cart badge to the number of items | CRT-P0-01, CRT-P1-02 | covered |
| R4 | The cart shows each item, the item count and the total price | PRD-P2-05, CRT-P0-01, CRT-P1-02, CRT-P1-10 | covered (defects D-07) |
| R5 | "Remove Item" removes it; an empty cart shows "No Items" and "Go Shopp… | CRT-P1-03, CRT-P2-09 | covered |
| R6 | Sorting offers name A–Z, name Z–A, price low–high, price high–low | CAT-P1-02, CAT-P1-03, CAT-P1-04, CAT-P1-05 | covered |
| R7 | Checkout requires sign-in | LGN-P0-01, CHK-P0-01, CHK-P0-02 | covered |
| R8 | Login: empty username gives "Username is required"; missing password g… | LGN-P1-02, LGN-P1-03 | covered |
| R9 | The locked-out demo user gets "Sorry this user has been locked out." | LGN-P1-04 | covered |
| R10 | Assumption: unknown usernames or wrong passwords are refused | LGN-P1-05, LGN-P1-06 | covered (defects D-01) |
| R11 | Address: full name, address line 1, city, zip and country are required… | CHK-P0-01, CHK-P1-03, CHK-P1-05, CHK-P2-06 | covered (defects D-05) |
| R12 | Payment: card holder name, card number, expiry date and security code … | CHK-P0-01, CHK-P1-08, CHK-P1-09, CHK-P1-10, CHK-P1-11, CHK-P2-12, CHK-P2-13, CHK-P2-14 | covered (defects D-06) |
| R13 | The review shows the items, the address, the card holder and a total | CHK-P0-01, CHK-P1-15 | covered |
| R14 | Placing the order shows "Checkout Complete" and empties the cart | CHK-P0-01, CHK-P1-04 | covered |
| R15 | Killing and relaunching the app empties the cart | CRT-P2-04 | covered |
| R16 | The catalogue holds 24 products, $7.99 to $49.99; 4 show per screen | CAT-P2-06 | covered |
| R17 | At quantity 0, Add to cart is disabled | PRD-P2-04 | covered |
| R18 | A product has 4 colours; tapping one selects it | PRD-P2-06 | covered |
| R19 | Tapping a rating star shows "Thank you for submitting your review!" wi… | PRD-P2-07 | covered |
| R20 | Adding the same product again raises that row's quantity instead of ad… | CRT-P1-05 | covered |
| R21 | The cart's + and − change the quantity, count, total and badge; − from… | CRT-P1-06, CRT-P1-07, CRT-P2-08 | covered |
| R22 | Assumption: the username must be an email address | LGN-P2-07, LGN-P2-08, LGN-P2-09 | covered (defects D-04) |
| R23 | The password field is masked; tapping a listed demo username fills the… | LGN-P1-10, LGN-P1-11 | covered |
| R24 | Log Out asks for confirmation (CANCEL / LOGOUT) and then opens Login; … | LGN-P1-12, LGN-P1-13, APP-P2-08 | covered |
| R25 | A signed-in shopper goes from the cart straight to the address form | CHK-P1-07 | covered |
| R26 | The review adds DHL Standard Delivery, $5.99, to the cart total | CHK-P1-15 | covered |
| R27 | Assumption: the review masks the card number | CHK-P1-16 | covered (defects D-08) |
| R28 | "Billing address is the same as shipping" is ticked by default; untick… | CHK-P2-17 | covered |
| R29 | Going to the background keeps the current screen and what was typed | APP-P2-01, APP-P2-02, APP-P2-03 | covered |
| R30 | The app is locked to portrait | APP-P2-04 | covered |
| R31 | The phone's Back button returns from a product or the cart to the cata… | APP-P2-05, APP-P2-06, APP-P2-07 | covered (defects D-03) |

## Screens

| Screen | Cases |
| --- | --- |
| Catalogue and sort sheet | CAT-P0-01 to CAT-P2-06, APP-P2-04 to APP-P2-06 |
| Product details | PRD-P0-01 to PRD-P0-08, APP-P2-02 |
| Cart and empty cart | CRT-P0-01 to CRT-P2-09, APP-P2-03, APP-P2-06 |
| Menu and Log Out dialog | LGN-P0-01, LGN-P1-12, LGN-P1-13, APP-P2-07, APP-P2-08 |
| Login | LGN-P0-01 to LGN-P1-11, CHK-P0-02 |
| Checkout: address | CHK-P1-03, CHK-P1-05, CHK-P2-06, CHK-P1-07, APP-P2-01 |
| Checkout: payment | CHK-P1-08 to CHK-P2-14, CHK-P2-17 |
| Checkout: review | CHK-P0-01, CHK-P1-15, CHK-P1-16 |
| Checkout: complete | CHK-P0-01, CHK-P1-04 |

## Categories

Positive, negative and edge cases exist for every feature. Phone behaviour covered: background, rotation (portrait lock), the Back button, restart. Not applicable: network failure (the app makes no network calls for shopping) and permissions (the shopping journey asks for none).

## Open questions

- Two-product cart: re-test CRT-P1-10 once D-07 is fixed.
- Payment validation: the expected rules (card length, expiry in the future, 3–4 digit code) are assumptions; confirm with a product owner in a real project.
