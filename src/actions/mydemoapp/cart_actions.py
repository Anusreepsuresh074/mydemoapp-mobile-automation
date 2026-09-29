from src.screens.mydemoapp.cart_screen import CartScreen


class CartActions:
    def __init__(self, driver):
        self.screen = CartScreen(driver)

    def item_names(self) -> list[str]:
        return [el.text for el in self.screen.find_all(CartScreen.txt_item_name)]

    def item_price(self) -> str:
        return self.screen.text_of(CartScreen.txt_item_price)

    def item_count(self) -> str:
        return self.screen.text_of(CartScreen.txt_item_count)

    def total(self) -> str:
        return self.screen.text_of(CartScreen.txt_total)

    def remove_first_item(self) -> None:
        self.screen.tap(CartScreen.btn_remove)

    def proceed_to_checkout(self) -> None:
        self.screen.tap(CartScreen.btn_checkout)

    def is_empty(self) -> bool:
        return self.screen.is_visible(CartScreen.txt_empty_title) and self.screen.is_visible(CartScreen.btn_go_shopping)
