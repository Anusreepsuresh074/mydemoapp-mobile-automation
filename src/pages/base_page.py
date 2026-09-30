"""BasePage: what every page object shares. Finding elements with explicit waits, never sleeps."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

PACKAGE = "com.saucelabs.mydemoapp.android"
DEFAULT_TIMEOUT = 15

Locator = tuple[str, str]


def by_id(name: str) -> Locator:
    """A resource id of My Demo App; every one is namespaced by the package."""
    return AppiumBy.ID, f"{PACKAGE}:id/{name}"


def by_accessibility_id(value: str) -> Locator:
    return AppiumBy.ACCESSIBILITY_ID, value


def by_text(text: str) -> Locator:
    return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'


def by_android_id(name: str) -> Locator:
    """A resource id of Android itself, such as the buttons of a system dialog."""
    return AppiumBy.ID, f"android:id/{name}"


def by_id_and_text(name: str, text: str) -> Locator:
    """For rows that share one resource id and differ only by their visible text (the side menu)."""
    return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{PACKAGE}:id/{name}").text("{text}")'


class BasePage:
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

    def wait_for_any(self, locators: list[Locator], timeout: float = 5) -> bool:
        """True as soon as one of the elements is visible; False if none shows within the timeout."""
        try:
            self.wait(timeout).until(ec.any_of(*(ec.visibility_of_element_located(loc) for loc in locators)))
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

    def texts_of(self, locator: Locator) -> list[str]:
        return [element.text for element in self.find_all(locator)]

    def attribute_of(self, locator: Locator, name: str) -> str:
        return self.find(locator).get_attribute(name)

    def scroll_to(self, locator: Locator) -> None:
        """Scroll the screen's scrollable area until the element with this resource id is in view."""
        by, value = locator
        assert by == AppiumBy.ID, "scroll_to takes a resource-id locator"
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().resourceId("{value}"))',
        )

    def swipe_up(self) -> bool:
        """Scroll the content down by most of a screen; False once the end of the content is reached."""
        size = self.driver.get_window_size()
        return self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": size["width"] * 0.1,
                "top": size["height"] * 0.25,
                "width": size["width"] * 0.8,
                "height": size["height"] * 0.55,
                "direction": "down",
                "percent": 0.9,
            },
        )

    def app_is_in_foreground(self) -> bool:
        return self.driver.current_package == PACKAGE

    def hide_keyboard(self) -> None:
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    def go_back(self) -> None:
        """The phone's Back button."""
        self.driver.back()
