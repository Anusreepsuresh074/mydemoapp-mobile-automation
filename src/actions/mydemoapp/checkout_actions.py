from src.screens.mydemoapp.checkout_screens import AddressScreen, CompleteScreen, PaymentScreen, ReviewScreen


class CheckoutActions:
    def __init__(self, driver):
        self.driver = driver
        self.address = AddressScreen(driver)
        self.payment = PaymentScreen(driver)
        self.review = ReviewScreen(driver)
        self.complete = CompleteScreen(driver)

    def _hide_keyboard(self) -> None:
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    def is_on_address_form(self) -> bool:
        return self.address.is_visible(AddressScreen.btn_to_payment) and self.address.is_visible(
            AddressScreen.input_full_name
        )

    def fill_address(self, data: dict) -> None:
        self.address.type_text(AddressScreen.input_full_name, data["full_name"])
        self.address.type_text(AddressScreen.input_address_1, data["address_1"])
        self.address.type_text(AddressScreen.input_city, data["city"])
        self.address.type_text(AddressScreen.input_zip, data["zip"])
        self.address.type_text(AddressScreen.input_country, data["country"])
        self._hide_keyboard()

    def typed_full_name(self) -> str:
        return self.address.text_of(AddressScreen.input_full_name)

    def to_payment(self) -> None:
        self._hide_keyboard()
        self.address.tap(AddressScreen.btn_to_payment)

    def address_errors(self) -> list[str]:
        return [
            self.address.text_of(AddressScreen.msg_full_name_error),
            self.address.text_of(AddressScreen.msg_address_error),
            self.address.text_of(AddressScreen.msg_city_error),
        ]

    def fill_card(self, card: dict) -> None:
        self.payment.type_text(PaymentScreen.input_card_name, card["name"])
        self.payment.type_text(PaymentScreen.input_card_number, card["number"])
        self.payment.type_text(PaymentScreen.input_expiry, card["expiry"])
        self.payment.type_text(PaymentScreen.input_security_code, card["security_code"])
        self._hide_keyboard()

    def to_review(self) -> None:
        self.payment.tap(PaymentScreen.btn_review_order)

    def review_details(self) -> dict:
        return {
            "heading": self.review.text_of(ReviewScreen.txt_heading),
            "item": self.review.text_of(ReviewScreen.txt_item_name),
            "full_name": self.review.text_of(ReviewScreen.txt_full_name),
            "address": self.review.text_of(ReviewScreen.txt_address),
            "card_holder": self.review.text_of(ReviewScreen.txt_card_holder),
        }

    def place_order(self) -> None:
        self.review.tap(ReviewScreen.btn_place_order)

    def completion_texts(self) -> tuple[str, str]:
        return self.complete.text_of(CompleteScreen.txt_complete), self.complete.text_of(CompleteScreen.txt_thank_you)

    def continue_shopping(self) -> None:
        self.complete.tap(CompleteScreen.btn_continue_shopping)
