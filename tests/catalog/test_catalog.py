import allure
import pytest

from src.utils.money import price_value
from tests.catalog.catalog_td import HIGHEST_PRICE, LOWEST_PRICE, PRODUCT_COUNT

pytestmark = allure.feature("Catalogue")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("CAT-P0-01 The catalogue shows products with a name and price")
def test_catalog_shows_products_with_name_and_price(catalog):
    assert catalog.title() == "Products"
    products = catalog.visible_products()
    assert products, "no products shown"
    assert all(name.strip() for name, _ in products), f"a product has no name: {products}"
    assert all(price.startswith("$") for _, price in products), f"a price doesn't start with $: {products}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-02 Sort by price, low to high, across all products")
def test_sort_by_price_ascending(catalog):
    catalog.sort_by("price ascending")
    prices = [price_value(price) for _, price in catalog.all_products()]
    assert len(prices) == PRODUCT_COUNT
    assert prices == sorted(prices), f"prices not ascending: {prices}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-03 Sort by name, Z to A, across all products")
def test_sort_by_name_descending(catalog):
    catalog.sort_by("name descending")
    names = [name for name, _ in catalog.all_products()]
    assert len(names) == PRODUCT_COUNT
    assert names == sorted(names, reverse=True), f"names not descending: {names}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-04 Sort by price, high to low, across all products")
def test_sort_by_price_descending(catalog):
    catalog.sort_by("price descending")
    prices = [price_value(price) for _, price in catalog.all_products()]
    assert len(prices) == PRODUCT_COUNT
    assert prices == sorted(prices, reverse=True), f"prices not descending: {prices}"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("CAT-P1-05 Sort by name, A to Z, across all products")
def test_sort_by_name_ascending(catalog):
    catalog.sort_by("name ascending")
    names = [name for name, _ in catalog.all_products()]
    assert len(names) == PRODUCT_COUNT
    assert names == sorted(names), f"names not ascending: {names}"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("CAT-P2-06 Scrolling to the end shows every product")
def test_scrolling_shows_every_product(catalog):
    products = catalog.all_products()
    assert len(products) == PRODUCT_COUNT, f"expected {PRODUCT_COUNT} products, found {len(products)}"
    prices = [price_value(price) for _, price in products]
    assert min(prices) == LOWEST_PRICE
    assert max(prices) == HIGHEST_PRICE
