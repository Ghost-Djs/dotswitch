from __future__ import annotations

import argparse
import sys

from dotswitch.profiles import ProfileError, load_profiles
from dotswitch.state import (
    get_current_profile,
    get_default_profile,
    get_last_used_profile,
    set_default_profile,
)

VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dotswitch",
        description="Switch and manage Hyprland dotfile profiles.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    commands = parser.add_subparsers(dest="command")

    commands.add_parser("list", help="List registered profiles")
    commands.add_parser("status", help="Show profile state")

    default_parser = commands.add_parser(
        "default",
        help="Set the default profile or use last-used",
    )
    default_parser.add_argument("profile")

    update_parser = commands.add_parser(
        "update",
        help="Update one or all profiles",
    )
    update_parser.add_argument("profile", nargs="?")
    update_parser.add_argument("--all", action="store_true")
    update_parser.add_argument("--check", action="store_true")
    update_parser.add_argument("--dry-run", action="store_true")

    return parser


def command_list() -> int:
    profiles = load_profiles()

    if not profiles:
        print("No profiles registered.")
        return 0

    current = get_current_profile()
    default = get_default_profile()

    for profile in profiles.values():
        markers: list[str] = []

        if profile.id == current:
            markers.append("current")

        if profile.id == default:
            markers.append("default")

        if profile.experimental:
            markers.append("experimental")

        suffix = f" [{', '.join(markers)}]" if markers else ""
        print(f"{profile.id:<20} {profile.name}{suffix}")

    return 0


def command_status() -> int:
    print(f"Current:   {get_current_profile() or 'none'}")
    print(f"Default:   {get_default_profile() or 'none'}")
    print(f"Last used: {get_last_used_profile() or 'none'}")
    return 0


def command_default(profile_id: str) -> int:
    profiles = load_profiles()

    if profile_id != "last-used" and profile_id not in profiles:
        print(f"Unknown profile: {profile_id}", file=sys.stderr)
        return 1

    set_default_profile(profile_id)
    print(f"Default profile set to: {profile_id}")
    return 0


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "list":
            exit_code = command_list()
        elif args.command == "status":
            exit_code = command_status()
        elif args.command == "default":
            exit_code = command_default(args.profile)
        elif args.command == "update":
            print("Update support is not implemented yet.")
            exit_code = 0
        else:
            parser.print_help()
            exit_code = 0

    except ProfileError as exc:
        print(f"Profile error: {exc}", file=sys.stderr)
        exit_code = 1

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
