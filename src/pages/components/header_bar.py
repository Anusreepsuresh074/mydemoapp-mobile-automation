"""The top bar shown on most screens: the menu button, the logo and the cart with its badge."""

import allure

from src.pages.base_page import BasePage, by_id


class HeaderBar(BasePage):
    btn_menu = by_id("menuIV")
    btn_cart = by_id("cartRL")
    txt_cart_badge = by_id("cartTV")

    def cart_badge(self) -> str | None:
        """The number on the cart icon, or None when the cart is empty and no badge is shown."""
        if not self.is_visible(self.txt_cart_badge, timeout=2):
            return None
        return self.text_of(self.txt_cart_badge)

    @allure.step("Open the side menu")
    def open_menu(self):
        from src.pages.components.side_menu import SideMenu

        self.tap(self.btn_menu)
        return SideMenu(self.driver)

    @allure.step("Open the cart")
    def open_cart(self):
        from src.pages.cart_page import CartPage

        self.tap(self.btn_cart)
        return CartPage(self.driver)
