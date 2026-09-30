import allure
import pytest

from src.pages.catalog_page import CatalogPage
from src.pages.checkout_address_page import CheckoutAddressPage
from src.pages.checkout_complete_page import CheckoutCompletePage
from src.pages.checkout_payment_page import CheckoutPaymentPage
from src.pages.checkout_review_page import CheckoutReviewPage
from src.pages.login_page import LoginPage
from src.utils.money import price_value
from tests.checkout.checkout_td import (
    ADDRESS,
    CARD,
    DELIVERY,
    MISSING_ADDRESS_FIELD,
    PAYMENT_ERROR,
    REQUIRED_ADDRESS_ERRORS,
)

pytestmark = allure.feature("Checkout")


def _place_order(app, address_page) -> dict:
    """From the address form to Checkout Complete; returns what the review screen showed."""
    address_page.fill(ADDRESS)
    address_page.to_payment()
    payment = CheckoutPaymentPage(app)
    payment.fill(CARD)
    payment.to_review()
    review = CheckoutReviewPage(app)
    details = review.details()
    review.place_order()
    return details


def _submit_card(app, payment_page, card: dict) -> CheckoutReviewPage:
    payment_page.fill(card)
    payment_page.to_review()
    return CheckoutReviewPage(app)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CHK-P0-01 A signed-in shopper can place an order")
def test_signed_in_shopper_can_place_an_order(app, first_product_in_cart, address_page):
    name, _ = first_product_in_cart
    review = _place_order(app, address_page)
    assert review["heading"] == "Review your order"
    assert review["item"] == name
    assert review["full_name"] == ADDRESS["full_name"]
    assert review["address"] == ADDRESS["address_1"]
    assert review["card_holder"] == CARD["name"]
    assert CheckoutCompletePage(app).messages() == ("Checkout Complete", "Thank you for your order")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CHK-P0-02 Checkout while signed out asks for sign-in")
def test_checkout_while_signed_out_asks_for_sign_in(app, catalog, first_product_in_cart):
    catalog.header.open_cart().proceed_to_checkout()
    assert LoginPage(app).is_open()


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-03 The empty address form shows every required error")
def test_empty_address_form_shows_every_required_error(address_page):
    address_page.to_payment()
    errors = address_page.errors()
    assert set(errors) == set(REQUIRED_ADDRESS_ERRORS), f"errors shown: {errors}"
    assert address_page.is_open()


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-04 After an order the cart is empty")
def test_cart_is_empty_after_an_order(app, address_page):
    _place_order(app, address_page)
    CheckoutCompletePage(app).continue_shopping()
    assert CatalogPage(app).header.open_cart().is_empty()


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.parametrize("missing", MISSING_ADDRESS_FIELD)
@allure.title("CHK-P1-05 Each required address field is needed: {missing}")
def test_each_required_address_field_is_needed(app, address_page, missing):
    address_page.fill({key: value for key, value in ADDRESS.items() if key != missing})
    address_page.to_payment()
    errors = address_page.errors()
    assert list(errors) == [missing], f"expected an error only for {missing}, got {errors}"
    assert address_page.is_open()
    assert not CheckoutPaymentPage(app).is_open(timeout=5)


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.xfail(reason="D-05: the country error reads 'Please provide your'", strict=True)
@allure.title("CHK-P2-06 The country error message is complete (known defect D-05)")
def test_country_error_message_is_complete(address_page):
    address_page.fill({key: value for key, value in ADDRESS.items() if key != "country"})
    address_page.to_payment()
    assert address_page.errors().get("country") == REQUIRED_ADDRESS_ERRORS["country"]


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-07 A signed-in shopper goes straight to the address form")
def test_signed_in_shopper_goes_straight_to_the_address_form(app, signed_in):
    signed_in.open_product(0).add_to_cart()
    signed_in.header.open_cart().proceed_to_checkout()
    assert CheckoutAddressPage(app).is_open()
    assert not LoginPage(app).is_open(timeout=5), "Login was shown although the shopper is signed in"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-08 An empty payment form is refused")
def test_empty_payment_form_is_refused(app, payment_page):
    payment_page.to_review()
    errors = payment_page.errors()
    assert errors, "no payment errors shown"
    assert set(errors.values()) == {PAYMENT_ERROR}, f"errors shown: {errors}"
    assert payment_page.is_open()
    assert not CheckoutReviewPage(app).is_open(timeout=5)


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-09 A missing card holder name is refused")
def test_missing_card_holder_name_is_refused(app, payment_page):
    review = _submit_card(app, payment_page, {key: value for key, value in CARD.items() if key != "name"})
    assert payment_page.errors() == {"name": PAYMENT_ERROR}
    assert not review.is_open(timeout=5)


@pytest.mark.regression
@pytest.mark.parametrize(
    "card_change",
    [
        pytest.param({"number": "41111"}, id="CHK-P1-10-card-number-too-short", marks=pytest.mark.p1),
        pytest.param({"expiry": "0120"}, id="CHK-P1-11-expired-card", marks=pytest.mark.p1),
        pytest.param({"expiry": "1"}, id="CHK-P2-12-incomplete-expiry", marks=pytest.mark.p2),
        pytest.param({"security_code": "1"}, id="CHK-P2-13-one-digit-security-code", marks=pytest.mark.p2),
    ],
)
@pytest.mark.xfail(reason="D-06: card details are not validated", strict=True)
@allure.title("CHK-P1-10..P2-13 Invalid card details are refused (known defect D-06): {card_change}")
def test_invalid_card_details_are_refused(app, payment_page, card_change):
    review = _submit_card(app, payment_page, {**CARD, **card_change})
    assert not review.is_open(timeout=5), f"the review opened with invalid card details {card_change}"
    assert payment_page.errors(), "no error shown"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CHK-P2-14 The card number field refuses letters")
def test_card_number_field_refuses_letters(app, payment_page):
    payment_page.fill({"number": "abcdabcdabcdabcd"})
    typed = payment_page.typed("number")
    assert not typed.startswith("abcd"), f"letters were typed into the card number: {typed}"
    review = _submit_card(app, payment_page, {key: value for key, value in CARD.items() if key != "number"})
    assert not review.is_open(timeout=5), "the review opened without a card number"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-15 The review shows the order and a correct total")
def test_review_shows_the_order_and_a_correct_total(app, catalog, test_user):
    product = catalog.open_product(0)
    product.increase(1)
    product.add_to_cart()
    cart = product.header.open_cart()
    cart_total = price_value(cart.total())
    cart.proceed_to_checkout()
    LoginPage(app).log_in(*test_user)
    address = CheckoutAddressPage(app)
    address.fill(ADDRESS)
    address.to_payment()
    review = _submit_card(app, CheckoutPaymentPage(app), CARD)
    assert review.is_open()
    details = review.details()
    assert details["full_name"] == ADDRESS["full_name"]
    assert details["address"] == ADDRESS["address_1"]
    assert details["card_holder"] == CARD["name"]
    assert review.item_count() == "2 Items"
    delivery_name, delivery_price = review.delivery()
    assert (delivery_name, delivery_price) == DELIVERY
    assert price_value(review.total()) == pytest.approx(cart_total + price_value(delivery_price))


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="D-08: the review shows the full card number", strict=True)
@allure.title("CHK-P1-16 The review hides the card number (known defect D-08)")
def test_review_hides_the_card_number(app, payment_page):
    review = _submit_card(app, payment_page, CARD)
    assert review.is_open()
    shown = review.card_number_shown().replace(" ", "")
    assert CARD["number"] not in shown, f"the full card number is shown: {shown}"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CHK-P2-17 The billing address can differ from shipping")
def test_billing_address_can_differ_from_shipping(payment_page):
    assert payment_page.billing_same_is_ticked(), "the box should be ticked by default"
    assert not payment_page.billing_form_is_shown()
    payment_page.toggle_billing_same()
    assert not payment_page.billing_same_is_ticked()
    assert payment_page.billing_form_is_shown(), "no billing address form after unticking"
