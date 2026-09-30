"""Session set-up: memory guard, one Appium session, a clean app per test, shared journeys, failure attachments."""

import allure
import pytest

from src.core.config import Settings, credentials
from src.core.driver import create_driver
from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.checkout_address_page import CheckoutAddressPage
from src.pages.checkout_payment_page import CheckoutPaymentPage
from src.pages.login_page import LoginPage
from tests.checkout.checkout_td import ADDRESS


def _available_memory_mb() -> int:
    with open("/proc/meminfo") as meminfo:
        for line in meminfo:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) // 1024
    return 0


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.load()


@pytest.fixture(scope="session", autouse=True)
def _memory_guard(settings):
    """Fail at once on a starved machine instead of failing randomly later (create-mobile-framework-structure)."""
    available = _available_memory_mb()
    if available and available < settings.min_available_memory_mb:
        pytest.exit(f"Only {available} MB memory available; need {settings.min_available_memory_mb} MB.", returncode=3)


@pytest.fixture(scope="session")
def driver(settings):
    session = create_driver(settings)
    yield session
    session.quit()


@pytest.fixture
def app(driver, settings):
    """A fresh app for every test: clear its data, then launch it (mobile-teardown's "cheap sign-in" strategy)."""
    driver.terminate_app(settings.app_package)
    driver.execute_script("mobile: clearApp", {"appId": settings.app_package})
    driver.activate_app(settings.app_package)
    return driver


@pytest.fixture
def test_user() -> tuple[str, str]:
    """The app's demo account (username, password), from the environment only."""
    return credentials()


@pytest.fixture
def catalog(app) -> CatalogPage:
    """A fresh app on its first screen, the catalogue."""
    page = CatalogPage(app)
    assert page.is_open(), "the app did not open on the catalogue"
    return page


@pytest.fixture
def signed_in(catalog, test_user) -> CatalogPage:
    """Signed in as the demo user through the menu, back on the catalogue."""
    catalog.header.open_menu().choose_log_in().log_in(*test_user)
    assert catalog.is_open(), "the catalogue did not come back after signing in"
    return catalog


@pytest.fixture
def first_product_in_cart(catalog) -> tuple[str, str]:
    """The first product added to the cart once; returns its (name, price)."""
    name, price = catalog.first_product()
    catalog.open_product(0).add_to_cart()
    return name, price


@pytest.fixture
def address_page(app, first_product_in_cart, test_user) -> CheckoutAddressPage:
    """Signed in at the checkout address form, with the first product in the cart."""
    cart: CartPage = CatalogPage(app).header.open_cart()
    cart.proceed_to_checkout()
    LoginPage(app).log_in(*test_user)
    page = CheckoutAddressPage(app)
    assert page.is_open(), "the address form did not open after signing in"
    return page


@pytest.fixture
def payment_page(app, address_page) -> CheckoutPaymentPage:
    """At the payment form, with a valid shipping address entered."""
    address_page.fill(ADDRESS)
    address_page.to_payment()
    page = CheckoutPaymentPage(app)
    assert page.is_open(), "the payment form did not open"
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "app" in item.fixturenames:
        driver = item.funcargs.get("app")
        if driver is not None:
            allure.attach(driver.get_screenshot_as_png(), "screenshot", allure.attachment_type.PNG)
            allure.attach(driver.page_source, "page source", allure.attachment_type.XML)
