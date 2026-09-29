"""Catalogue: the product grid, plus the header shared by most screens."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class CatalogScreen(BaseScreen):
    txt_title = rid("productTV")
    card_product_image = rid("productIV")
    txt_product_name = rid("titleTV")
    txt_product_price = rid("priceTV")
    btn_sort = rid("sortIV")
    btn_cart = rid("cartRL")
    txt_cart_badge = rid("cartTV")
    btn_menu = rid("menuIV")

    def product_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.txt_product_name)]

    def product_prices(self) -> list[str]:
        return [el.text for el in self.find_all(self.txt_product_price)]
