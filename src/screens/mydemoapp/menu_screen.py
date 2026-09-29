"""The side menu. Its rows share one id, so rows are found by their visible text."""

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_screen import BaseScreen, Locator
from src.screens.mydemoapp._ids import PACKAGE


def _row(text: str) -> Locator:
    return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{PACKAGE}:id/itemTV").text("{text}")'


class MenuScreen(BaseScreen):
    lnk_log_in = _row("Log In")
    lnk_log_out = _row("Log Out")
    lnk_catalog = _row("Catalog")
