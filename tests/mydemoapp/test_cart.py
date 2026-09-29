import allure
import pytest

from src.actions.mydemoapp.cart_actions import CartActions
from src.actions.mydemoapp.catalog_actions import CatalogActions
from src.constants.mydemoapp.test_data import price_value
from src.flows.mydemoapp.shopping_flows import add_first_product_to_cart

pytestmark = allure.feature("Cart")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CRT-P0-01 Adding a product updates the cart")
def test_adding_a_product_updates_the_cart(app):
    name, price = add_first_product_to_cart(app)
    catalog = CatalogActions(app)
    assert catalog.cart_badge() == "1"
    catalog.open_cart()
    cart = CartActions(app)
    assert cart.item_names() == [name]
    assert cart.item_price() == price
    assert cart.item_count() == "1 Items"
    assert price_value(cart.total()) == price_value(price)


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-02 Adding quantity 2 updates count and total")
def test_quantity_two_updates_count_and_total(app):
    _, price = add_first_product_to_cart(app, extra_quantity=1)
    CatalogActions(app).open_cart()
    cart = CartActions(app)
    assert cart.item_count() == "2 Items"
    assert price_value(cart.total()) == pytest.approx(2 * price_value(price))


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-03 Removing the only item empties the cart")
def test_removing_the_only_item_empties_the_cart(app):
    add_first_product_to_cart(app)
    catalog = CatalogActions(app)
    catalog.open_cart()
    cart = CartActions(app)
    cart.remove_first_item()
    assert cart.is_empty()
    assert catalog.cart_badge() is None, "the cart badge is still shown"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CRT-P2-04 A restart empties the cart (observed behaviour)")
def test_restart_empties_the_cart(app, settings):
    add_first_product_to_cart(app)
    assert CatalogActions(app).cart_badge() == "1"
    app.terminate_app(settings.app_package)
    app.activate_app(settings.app_package)
    assert CatalogActions(app).cart_badge() is None, "the cart kept its items after a restart"
