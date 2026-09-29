"""Every resource id in My Demo App is namespaced by the package."""

from src.core.base_screen import Locator, by_id

PACKAGE = "com.saucelabs.mydemoapp.android"


def rid(name: str) -> Locator:
    return by_id(f"{PACKAGE}:id/{name}")
