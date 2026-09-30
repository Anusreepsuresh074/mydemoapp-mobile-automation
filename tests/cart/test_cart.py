import allure
import pytest

from src.pages.catalog_page import CatalogPage
from src.utils.money import price_value

pytestmark = allure.feature("Cart")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CRT-P0-01 Adding a product updates the cart")
def test_adding_a_product_updates_the_cart(catalog, first_product_in_cart):
    name, price = first_product_in_cart
    assert catalog.header.cart_badge() == "1"
    cart = catalog.header.open_cart()
    assert cart.item_names() == [name]
    assert cart.item_price() == price
    assert cart.item_count() == "1 Items"
    assert price_value(cart.total()) == price_value(price)


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-02 Adding quantity 2 updates count and total")
def test_quantity_two_updates_count_and_total(catalog):
    _, price = catalog.first_product()
    product = catalog.open_product(0)
    product.increase(1)
    product.add_to_cart()
    cart = product.header.open_cart()
    assert cart.item_count() == "2 Items"
    assert price_value(cart.total()) == pytest.approx(2 * price_value(price))


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-03 Removing the only item empties the cart")
def test_removing_the_only_item_empties_the_cart(catalog, first_product_in_cart):
    cart = catalog.header.open_cart()
    cart.remove_first_item()
    assert cart.is_empty()
    assert cart.header.cart_badge() is None, "the cart badge is still shown"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CRT-P2-04 A restart empties the cart (observed behaviour)")
def test_restart_empties_the_cart(app, settings, catalog, first_product_in_cart):
    assert catalog.header.cart_badge() == "1"
    app.terminate_app(settings.app_package)
    app.activate_app(settings.app_package)
    assert CatalogPage(app).header.cart_badge() is None, "the cart kept its items after a restart"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-05 Adding the same product twice makes one row")
def test_same_product_twice_makes_one_row(catalog):
    name, price = catalog.first_product()
    product = catalog.open_product(0)
    product.add_to_cart()
    product.add_to_cart()
    assert product.header.cart_badge() == "2"
    cart = product.header.open_cart()
    assert cart.item_names() == [name], "the product appears in more than one row"
    assert cart.item_quantities() == ["2"]
    assert cart.item_count() == "2 Items"
    assert price_value(cart.total()) == pytest.approx(2 * price_value(price))


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-06 + in the cart raises count, total and badge")
def test_plus_in_cart_raises_count_total_and_badge(catalog, first_product_in_cart):
    _, price = first_product_in_cart
    cart = catalog.header.open_cart()
    cart.increase_first_item()
    assert cart.item_quantities() == ["2"]
    assert cart.item_count() == "2 Items"
    assert price_value(cart.total()) == pytest.approx(2 * price_value(price))
    assert cart.header.cart_badge() == "2"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CRT-P1-07 - in the cart lowers count, total and badge")
def test_minus_in_cart_lowers_count_total_and_badge(catalog):
    _, price = catalog.first_product()
    product = catalog.open_product(0)
    product.increase(1)
    product.add_to_cart()
    cart = product.header.open_cart()
    assert cart.item_count() == "2 Items"
    cart.decrease_first_item()
    assert cart.item_quantities() == ["1"]
    assert cart.item_count() == "1 Items"
    assert price_value(cart.total()) == pytest.approx(price_value(price))
    assert cart.header.cart_badge() == "1"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CRT-P2-08 - from 1 in the cart removes the item")
def test_minus_from_one_removes_the_item(catalog, first_product_in_cart):
    cart = catalog.header.open_cart()
    cart.decrease_first_item()
    assert cart.is_empty()
    assert cart.header.cart_badge() is None


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CRT-P2-09 Go Shopping returns to the catalogue")
def test_go_shopping_returns_to_the_catalogue(catalog):
    cart = catalog.header.open_cart()
    assert cart.is_empty()
    cart.go_shopping()
    assert catalog.is_open()


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.skip(reason="Blocked by D-07: opening a second product after going back crashes the app")
@allure.title("CRT-P1-10 Two different products add up in the cart (blocked by D-07)")
def test_two_different_products_add_up(catalog):
    first_name, first_price = catalog.first_product()
    catalog.open_product(0).add_to_cart()
    catalog.go_back()
    second_name = catalog.product_names()[1]
    second = catalog.open_product(1)
    second_price = second.price()
    second.add_to_cart()
    cart = second.header.open_cart()
    assert sorted(cart.item_names()) == sorted([first_name, second_name])
    assert cart.item_count() == "2 Items"
    assert price_value(cart.total()) == pytest.approx(price_value(first_price) + price_value(second_price))
