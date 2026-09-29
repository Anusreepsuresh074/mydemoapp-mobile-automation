"""The sort options sheet opened from the catalogue."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class SortSheet(BaseScreen):
    btn_name_ascending = rid("nameAscCL")
    btn_name_descending = rid("nameDesCL")
    btn_price_ascending = rid("priceAscCL")
    btn_price_descending = rid("priceDesCL")
