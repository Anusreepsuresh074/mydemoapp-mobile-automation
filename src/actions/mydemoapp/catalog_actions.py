from src.screens.mydemoapp.catalog_screen import CatalogScreen
from src.screens.mydemoapp.sort_sheet import SortSheet

SORT_OPTIONS = {
    "name ascending": SortSheet.btn_name_ascending,
    "name descending": SortSheet.btn_name_descending,
    "price ascending": SortSheet.btn_price_ascending,
    "price descending": SortSheet.btn_price_descending,
}


class CatalogActions:
    def __init__(self, driver):
        self.screen = CatalogScreen(driver)
        self.sort_sheet = SortSheet(driver)

    def title(self) -> str:
        return self.screen.text_of(CatalogScreen.txt_title)

    def first_product(self) -> tuple[str, str]:
        return self.screen.product_names()[0], self.screen.product_prices()[0]

    def names(self) -> list[str]:
        return self.screen.product_names()

    def prices(self) -> list[str]:
        return self.screen.product_prices()

    def open_first_product(self) -> None:
        self.screen.find_all(CatalogScreen.card_product_image)[0].click()

    def open_cart(self) -> None:
        self.screen.tap(CatalogScreen.btn_cart)

    def open_menu(self) -> None:
        self.screen.tap(CatalogScreen.btn_menu)

    def sort_by(self, option: str) -> None:
        self.screen.tap(CatalogScreen.btn_sort)
        self.sort_sheet.tap(SORT_OPTIONS[option])

    def cart_badge(self) -> str | None:
        if not self.screen.is_visible(CatalogScreen.txt_cart_badge, timeout=2):
            return None
        return self.screen.text_of(CatalogScreen.txt_cart_badge)
