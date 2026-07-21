from __future__ import annotations

import argparse

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
    commands.add_parser("status", help="Show the current profile")

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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    print(f"{args.command}: not implemented yet")


if __name__ == "__main__":
    main()
