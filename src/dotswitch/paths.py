from __future__ import annotations

import os
from pathlib import Path


def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def xdg_state_home() -> Path:
    return Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))


CONFIG_DIR = xdg_config_home() / "dotswitch"
PROFILES_DIR = CONFIG_DIR / "profiles"

STATE_DIR = xdg_state_home() / "dotswitch"
DEFAULT_PROFILE_FILE = STATE_DIR / "default"
CURRENT_PROFILE_FILE = STATE_DIR / "current"
LAST_USED_PROFILE_FILE = STATE_DIR / "last-used"
