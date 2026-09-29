"""Product details."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class ProductScreen(BaseScreen):
    txt_name = rid("productTV")
    txt_price = rid("priceTV")
    btn_minus = rid("minusIV")
    txt_quantity = rid("noTV")
    btn_plus = rid("plusIV")
    btn_add_to_cart = rid("cartBt")
