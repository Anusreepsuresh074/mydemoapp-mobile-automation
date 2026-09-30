import contextlib

import allure
import pytest
from selenium.common.exceptions import WebDriverException

from src.pages.catalog_page import CatalogPage
from tests.checkout.checkout_td import ADDRESS

pytestmark = allure.feature("App state")

BACKGROUND_SECONDS = 3


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-01 Checkout survives going to the background")
def test_checkout_survives_going_to_the_background(app, address_page):
    address_page.fill(ADDRESS)
    app.background_app(BACKGROUND_SECONDS)
    assert address_page.is_open()
    assert address_page.typed_full_name() == ADDRESS["full_name"]


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-02 The product quantity survives going to the background")
def test_product_quantity_survives_the_background(app, catalog):
    product = catalog.open_product(0)
    product.increase(2)
    app.background_app(BACKGROUND_SECONDS)
    assert product.is_open()
    assert product.quantity() == 3


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-03 The cart badge survives going to the background")
def test_cart_badge_survives_the_background(app, catalog, first_product_in_cart):
    app.background_app(BACKGROUND_SECONDS)
    assert catalog.header.cart_badge() == "1"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-04 The app stays upright when the phone is turned")
def test_app_stays_in_portrait(app, catalog):
    # The app is locked to portrait, so the request may be refused outright.
    with contextlib.suppress(WebDriverException):
        app.orientation = "LANDSCAPE"
    try:
        assert app.orientation == "PORTRAIT"
        assert catalog.is_open()
    finally:
        app.orientation = "PORTRAIT"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-05 Back from a product returns to the catalogue")
def test_back_from_a_product_returns_to_the_catalogue(catalog):
    product = catalog.open_product(0)
    product.go_back()
    assert catalog.is_open()
    assert catalog.app_is_in_foreground()


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-06 Back from the cart returns to the catalogue")
def test_back_from_the_cart_returns_to_the_catalogue(catalog):
    cart = catalog.header.open_cart()
    cart.go_back()
    assert catalog.is_open()
    assert catalog.app_is_in_foreground()


@pytest.mark.regression
@pytest.mark.p2
@pytest.mark.xfail(reason="D-03: Back with the side menu open closes the app", strict=True)
@allure.title("APP-P2-07 Back with the menu open only closes the menu (known defect D-03)")
def test_back_with_the_menu_open_only_closes_the_menu(catalog):
    menu = catalog.header.open_menu()
    assert menu.shows_log_in()
    menu.go_back()
    assert catalog.app_is_in_foreground(), "the app closed"
    assert catalog.is_open()
    assert not menu.shows_log_in(), "the menu is still open"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("APP-P2-08 A restart signs the user out (observed behaviour)")
def test_restart_signs_the_user_out(app, settings, signed_in):
    app.terminate_app(settings.app_package)
    app.activate_app(settings.app_package)
    catalog = CatalogPage(app)
    assert catalog.is_open()
    assert catalog.header.open_menu().shows_log_in(), "still signed in after a restart"
