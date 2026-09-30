"""The sort options sheet, opened from the catalogue."""

import allure

from src.pages.base_page import BasePage, by_id


class SortSheet(BasePage):
    btn_name_ascending = by_id("nameAscCL")
    btn_name_descending = by_id("nameDesCL")
    btn_price_ascending = by_id("priceAscCL")
    btn_price_descending = by_id("priceDesCL")

    OPTIONS = {
        "name ascending": btn_name_ascending,
        "name descending": btn_name_descending,
        "price ascending": btn_price_ascending,
        "price descending": btn_price_descending,
    }

    @allure.step("Choose sort order: {option}")
    def choose(self, option: str) -> None:
        self.tap(self.OPTIONS[option])
