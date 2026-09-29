"""The cart, filled or empty."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class CartScreen(BaseScreen):
    txt_title = rid("productTV")
    txt_item_name = rid("titleTV")
    txt_item_price = rid("priceTV")
    txt_item_quantity = rid("noTV")
    btn_remove = rid("removeBt")
    txt_item_count = rid("itemsTV")
    txt_total = rid("totalPriceTV")
    btn_checkout = rid("cartBt")
    txt_empty_title = rid("noItemTitleTV")
    btn_go_shopping = rid("shoppingBt")
