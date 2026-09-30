"""The catalogue: the product grid, the first screen of the app."""

import allure

from src.pages.base_page import BasePage, by_id
from src.pages.components.header_bar import HeaderBar
from src.pages.components.sort_sheet import SortSheet
from src.pages.product_page import ProductPage


class CatalogPage(BasePage):
    txt_title = by_id("productTV")
    card_product_image = by_id("productIV")
    txt_product_name = by_id("titleTV")
    txt_product_price = by_id("priceTV")
    btn_sort = by_id("sortIV")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderBar(driver)

    def title(self) -> str:
        return self.text_of(self.txt_title)

    def is_open(self) -> bool:
        return self.is_visible(self.btn_sort)

    def product_names(self) -> list[str]:
        return self.texts_of(self.txt_product_name)

    def product_prices(self) -> list[str]:
        return self.texts_of(self.txt_product_price)

    def visible_products(self) -> list[tuple[str, str]]:
        """(name, price) of every card whose name and price are both on screen.

        A card's price sits under its name in the same column, so each name is paired with the nearest
        price below it at the same left edge; a card cut by the screen edge is left out."""
        names = [(e.text, e.rect) for e in self.driver.find_elements(*self.txt_product_name)]
        prices = [(e.text, e.rect) for e in self.driver.find_elements(*self.txt_product_price)]
        products = []
        for name, n in names:
            below = [(p["y"] - n["y"], price) for price, p in prices if p["x"] == n["x"] and p["y"] > n["y"]]
            if below:
                products.append((name, min(below)[1]))
        return products

    @allure.step("Read every product, scrolling to the end of the catalogue")
    def all_products(self) -> list[tuple[str, str]]:
        """Every (name, price) in the catalogue, in screen order."""
        self.find(self.txt_product_name)
        seen: dict[str, str] = {}
        screens_without_new = 0
        while screens_without_new < 2:
            before = len(seen)
            for name, price in self.visible_products():
                seen.setdefault(name, price)
            self.swipe_up()
            screens_without_new = screens_without_new + 1 if len(seen) == before else 0
        return list(seen.items())

    def first_product(self) -> tuple[str, str]:
        """The (name, price) of the first product in the grid."""
        return self.product_names()[0], self.product_prices()[0]

    @allure.step("Open product number {index} in the grid")
    def open_product(self, index: int = 0) -> ProductPage:
        # After Back the grid redraws; wait until it is showing before picking a card.
        self.find(self.card_product_image)
        self.find_all(self.card_product_image)[index].click()
        page = ProductPage(self.driver)
        assert page.is_open(), f"product {index} did not open"
        return page

    @allure.step("Sort the catalogue by {option}")
    def sort_by(self, option: str) -> None:
        self.tap(self.btn_sort)
        SortSheet(self.driver).choose(option)
