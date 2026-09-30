"""Checkout, step 4: the order is complete."""

import allure

from src.pages.base_page import BasePage, by_id


class CheckoutCompletePage(BasePage):
    txt_complete = by_id("completeTV")
    txt_thank_you = by_id("thankYouTV")
    btn_continue_shopping = by_id("shoopingBt")

    def is_open(self) -> bool:
        return self.is_visible(self.txt_complete)

    def messages(self) -> tuple[str, str]:
        return self.text_of(self.txt_complete), self.text_of(self.txt_thank_you)

    @allure.step("Continue shopping")
    def continue_shopping(self) -> None:
        self.tap(self.btn_continue_shopping)
