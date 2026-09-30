"""The side menu. Its rows share one resource id, so each row is found by its visible text."""

import allure

from src.pages.base_page import BasePage, by_android_id, by_id_and_text


class SideMenu(BasePage):
    lnk_catalog = by_id_and_text("itemTV", "Catalog")
    lnk_log_in = by_id_and_text("itemTV", "Log In")
    lnk_log_out = by_id_and_text("itemTV", "Log Out")
    # The "Are you sure you want to logout" confirmation is a standard Android dialog.
    txt_dialog_message = by_android_id("message")
    btn_dialog_logout = by_android_id("button1")
    btn_dialog_cancel = by_android_id("button2")

    def shows_log_out(self) -> bool:
        return self.is_visible(self.lnk_log_out, timeout=5)

    def shows_log_in(self) -> bool:
        return self.is_visible(self.lnk_log_in, timeout=5)

    @allure.step("Choose Log In")
    def choose_log_in(self):
        from src.pages.login_page import LoginPage

        self.tap(self.lnk_log_in)
        return LoginPage(self.driver)

    @allure.step("Choose Catalog")
    def choose_catalog(self):
        from src.pages.catalog_page import CatalogPage

        self.tap(self.lnk_catalog)
        return CatalogPage(self.driver)

    @allure.step("Choose Log Out")
    def choose_log_out(self) -> str:
        """Opens the confirmation dialog; returns its message."""
        self.tap(self.lnk_log_out)
        return self.text_of(self.txt_dialog_message)

    @allure.step("Confirm Log Out")
    def confirm_log_out(self) -> None:
        self.tap(self.btn_dialog_logout)

    @allure.step("Cancel Log Out")
    def cancel_log_out(self) -> None:
        self.tap(self.btn_dialog_cancel)

    def close(self) -> None:
        self.go_back()
