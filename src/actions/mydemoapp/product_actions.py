from src.screens.mydemoapp.product_screen import ProductScreen


class ProductActions:
    def __init__(self, driver):
        self.screen = ProductScreen(driver)

    def name(self) -> str:
        return self.screen.text_of(ProductScreen.txt_name)

    def price(self) -> str:
        return self.screen.text_of(ProductScreen.txt_price)

    def quantity(self) -> int:
        return int(self.screen.text_of(ProductScreen.txt_quantity))

    def increase(self, times: int = 1) -> None:
        for _ in range(times):
            self.screen.tap(ProductScreen.btn_plus)

    def decrease(self, times: int = 1) -> None:
        for _ in range(times):
            self.screen.tap(ProductScreen.btn_minus)

    def add_to_cart(self) -> None:
        self.screen.tap(ProductScreen.btn_add_to_cart)

    def is_open(self) -> bool:
        return self.screen.is_visible(ProductScreen.btn_add_to_cart)
