"""Checkout, step 4: the order is complete."""

import allure

from src.pages.base_page import DEFAULT_TIMEOUT, BasePage, by_id


class CheckoutCompletePage(BasePage):
    txt_complete = by_id("completeTV")
    txt_thank_you = by_id("thankYouTV")
    btn_continue_shopping = by_id("shoopingBt")

    def is_open(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """True when this screen is showing; pass a short timeout when checking that it is NOT."""
        return self.is_visible(self.txt_complete, timeout)

    def messages(self) -> tuple[str, str]:
        return self.text_of(self.txt_complete), self.text_of(self.txt_thank_you)

    @allure.step("Continue shopping")
    def continue_shopping(self) -> None:
        self.tap(self.btn_continue_shopping)
