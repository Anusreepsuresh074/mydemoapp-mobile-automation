"""Session set-up: memory guard, one Appium session, a clean app for every test, failure attachments."""

import allure
import pytest

from src.core.config import Settings
from src.core.driver import create_driver


def _available_memory_mb() -> int:
    with open("/proc/meminfo") as meminfo:
        for line in meminfo:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) // 1024
    return 0


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.load()


@pytest.fixture(scope="session", autouse=True)
def _memory_guard(settings):
    """Fail at once on a starved machine instead of failing randomly later (create-mobile-framework-structure)."""
    available = _available_memory_mb()
    if available and available < settings.min_available_memory_mb:
        pytest.exit(f"Only {available} MB memory available; need {settings.min_available_memory_mb} MB.", returncode=3)


@pytest.fixture(scope="session")
def driver(settings):
    session = create_driver(settings)
    yield session
    session.quit()


@pytest.fixture
def app(driver, settings):
    """A fresh app for every test: clear its data, then launch it (mobile-teardown's "cheap sign-in" strategy)."""
    driver.terminate_app(settings.app_package)
    driver.execute_script("mobile: clearApp", {"appId": settings.app_package})
    driver.activate_app(settings.app_package)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "app" in item.fixturenames:
        driver = item.funcargs.get("app")
        if driver is not None:
            allure.attach(driver.get_screenshot_as_png(), "screenshot", allure.attachment_type.PNG)
            allure.attach(driver.page_source, "page source", allure.attachment_type.XML)
