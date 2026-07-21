# dotswitch

A modular profile switcher for Hyprland dotfile setups.

## Planned features

- TOML-based profile manifests
- Git, local and external profile sources
- Fixed default profile or `last-used`
- Fallback profiles
- Atomic profile activation
- Profile validation and health checks
- Update one profile or all registered profiles
- Snapshots and rollback
- Adapters for Omarchy, ML4W, Caelestia and custom dotfiles

## Current status

Early development. The command-line interface and profile format are currently being designed.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install --editable .
dotswitch --help



