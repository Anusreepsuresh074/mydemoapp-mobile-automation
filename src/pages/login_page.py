"""Login."""

import allure

from src.pages.base_page import DEFAULT_TIMEOUT, BasePage, by_id


class LoginPage(BasePage):
    txt_title = by_id("loginTV")
    input_username = by_id("nameET")
    input_password = by_id("passwordET")
    btn_login = by_id("loginBtn")
    msg_username_error = by_id("nameErrorTV")
    msg_password_error = by_id("passwordErrorTV")
    lnk_demo_user = by_id("username1TV")

    def is_open(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """True when this screen is showing; pass a short timeout when checking that it is NOT."""
        return self.is_visible(self.btn_login, timeout)

    @allure.step("Log in as {username}")
    def log_in(self, username: str, password: str) -> None:
        """Types only the fields given (an empty string leaves that field empty), then taps Login."""
        if username:
            self.type_text(self.input_username, username)
        if password:
            self.type_text(self.input_password, password)
        self.hide_keyboard()
        self.tap(self.btn_login)

    def password_is_masked(self) -> bool:
        return self.attribute_of(self.input_password, "password") == "true"

    def typed_username(self) -> str:
        return self.text_of(self.input_username)

    def password_is_filled(self) -> bool:
        return bool(self.text_of(self.input_password))

    def demo_username(self) -> str:
        return self.text_of(self.lnk_demo_user)

    @allure.step("Tap the listed demo username")
    def use_demo_user(self) -> None:
        self.tap(self.lnk_demo_user)

    @allure.step("Tap Login")
    def submit(self) -> None:
        self.hide_keyboard()
        self.tap(self.btn_login)

    def username_error(self) -> str:
        return self.text_of(self.msg_username_error)

    def password_error(self) -> str:
        return self.text_of(self.msg_password_error)
