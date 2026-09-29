"""Settings for the run, read once from environment variables (a local .env file or CI secrets)."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set. Copy .env.example to .env and fill it in.")
    return value


@dataclass(frozen=True)
class Settings:
    app_path: Path
    app_package: str
    app_activity: str
    platform_name: str
    device_name: str
    appium_url: str
    min_available_memory_mb: int

    @classmethod
    def load(cls) -> "Settings":
        host = os.getenv("APPIUM_HOST", "127.0.0.1")
        port = os.getenv("APPIUM_PORT", "4723")
        return cls(
            app_path=(ROOT / _required("APP_PATH")).resolve(),
            app_package=_required("APP_PACKAGE"),
            app_activity=os.getenv("APP_ACTIVITY", "").strip(),
            platform_name=os.getenv("PLATFORM_NAME", "Android"),
            device_name=os.getenv("DEVICE_NAME", "emulator-5554"),
            appium_url=f"http://{host}:{port}",
            min_available_memory_mb=int(os.getenv("MIN_AVAILABLE_MEMORY_MB", "2048")),
        )


def credentials() -> tuple[str, str]:
    """The test account, from the environment only (see get-mobile-auth)."""
    return _required("TEST_USERNAME"), _required("TEST_PASSWORD")
