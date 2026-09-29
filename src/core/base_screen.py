"""The base class for every screen: finding elements with explicit waits, never sleeps."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15

Locator = tuple[str, str]


def by_id(resource_id: str) -> Locator:
    return AppiumBy.ID, resource_id


def by_accessibility_id(value: str) -> Locator:
    return AppiumBy.ACCESSIBILITY_ID, value


def by_text(text: str) -> Locator:
    return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'


class BaseScreen:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout: float = DEFAULT_TIMEOUT) -> WebDriverWait:
        # A screen that redraws (a drawer sliding in, a list refreshing) makes a found element stale;
        # the wait then simply finds it again instead of failing.
        return WebDriverWait(self.driver, timeout, ignored_exceptions=[StaleElementReferenceException])

    def find(self, locator: Locator, timeout: float = DEFAULT_TIMEOUT):
        return self.wait(timeout).until(ec.visibility_of_element_located(locator))

    def find_all(self, locator: Locator, timeout: float = DEFAULT_TIMEOUT):
        self.wait(timeout).until(ec.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def is_visible(self, locator: Locator, timeout: float = 3) -> bool:
        try:
            self.find(locator, timeout)
            return True
        except Exception:
            return False

    def tap(self, locator: Locator) -> None:
        def _click(driver) -> bool:
            element = ec.element_to_be_clickable(locator)(driver)
            if not element:
                return False
            element.click()
            return True

        self.wait().until(_click)

    def type_text(self, locator: Locator, text: str) -> None:
        def _type(driver) -> bool:
            field = ec.visibility_of_element_located(locator)(driver)
            if not field:
                return False
            field.clear()
            field.send_keys(text)
            return True

        self.wait().until(_type)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text
