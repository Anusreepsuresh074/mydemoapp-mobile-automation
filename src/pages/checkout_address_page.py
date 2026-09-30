"""Checkout, step 1: the shipping address form."""

import allure

from src.pages.base_page import BasePage, by_id


class CheckoutAddressPage(BasePage):
    input_full_name = by_id("fullNameET")
    input_address_1 = by_id("address1ET")
    input_address_2 = by_id("address2ET")
    input_city = by_id("cityET")
    input_state = by_id("stateET")
    input_zip = by_id("zipET")
    input_country = by_id("countryET")
    btn_to_payment = by_id("paymentBtn")
    msg_full_name_error = by_id("fullNameErrorTV")
    msg_address_error = by_id("address1ErrorTV")
    msg_city_error = by_id("cityErrorTV")
    msg_zip_error = by_id("zipErrorTV")
    msg_country_error = by_id("countryErrorTV")

    FIELDS = {
        "full_name": input_full_name,
        "address_1": input_address_1,
        "address_2": input_address_2,
        "city": input_city,
        "state": input_state,
        "zip": input_zip,
        "country": input_country,
    }

    def is_open(self) -> bool:
        return self.is_visible(self.btn_to_payment) and self.is_visible(self.input_full_name)

    @allure.step("Fill the shipping address")
    def fill(self, address: dict) -> None:
        """Types every field present in `address` (keys as in FIELDS); missing keys stay empty."""
        for key, value in address.items():
            self.type_text(self.FIELDS[key], value)
        self.hide_keyboard()

    def typed_full_name(self) -> str:
        return self.text_of(self.input_full_name)

    @allure.step("Tap To Payment")
    def to_payment(self) -> None:
        self.hide_keyboard()
        self.tap(self.btn_to_payment)

    ERRORS = {
        "full_name": msg_full_name_error,
        "address_1": msg_address_error,
        "city": msg_city_error,
        "zip": msg_zip_error,
        "country": msg_country_error,
    }

    def errors(self) -> dict[str, str]:
        """The error shown under each required field, by field key; fields without an error are left out."""
        shown = {}
        for key, locator in self.ERRORS.items():
            elements = self.driver.find_elements(*locator)
            if elements and elements[0].text:
                shown[key] = elements[0].text
        return shown
