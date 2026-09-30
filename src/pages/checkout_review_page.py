"""Checkout, step 3: review the order before placing it."""

import allure

from src.pages.base_page import BasePage, by_id


class CheckoutReviewPage(BasePage):
    txt_heading = by_id("enterShippingAddressTV")
    txt_item_name = by_id("titleTV")
    txt_full_name = by_id("fullNameTV")
    txt_address = by_id("addressTV")
    txt_card_holder = by_id("cardHolderTV")
    txt_card_number = by_id("cardNumberTV")
    txt_delivery_name = by_id("dhlTV")
    txt_delivery_price = by_id("amountTV")
    txt_item_count = by_id("itemNumberTV")
    txt_total = by_id("totalAmountTV")
    btn_place_order = by_id("paymentBtn")

    def is_open(self) -> bool:
        # Place Order shares its id with the payment screen's Review Order button, so the heading decides.
        return self.is_visible(self.txt_heading, timeout=5)

    def details(self) -> dict:
        return {
            "heading": self.text_of(self.txt_heading),
            "item": self.text_of(self.txt_item_name),
            "full_name": self.text_of(self.txt_full_name),
            "address": self.text_of(self.txt_address),
            "card_holder": self.text_of(self.txt_card_holder),
        }

    def item_count(self) -> str:
        return self.text_of(self.txt_item_count)

    def total(self) -> str:
        return self.text_of(self.txt_total)

    def card_number_shown(self) -> str:
        self.scroll_to(self.txt_card_number)
        return self.text_of(self.txt_card_number)

    def delivery(self) -> tuple[str, str]:
        """(delivery method, its price), further down the review."""
        self.scroll_to(self.txt_delivery_price)
        return self.text_of(self.txt_delivery_name), self.text_of(self.txt_delivery_price)

    @allure.step("Place the order")
    def place_order(self) -> None:
        self.tap(self.btn_place_order)
