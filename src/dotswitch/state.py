from __future__ import annotations

from pathlib import Path

from dotswitch.paths import (
    CURRENT_PROFILE_FILE,
    DEFAULT_PROFILE_FILE,
    LAST_USED_PROFILE_FILE,
    STATE_DIR,
)


def read_value(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None

    return value or None


def write_value(path: Path, value: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(value + "\n", encoding="utf-8")
    temporary_path.replace(path)


def get_default_profile() -> str | None:
    return read_value(DEFAULT_PROFILE_FILE)


def set_default_profile(profile: str) -> None:
    write_value(DEFAULT_PROFILE_FILE, profile)


def get_current_profile() -> str | None:
    return read_value(CURRENT_PROFILE_FILE)


def get_last_used_profile() -> str | None:
    return read_value(LAST_USED_PROFILE_FILE)
