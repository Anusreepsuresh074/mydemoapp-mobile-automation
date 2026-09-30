"""Product details: name, price, quantity and Add to cart."""

import allure

from src.pages.base_page import DEFAULT_TIMEOUT, BasePage, by_accessibility_id, by_id
from src.pages.components.header_bar import HeaderBar


class ProductPage(BasePage):
    txt_name = by_id("productTV")
    txt_price = by_id("priceTV")
    btn_minus = by_id("minusIV")
    txt_quantity = by_id("noTV")
    btn_plus = by_id("plusIV")
    btn_add_to_cart = by_id("cartBt")
    icn_selected_colour = by_id("aroundIV")
    txt_review_thanks = by_id("sortTV")
    btn_review_continue = by_id("closeBt")

    @staticmethod
    def btn_colour(colour: str):
        """A colour swatch by its label, e.g. "Blue"."""
        return by_accessibility_id(f"{colour} color")

    @staticmethod
    def btn_star(number: int):
        return by_id(f"start{number}IV")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderBar(driver)

    def is_open(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """True when this screen is showing; pass a short timeout when checking that it is NOT."""
        return self.is_visible(self.btn_add_to_cart, timeout)

    def name(self) -> str:
        return self.text_of(self.txt_name)

    def price(self) -> str:
        return self.text_of(self.txt_price)

    def quantity(self) -> int:
        return int(self.text_of(self.txt_quantity))

    @allure.step("Tap + {times} time(s)")
    def increase(self, times: int = 1) -> None:
        for _ in range(times):
            self.tap(self.btn_plus)

    @allure.step("Tap - {times} time(s)")
    def decrease(self, times: int = 1) -> None:
        for _ in range(times):
            self.tap(self.btn_minus)

    def add_to_cart_enabled(self) -> bool:
        return self.attribute_of(self.btn_add_to_cart, "enabled") == "true"

    @allure.step("Choose colour {colour}")
    def choose_colour(self, colour: str) -> None:
        self.tap(self.btn_colour(colour))

    def selected_colour_is(self, colour: str) -> bool:
        """True when the selection ring sits around this colour's swatch."""
        ring = self.find(self.icn_selected_colour).rect
        swatch = self.find(self.btn_colour(colour)).rect
        ring_centre = (ring["x"] + ring["width"] / 2, ring["y"] + ring["height"] / 2)
        swatch_centre = (swatch["x"] + swatch["width"] / 2, swatch["y"] + swatch["height"] / 2)
        return abs(ring_centre[0] - swatch_centre[0]) < 5 and abs(ring_centre[1] - swatch_centre[1]) < 5

    @allure.step("Rate the product {stars} star(s)")
    def rate(self, stars: int) -> None:
        self.tap(self.btn_star(stars))

    def review_thanks(self) -> str:
        return self.text_of(self.txt_review_thanks)

    @allure.step("Close the review message")
    def close_review_message(self) -> None:
        self.tap(self.btn_review_continue)

    @allure.step("Press Add to cart, even while it is disabled")
    def press_add_to_cart(self) -> None:
        """For checking a disabled button does nothing; add_to_cart() waits for it to be enabled."""
        self.find(self.btn_add_to_cart).click()

    @allure.step("Add to cart")
    def add_to_cart(self) -> None:
        self.tap(self.btn_add_to_cart)
