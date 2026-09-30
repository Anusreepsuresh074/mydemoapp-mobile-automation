"""The cart, filled or empty."""

import allure

from src.pages.base_page import BasePage, by_id
from src.pages.components.header_bar import HeaderBar


class CartPage(BasePage):
    txt_item_name = by_id("titleTV")
    txt_item_price = by_id("priceTV")
    txt_item_quantity = by_id("noTV")
    btn_remove = by_id("removeBt")
    btn_plus = by_id("plusIV")
    btn_minus = by_id("minusIV")
    txt_item_count = by_id("itemsTV")
    txt_total = by_id("totalPriceTV")
    btn_checkout = by_id("cartBt")
    txt_empty_title = by_id("noItemTitleTV")
    btn_go_shopping = by_id("shoppingBt")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderBar(driver)

    def item_names(self) -> list[str]:
        return self.texts_of(self.txt_item_name)

    def item_price(self) -> str:
        return self.text_of(self.txt_item_price)

    def item_quantities(self) -> list[str]:
        return self.texts_of(self.txt_item_quantity)

    def item_count(self) -> str:
        return self.text_of(self.txt_item_count)

    def total(self) -> str:
        return self.text_of(self.txt_total)

    def is_empty(self) -> bool:
        return self.is_visible(self.txt_empty_title) and self.is_visible(self.btn_go_shopping)

    @allure.step("Tap + on the first item")
    def increase_first_item(self) -> None:
        self.tap(self.btn_plus)

    @allure.step("Tap - on the first item")
    def decrease_first_item(self) -> None:
        self.tap(self.btn_minus)

    @allure.step("Go shopping")
    def go_shopping(self) -> None:
        self.tap(self.btn_go_shopping)

    @allure.step("Remove the first item")
    def remove_first_item(self) -> None:
        self.tap(self.btn_remove)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        """Leads to Login when signed out, or to the address form when signed in."""
        self.tap(self.btn_checkout)
