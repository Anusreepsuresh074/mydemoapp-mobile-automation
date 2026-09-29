"""Journeys across screens. Flows use actions only (docs/framework-rules.md)."""

from src.actions.mydemoapp.cart_actions import CartActions
from src.actions.mydemoapp.catalog_actions import CatalogActions
from src.actions.mydemoapp.checkout_actions import CheckoutActions
from src.actions.mydemoapp.login_actions import LoginActions
from src.actions.mydemoapp.menu_actions import MenuActions
from src.actions.mydemoapp.product_actions import ProductActions


def add_first_product_to_cart(driver, extra_quantity: int = 0) -> tuple[str, str]:
    """Open the first product, optionally raise its quantity, add it; returns its (name, price)."""
    CatalogActions(driver).open_first_product()
    product = ProductActions(driver)
    name, price = product.name(), product.price()
    product.increase(extra_quantity)
    product.add_to_cart()
    return name, price


def sign_in_from_menu(driver, username: str, password: str) -> None:
    menu = MenuActions(driver)
    menu.open()
    menu.choose_log_in()
    LoginActions(driver).log_in(username, password)


def checkout_to_address_form(driver, username: str, password: str) -> None:
    """From a filled cart: open the cart, proceed, and sign in when asked."""
    CatalogActions(driver).open_cart()
    CartActions(driver).proceed_to_checkout()
    LoginActions(driver).log_in(username, password)


def place_order(driver, address: dict, card: dict) -> dict:
    """From the address form to the complete screen; returns what the review screen showed."""
    checkout = CheckoutActions(driver)
    checkout.fill_address(address)
    checkout.to_payment()
    checkout.fill_card(card)
    checkout.to_review()
    review = checkout.review_details()
    checkout.place_order()
    return review
