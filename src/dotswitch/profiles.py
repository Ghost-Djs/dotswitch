from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotswitch.paths import PROFILES_DIR


@dataclass(frozen=True)
class Profile:
    id: str
    name: str
    path: Path
    fallback: str | None = None
    experimental: bool = False


class ProfileError(Exception):
    pass


def load_profile(path: Path) -> Profile:
    try:
        with path.open("rb") as file:
            data = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProfileError(f"Could not read profile {path}: {exc}") from exc

    profile_id = data.get("id")
    name = data.get("name")

    if not isinstance(profile_id, str) or not profile_id.strip():
        raise ProfileError(f"{path}: missing or invalid 'id'")

    if not isinstance(name, str) or not name.strip():
        raise ProfileError(f"{path}: missing or invalid 'name'")

    fallback = data.get("fallback")
    experimental = data.get("experimental", False)

    if fallback is not None and not isinstance(fallback, str):
        raise ProfileError(f"{path}: 'fallback' must be a string")

    if not isinstance(experimental, bool):
        raise ProfileError(f"{path}: 'experimental' must be a boolean")

    return Profile(
        id=profile_id,
        name=name,
        path=path,
        fallback=fallback,
        experimental=experimental,
    )


def load_profiles(directory: Path = PROFILES_DIR) -> dict[str, Profile]:
    directory.mkdir(parents=True, exist_ok=True)

    profiles: dict[str, Profile] = {}

    for path in sorted(directory.glob("*.toml")):
        profile = load_profile(path)

        if profile.id in profiles:
            raise ProfileError(f"Duplicate profile id: {profile.id}")

        profiles[profile.id] = profile

    return profiles
