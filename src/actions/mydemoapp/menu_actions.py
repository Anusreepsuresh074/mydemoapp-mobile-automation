from src.screens.mydemoapp.catalog_screen import CatalogScreen
from src.screens.mydemoapp.menu_screen import MenuScreen


class MenuActions:
    def __init__(self, driver):
        self.driver = driver
        self.screen = MenuScreen(driver)

    def open(self) -> None:
        CatalogScreen(self.driver).tap(CatalogScreen.btn_menu)

    def choose_log_in(self) -> None:
        self.screen.tap(MenuScreen.lnk_log_in)

    def shows_log_out(self) -> bool:
        return self.screen.is_visible(MenuScreen.lnk_log_out, timeout=3)

    def close(self) -> None:
        self.driver.back()
