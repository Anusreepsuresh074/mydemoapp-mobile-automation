import allure
import pytest

from src.actions.mydemoapp.cart_actions import CartActions
from src.actions.mydemoapp.catalog_actions import CatalogActions
from src.actions.mydemoapp.checkout_actions import CheckoutActions
from src.actions.mydemoapp.login_actions import LoginActions
from src.constants.mydemoapp.test_data import ADDRESS, CARD
from src.core.config import credentials
from src.flows.mydemoapp.shopping_flows import add_first_product_to_cart, checkout_to_address_form, place_order

pytestmark = allure.feature("Checkout")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CHK-P0-01 A signed-in shopper can place an order")
def test_signed_in_shopper_can_place_an_order(app):
    name, _ = add_first_product_to_cart(app)
    checkout_to_address_form(app, *credentials())
    review = place_order(app, ADDRESS, CARD)
    assert review["heading"] == "Review your order"
    assert review["item"] == name
    assert review["full_name"] == ADDRESS["full_name"]
    assert review["address"] == ADDRESS["address_1"]
    assert review["card_holder"] == CARD["name"]
    assert CheckoutActions(app).completion_texts() == ("Checkout Complete", "Thank you for your order")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CHK-P0-02 Checkout while signed out asks for sign-in")
def test_checkout_while_signed_out_asks_for_sign_in(app):
    add_first_product_to_cart(app)
    CatalogActions(app).open_cart()
    CartActions(app).proceed_to_checkout()
    assert LoginActions(app).is_open()


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-03 The address form requires its fields")
def test_address_form_requires_its_fields(app):
    add_first_product_to_cart(app)
    checkout_to_address_form(app, *credentials())
    checkout = CheckoutActions(app)
    checkout.to_payment()
    assert checkout.address_errors() == [
        "Please provide your full name.",
        "Please provide your address.",
        "Please provide your city.",
    ]
    assert checkout.is_on_address_form()


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CHK-P1-04 After an order the cart is empty")
def test_cart_is_empty_after_an_order(app):
    add_first_product_to_cart(app)
    checkout_to_address_form(app, *credentials())
    place_order(app, ADDRESS, CARD)
    CheckoutActions(app).continue_shopping()
    CatalogActions(app).open_cart()
    assert CartActions(app).is_empty()


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-01 Checkout survives going to the background")
def test_checkout_survives_going_to_the_background(app):
    add_first_product_to_cart(app)
    checkout_to_address_form(app, *credentials())
    checkout = CheckoutActions(app)
    checkout.fill_address(ADDRESS)
    app.background_app(3)
    assert checkout.is_on_address_form()
    assert checkout.typed_full_name() == ADDRESS["full_name"]
