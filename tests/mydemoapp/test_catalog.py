import allure
import pytest

from src.actions.mydemoapp.catalog_actions import CatalogActions
from src.actions.mydemoapp.product_actions import ProductActions
from src.constants.mydemoapp.test_data import price_value

pytestmark = allure.feature("Catalogue")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CAT-P0-01 The catalogue shows products with a name and price")
def test_catalog_shows_products_with_name_and_price(app):
    catalog = CatalogActions(app)
    assert catalog.title() == "Products"
    names, prices = catalog.names(), catalog.prices()
    assert names, "no products shown"
    assert all(name.strip() for name in names), f"a product has no name: {names}"
    assert all(price.startswith("$") for price in prices), f"a price doesn't start with $: {prices}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-02 Sort by price, low to high")
def test_sort_by_price_ascending(app):
    catalog = CatalogActions(app)
    catalog.sort_by("price ascending")
    prices = [price_value(p) for p in catalog.prices()]
    assert prices == sorted(prices), f"prices not ascending: {prices}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-03 Sort by name, Z to A")
def test_sort_by_name_descending(app):
    catalog = CatalogActions(app)
    catalog.sort_by("name descending")
    names = catalog.names()
    assert names == sorted(names, reverse=True), f"names not descending: {names}"


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("PRD-P0-01 Opening a product shows its details")
def test_opening_a_product_shows_its_details(app):
    catalog = CatalogActions(app)
    name, price = catalog.first_product()
    catalog.open_first_product()
    product = ProductActions(app)
    assert product.name() == name
    assert product.price() == price
    assert product.quantity() == 1


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="Known defect: the minus button lowers the quantity to 0", strict=True)
@allure.title("PRD-P1-02 Quantity can go up and not below 1 (known defect)")
def test_quantity_goes_up_and_not_below_one(app):
    CatalogActions(app).open_first_product()
    product = ProductActions(app)
    product.increase(2)
    assert product.quantity() == 3
    product.decrease(3)
    assert product.quantity() == 1, "quantity went below 1"
