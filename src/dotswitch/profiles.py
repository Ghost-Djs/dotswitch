from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotswitch.paths import PROFILES_DIR


@dataclass(frozen=True)
class ProfileSource:
    type: str
    path: Path | None = None
    repo: str | None = None


@dataclass(frozen=True)
class Profile:
    id: str
    name: str
    path: Path
    source: ProfileSource
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

    source_data = data.get("source")

    if not isinstance(source_data, dict):
        raise ProfileError(f"{path}: missing or invalid '[source]' section")

    source_type = source_data.get("type")
    source_path = source_data.get("path")
    source_repo = source_data.get("repo")

    if not isinstance(source_type, str) or not source_type.strip():
        raise ProfileError(f"{path}: missing or invalid 'source.type'")

    allowed_source_types = {"local", "git", "external"}

    if source_type not in allowed_source_types:
        raise ProfileError(
            f"{path}: unsupported source type '{source_type}'"
        )

    if source_path is not None and not isinstance(source_path, str):
        raise ProfileError(f"{path}: 'source.path' must be a string")

    if source_repo is not None and not isinstance(source_repo, str):
        raise ProfileError(f"{path}: 'source.repo' must be a string")

    if source_type == "local" and source_path is None:
        raise ProfileError(
            f"{path}: local sources require 'source.path'"
        )

    if source_type == "git" and source_repo is None:
        raise ProfileError(
            f"{path}: git sources require 'source.repo'"
        )

    source = ProfileSource(
        type=source_type,
        path=Path(source_path).expanduser() if source_path else None,
        repo=source_repo,
    )

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
        source=source,
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
