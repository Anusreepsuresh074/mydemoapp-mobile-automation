"""Creates the Appium session for Android (UiAutomator2)."""

import logging
import os
import subprocess

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException

from src.core.config import Settings

log = logging.getLogger(__name__)

# Session start-up (not a test) can hit a brief emulator adb drop right after another session or a cold boot.
# These are the signatures of that environment problem; anything else fails at once.
_STARTUP_ADB_ERRORS = ("device offline", "instrumentation process cannot be initialized")


def _options(settings: Settings) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = settings.platform_name
    options.device_name = settings.device_name
    # Pin the exact device, so a phone plugged in by USB is never used by accident.
    options.udid = settings.device_name
    options.app = str(settings.app_path)
    options.app_package = settings.app_package
    if settings.app_activity:
        options.app_activity = settings.app_activity
    options.auto_grant_permissions = True
    options.new_command_timeout = 120
    options.uiautomator2_server_launch_timeout = 60000
    options.adb_exec_timeout = 60000
    # A cold emulator can take longer than the default 20 s to show the app's first screen.
    options.app_wait_duration = 40000
    # On a cold emulator the splash screen can hand over to the main screen before Appium looks,
    # so either of the app's activities counts as "started".
    options.app_wait_activity = f"{settings.app_package}.view.activities.*"
    # Tests reset app state themselves (tests/conftest.py), so the session never reinstalls between tests.
    options.no_reset = True
    return options


def _clean_device_side(settings: Settings) -> None:
    """Remove leftovers of an aborted session (see skills/mobile-teardown, Pitfalls)."""
    adb = os.path.join(os.environ.get("ANDROID_HOME", os.path.expanduser("~/Android/Sdk")), "platform-tools", "adb")
    device = ["-s", settings.device_name]
    commands = [
        [*device, "forward", "--remove-all"],
        [*device, "shell", "am", "force-stop", "io.appium.uiautomator2.server.test"],
        [*device, "shell", "am", "force-stop", "io.appium.uiautomator2.server"],
    ]
    for args in commands:
        subprocess.run([adb, *args], capture_output=True, timeout=30, check=False)


def create_driver(settings: Settings) -> webdriver.Remote:
    _clean_device_side(settings)
    try:
        return webdriver.Remote(settings.appium_url, options=_options(settings))
    except WebDriverException as error:
        if not any(signature in str(error) for signature in _STARTUP_ADB_ERRORS):
            raise
        log.warning("Session start-up hit a known emulator adb drop; cleaning up and trying once more.")
        _clean_device_side(settings)
        return webdriver.Remote(settings.appium_url, options=_options(settings))
