"""Checkout, step 2: card details."""

import allure

from src.pages.base_page import BasePage, by_id


class CheckoutPaymentPage(BasePage):
    input_card_name = by_id("nameET")
    input_card_number = by_id("cardNumberET")
    input_expiry = by_id("expirationDateET")
    input_security_code = by_id("securityCodeET")
    chk_billing_same = by_id("billingAddressCB")
    btn_review_order = by_id("paymentBtn")
    msg_card_name_error = by_id("nameErrorTV")
    msg_card_number_error = by_id("cardNumberErrorTV")
    msg_expiry_error = by_id("expirationDateErrorTV")
    msg_security_code_error = by_id("securityCodeErrorTV")
    # The billing form reuses the shipping form's ids; it only exists while the checkbox is unticked.
    input_billing_full_name = by_id("fullNameET")

    FIELDS = {
        "name": input_card_name,
        "number": input_card_number,
        "expiry": input_expiry,
        "security_code": input_security_code,
    }

    def is_open(self) -> bool:
        return self.is_visible(self.input_card_number)

    ERRORS = {
        "name": msg_card_name_error,
        "number": msg_card_number_error,
        "expiry": msg_expiry_error,
        "security_code": msg_security_code_error,
    }

    def errors(self) -> dict[str, str]:
        shown = {}
        for key, locator in self.ERRORS.items():
            elements = self.driver.find_elements(*locator)
            if elements and elements[0].text:
                shown[key] = elements[0].text
        return shown

    def typed(self, field: str) -> str:
        """What a field holds; an empty field reports its grey hint text, so compare with care."""
        return self.text_of(self.FIELDS[field])

    def billing_same_is_ticked(self) -> bool:
        return self.attribute_of(self.chk_billing_same, "checked") == "true"

    @allure.step("Toggle 'billing address is the same as shipping'")
    def toggle_billing_same(self) -> None:
        self.tap(self.chk_billing_same)

    def billing_form_is_shown(self) -> bool:
        return self.is_visible(self.input_billing_full_name, timeout=3)

    @allure.step("Fill the card details")
    def fill(self, card: dict) -> None:
        for key, value in card.items():
            self.type_text(self.FIELDS[key], value)
        self.hide_keyboard()

    @allure.step("Tap Review Order")
    def to_review(self) -> None:
        self.hide_keyboard()
        self.tap(self.btn_review_order)
