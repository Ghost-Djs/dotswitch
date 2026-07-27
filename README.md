# dotswitch

> [!WARNING]
> **dotswitch is in early development and cannot safely switch real desktop configurations yet.**
>
> The current implementation provides only the initial command-line, profile-loading and state-management foundation.
>
> Transactional desktop switching, external profile installation, backups, rollback, fallback recovery, update management and the developer platform are still planned or under development.
>
> **Do not use dotswitch to manage an important desktop configuration yet.**
>
> Commands and workflows shown in this README may describe planned behaviour rather than functionality that is currently available.

<p align="center">
  <h1 align="center">dotswitch</h1>
  <p align="center">
    <strong>A safe profile manager for Linux desktop setups, shells and rices.</strong>
  </p>
  <p align="center">
    Install, test, switch, update and roll back Linux desktop setups without risking your current system.
  </p>
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-early%20development-orange">
  <img alt="License" src="https://img.shields.io/badge/license-GPL--3.0-blue">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Linux-lightgrey">
  <img alt="Focus" src="https://img.shields.io/badge/focus-Hyprland%20first-7c3aed">
  <img alt="Language" src="https://img.shields.io/badge/language-Python-3776AB">
</p>

---

## What is dotswitch?

dotswitch is an experimental Linux desktop profile manager.

It is designed to make complete desktop setups installable, testable, switchable, updateable and reversible without allowing third-party installers to overwrite the user's existing configuration.

Instead of installing every setup directly into `~/.config`, dotswitch is planned to import supported setups into isolated and independently managed profiles.

The long-term goal is to provide a common integration and management platform for Linux desktop profiles across compositors, desktop environments and distributions.

```text
Git repository or local setup
              ↓
        isolated profile
              ↓
        validation and build
              ↓
     temporary or persistent activation
              ↓
        fallback and rollback
```

---

## Current project status

dotswitch is currently a development prototype.

### Currently implemented

- Initial Python project structure
- XDG-based configuration and state paths
- TOML profile definitions
- Basic profile loading and validation
- Profile listing
- Profile status output
- Current-profile state handling
- Fixed default-profile handling
- `last-used` default mode
- Experimental profile metadata

### Not yet implemented

- Real desktop configuration deployment
- Safe switching of desktop configurations
- Isolated profile roots
- Transactional activation
- Automatic backups
- Automatic rollback
- Fallback and rescue mechanisms
- Installation of external desktop projects
- Package and dependency management
- Profile updates
- Shared asset deduplication
- Graphical profile browsing
- A stable developer SDK
- Community profile registry

The current commands must not be interpreted as proof that safe desktop switching already works.

---

## Why dotswitch?

Installing a Linux desktop rice often means cloning a repository, running an installation script and hoping that the existing desktop survives.

Different projects may:

- overwrite existing compositor configurations
- replace Waybar, Rofi, Quickshell or notification configurations
- install duplicate terminals and applications
- modify startup behaviour or system services
- replace themes, fonts, icons and wallpapers
- expect specific package versions
- use incompatible configuration layouts
- provide no reliable rollback method

dotswitch is intended to place a safe management layer between the user's system and those projects.

The existing desktop should remain available as a known working fallback, while imported setups are stored and managed separately.

---

## Planned user experience

The intended workflow is simple:

```bash
dotswitch setup
dotswitch browse
dotswitch install <profile>
dotswitch activate <profile>
dotswitch rollback <profile>
```

> [!NOTE]
> These commands describe planned behaviour and are not fully functional yet.

The goal is that a user can:

- keep the current desktop as a fallback
- try profiles temporarily
- make a profile persistent only when explicitly requested
- keep profile-specific keybindings, wallpapers and settings
- update a profile without modifying the active build
- roll back to a previous working version
- recover from a broken or black desktop session
- install supported setups without running destructive installers directly

---

## Example projects and affiliation

Projects such as:

- Caelestia Shell
- ML4W Dotfiles
- DankMaterialShell
- HyDE
- Omarchy
- JaKooLit Hyprland Dotfiles
- end-4 / illogical-impulse

are referenced throughout this README as examples of the kinds of desktop shells, dotfile collections and complete desktop setups that dotswitch may eventually support.

They are **not currently integrated unless explicitly stated otherwise**.

Their inclusion:

- does not guarantee future support
- does not imply endorsement
- does not imply affiliation
- does not make dotswitch an official installer for those projects

Future integrations should fetch projects from their official upstream sources while preserving licences, attribution and project ownership.

---

## Core concept

Every imported desktop setup should be stored as an isolated profile.

A profile may contain:

```text
profile/
├── source/
├── root/
├── overlay/
├── prefix/
├── builds/
├── manifest.toml
└── manifest.lock
```

### `source`

The original upstream repository or imported source tree.

This directory remains unchanged so that:

- updates can be fetched cleanly
- upstream changes remain traceable
- local modifications do not corrupt the original source
- installed revisions can be reproduced

### `root`

The generated and validated configuration used when the profile is active.

The profile root is assembled from:

```text
upstream source
+ dotswitch adapter rules
+ host-specific configuration
+ user overlay
= generated profile root
```

### `overlay`

Persistent profile-specific user changes.

Examples include:

- keybindings
- wallpaper selection
- monitor configuration
- shell settings
- layout changes
- launcher preferences
- personal theme adjustments

These changes should remain attached to the profile when switching away from it.

They should also be reapplied when a newer upstream version is built, as long as no incompatible conflict occurs.

### `prefix`

Profile-specific programs, scripts and libraries that should not be installed globally when local installation is possible.

Example:

```text
prefix/
├── bin/
├── lib/
└── share/
```

### `builds`

Generated and validated versions of a profile.

Keeping multiple builds allows dotswitch to update profiles without modifying the currently active version.

Example:

```text
builds/
├── revision-a/
├── revision-b/
└── revision-c/
```

### `manifest.toml`

Describes how a profile should be installed, built, activated and managed.

### `manifest.lock`

Records the exact state used to create an installed build.

This may include:

- upstream repository
- release or commit
- update channel
- adapter version
- dependency state
- build timestamp
- applied migrations

---

## Safe profile switching

Profile activation is intended to be transactional.

A profile must be prepared completely before it replaces the currently active profile.

The planned activation process is:

1. Validate the profile manifest
2. Detect the current host and desktop environment
3. Resolve compatibility and required capabilities
4. Resolve required dependencies
5. Build the profile in a staging directory
6. Validate generated files and paths
7. Create a snapshot and transaction journal
8. Stop conflicting profile-specific processes
9. Atomically switch the active profile
10. Start the new profile-specific processes
11. Run health checks
12. Mark the profile as healthy
13. Restore the previous profile automatically if activation fails

A build must never be modified while it is active.

---

## Temporary activation

Normal profile activation is planned to be temporary:

```bash
dotswitch activate example-profile
```

The profile would remain active only for the current session.

After logout or reboot, dotswitch would return to the configured default profile.

A profile would only become persistent when explicitly selected:

```bash
dotswitch default example-profile
```

A separate mode is planned for users who intentionally want the most recently used profile to load after login:

```bash
dotswitch default last-used
```

The safe default remains:

> Temporary switching unless the user explicitly changes the persistent default.

---

## System default and fallback

During initial setup, dotswitch should detect and import the currently working desktop configuration as:

```text
system-default
```

This profile should initially become:

- the current profile
- the default profile
- the fallback profile
- the last successfully used profile

The fallback must not be hardcoded to a specific project such as Omarchy.

On an Omarchy system, `system-default` may contain the existing Omarchy configuration.

On another system, it may contain:

- an existing Hyprland configuration
- a niri setup
- a Sway setup
- a GNOME desktop state
- a KDE Plasma desktop state
- another supported desktop configuration

The fallback is therefore based on the desktop that was already working before dotswitch took control.

---

## Failed-session protection

A newly started profile should first be marked as pending.

Example state:

```text
pending profile: example-profile
session healthy: false
fallback: system-default
```

Only after successful health checks should the profile be marked as healthy.

If a session crashes or never reaches a healthy state, the next login should automatically load the fallback profile.

Planned recovery methods include:

- a compositor keybinding
- a TTY-compatible rescue command
- a minimal recovery script without desktop dependencies
- recovery without relying on the active profile
- a login guard that detects unsuccessful profile starts

A panic keybinding is useful only while the compositor still processes input.

A separate TTY recovery path is required for completely broken or black desktop sessions.

---

## Global system and application handling

dotswitch does not create a completely separate operating system for every profile.

Normal applications and personal data remain global.

Examples include:

- games
- Steam libraries
- Heroic and Lutris libraries
- browsers
- development tools
- communication applications
- SSH keys and configuration
- Git configuration
- GPG configuration
- documents
- downloads
- personal application data

Shared desktop infrastructure also remains global:

- NetworkManager
- `nmcli`
- PipeWire
- WirePlumber
- BlueZ
- desktop portals
- common system services
- system-wide package management

Different profiles may provide different user interfaces for the same infrastructure.

For example:

```text
NetworkManager
├── desktop shell network menu
├── Waybar network module
└── another profile frontend
```

Similarly:

```text
PipeWire and WirePlumber
├── desktop shell volume controls
├── Waybar audio controls
├── wpctl
└── another profile frontend
```

The backend remains global while the visual frontend changes with the profile.

---

## Profile-managed components

Profiles should control only explicitly assigned desktop components.

Examples include:

- compositor configuration
- desktop shells
- bars
- launchers
- notification daemons
- lock screens
- idle daemons
- wallpaper services
- application launch menus
- optional terminal configuration
- optional shell configuration

Files and directories should be assigned an ownership class.

Planned ownership classes include:

```text
profile
optional
shared
protected
blocked
```

### `profile`

The component belongs to the active profile and changes when profiles are switched.

### `optional`

The profile recommends or provides the component, but the user may keep a global preference instead.

Examples:

- terminal
- shell
- file manager
- text editor

### `shared`

The resource remains available across multiple profiles.

### `protected`

The path must not be replaced automatically.

Examples include:

- `~/.ssh`
- `~/.gnupg`
- browser data
- personal documents
- game libraries
- Git identity

### `blocked`

The path or operation is considered unsafe for automatic integration.

---

## Isolated profile activation

dotswitch should not replace the entire `XDG_CONFIG_HOME` for a desktop session.

Doing so would cause unrelated applications to search for their configuration inside the active rice profile.

Instead, only declared desktop paths should be managed.

A central link may point to the active profile:

```text
~/.local/share/dotswitch/active
    -> profiles/example-profile/current
```

Managed configuration paths may then point through that active link:

```text
~/.config/hypr
    -> ~/.local/share/dotswitch/active/root/.config/hypr

~/.config/waybar
    -> ~/.local/share/dotswitch/active/root/.config/waybar
```

Switching the central active-profile link can change multiple managed paths atomically.

Profile-specific processes may additionally receive a controlled environment containing paths such as:

```text
PATH
XDG_CONFIG_HOME
QML import paths
profile-specific library paths
```

This environment should apply only to the relevant profile processes, not to every normal desktop application.

---

## Shared asset store

Wallpapers, fonts, icons, cursors and themes should not be duplicated for every installed profile.

dotswitch is planned to use a global content-addressed asset store:

```text
~/.local/share/dotswitch/store/
├── wallpapers/
├── fonts/
├── icons/
├── cursors/
├── themes/
└── blobs/
```

Assets are identified by content hashes.

If multiple profiles contain the same asset, the file should be stored only once while remaining available to every compatible profile.

Imported wallpapers may be grouped into collections:

```text
All wallpapers
Profile A
Profile B
Custom
Favorites
```

Every profile still keeps its own active wallpaper selection in its overlay.

This provides:

```text
one global wallpaper pool
+
one persistent wallpaper selection per profile
```

Known adapters should be able to:

- detect wallpaper directories
- import wallpaper assets
- deduplicate identical files
- preserve source attribution where required
- rewrite expected wallpaper paths
- emulate expected directory layouts
- expose imported wallpapers to other profiles

The same general model may later be used for:

- fonts
- icon themes
- cursor themes
- GTK themes
- Plasma themes
- colour schemes

---

## Profile types

The profile format is intended to support more than complete Hyprland configurations.

### Compositor profiles

Complete configurations for compositors such as:

- Hyprland
- niri
- Sway

### Desktop profiles

Complete desktop-environment configurations for environments such as:

- GNOME
- KDE Plasma
- Cinnamon
- Xfce

### Shell profiles

Desktop shells that run on top of a supported compositor.

Caelestia Shell and DankMaterialShell are examples of this category, not confirmed current integrations.

### Theme profiles

Visual packages containing combinations of:

- GTK themes
- Plasma styles
- icon themes
- cursor themes
- wallpapers
- colour schemes

### Component profiles

Individual desktop components such as:

- Waybar layouts
- Rofi themes
- notification configurations
- lock screens
- panel layouts
- wallpaper collections

### Profile bundles

A coordinated collection of compatible components.

A bundle may combine:

- compositor configuration
- shell
- launcher
- notification system
- theme
- wallpaper collection

---

## Compatibility detection

dotswitch is planned to detect:

- Linux distribution
- distribution family
- package manager
- init system
- user-service manager
- session type
- desktop environment
- compositor
- desktop or compositor version
- installed capabilities
- currently running desktop components
- host-specific hardware information

A future profile registry should separate profiles into:

```text
Compatible
Experimental
Unsupported
```

Example:

```text
Detected system:
Fedora · GNOME · Wayland

Compatible profiles:
- Example GNOME profile
- Example GNOME theme
- Example GNOME extension bundle

Unavailable:
- Example Hyprland setup
  Requires: Hyprland
```

Unsupported profiles may still be visible so the user can understand why they are unavailable.

The initial implementation is Hyprland-first, while the architecture is intended to remain backend-based.

---

## Desktop and compositor backends

Each desktop environment or compositor requires different installation, activation, backup and rollback logic.

The common dotswitch core should manage:

- profile metadata
- compatibility
- downloads
- versioning
- snapshots
- transaction state
- registry access
- user interface

Desktop-specific backends should handle the actual desktop state.

### Hyprland

Planned capabilities:

- isolated configuration roots
- atomic profile links
- process and conflict management
- `hyprctl` validation and reload support
- temporary session activation
- profile-specific shell management

### niri

Planned capabilities:

- profile-specific KDL configuration
- explicit configuration paths
- niri IPC integration
- profile-specific process management

### Sway

Planned capabilities:

- isolated configuration
- Sway IPC validation and reload
- Waybar and notification-daemon management

### GNOME

GNOME requires a different management model based on:

- dconf and GSettings snapshots
- GNOME Shell Extensions
- extension version compatibility
- GTK themes
- icon themes
- cursor themes
- GNOME Shell themes
- keybindings
- session reload requirements

### KDE Plasma

Plasma integration may include:

- KPackage installation
- KConfig management
- Global Themes
- Plasma styles
- layout scripts
- panel and widget snapshots
- icon, cursor and colour-scheme management

### NixOS and Home Manager

NixOS requires a separate declarative backend.

dotswitch should not fight against files already controlled by Home Manager.

A future backend may generate and select Nix modules while relying on Nix generations for activation and rollback.

### Gentoo

Gentoo support is possible but would initially be experimental because of:

- Portage
- USE flags
- package masks
- custom package versions
- variable init systems
- locally selected package features

dotswitch should not automatically modify `/etc/portage` without explicit and carefully designed user control.

---

## Project integrations

Known projects may receive tested first-class adapters.

Initial reference targets may include:

- the imported `system-default` profile
- an existing custom Hyprland setup
- Omarchy
- Caelestia Shell
- ML4W Dotfiles

Possible later adapter targets may include:

- DankMaterialShell
- end-4 / illogical-impulse
- HyDE
- JaKooLit Hyprland Dotfiles

These projects are examples and planning targets only.

An adapter may provide:

- compatibility rules
- package requirements
- capability requirements
- configuration ownership
- process definitions
- conflict groups
- asset import rules
- update channels
- health checks
- migrations
- safe removal logic
- expected directory emulation
- project-specific path rewriting

---

## Developer platform

dotswitch is intended to become both an end-user application and an integration platform for desktop and rice maintainers.

A simple project should ideally become compatible through a versioned manifest:

```text
dotswitch.toml
```

A manifest may describe:

- profile identity
- profile type
- supported desktops and compositors
- supported distributions
- required capabilities
- required packages
- optional applications
- managed configuration paths
- shared paths
- protected paths
- profile processes
- conflict groups
- health checks
- update channels
- migrations
- uninstall behaviour
- asset locations
- attribution and licence information

Complex projects may additionally provide a programmable adapter or plugin.

Simple projects should not require custom Python code.

Planned developer commands include:

```bash
dotswitch init
dotswitch validate
dotswitch test
dotswitch pack
dotswitch doctor
```

### `dotswitch init`

Creates an initial integration structure.

Example:

```text
dotswitch.toml
.dotswitch/
├── patches/
├── migrations/
├── tests/
└── screenshots/
```

### `dotswitch validate`

May validate:

- manifest schema
- compatibility declarations
- source paths
- protected path access
- unsafe commands
- missing dependencies
- process conflicts
- health checks
- licence metadata

### `dotswitch test`

May create and validate a profile in a controlled test environment without modifying the user's main desktop.

### `dotswitch pack`

May create a reproducible registry or distribution artefact.

### `dotswitch doctor`

May inspect an integration or installed profile for common problems.

The goal is to let maintainers publish setups that can be safely installed through dotswitch without writing another destructive installation script.

---

## Community registry

A future registry may allow users to discover compatible profiles through commands such as:

```bash
dotswitch search
dotswitch browse
dotswitch install
```

Registry submissions should be automatically checked for:

- manifest validity
- licence information
- upstream attribution
- compatibility claims
- unsafe path access
- unsafe root operations
- build reproducibility
- health-check definitions
- update behaviour

The registry should display only profiles compatible with the detected host by default.

Experimental and unsupported profiles should remain clearly marked.

---

## Generic Git repository import

Unknown repositories may later be imported through static analysis.

dotswitch may search for common components such as:

- Hyprland configuration
- niri configuration
- Sway configuration
- Waybar
- Rofi
- Quickshell
- AGS
- SwayNC
- Mako
- wallpaper directories
- fonts
- icon themes
- package lists
- startup commands
- installation scripts

Detected content may be classified as:

```text
Profile-managed
Optional
Shared
Protected
Blocked
Unknown
```

Sensitive or unrelated paths should remain protected.

Unknown installation scripts must not be executed blindly.

Instead, dotswitch should:

1. Inspect the repository
2. Detect known files and components
3. Identify potentially unsafe operations
4. Generate a local manifest draft
5. Show which parts can be integrated safely
6. Require explicit handling for unclear operations

Known repositories with official adapters can offer stronger guarantees than unknown automatically imported repositories.

---

## Package and dependency handling

The system package manager remains responsible for global packages.

Examples include:

- Pacman
- DNF
- APT
- Zypper
- Portage
- Nix

dotswitch should:

- detect required packages
- determine which packages are already available
- avoid installing duplicate packages
- track which profiles require a package
- avoid removing packages still used by another profile
- never remove protected system infrastructure automatically

Packages such as NetworkManager, PipeWire and WirePlumber remain global even when multiple profiles use them.

Profile-specific scripts and locally buildable tools may be stored in the profile prefix.

Optional applications such as terminals, editors and file managers should not automatically replace the user's preferred global applications.

---

## Process and conflict handling

Multiple desktop components may be installed at the same time, but conflicting processes should not run simultaneously.

Planned conflict groups may include:

```text
desktop shell
status bar
launcher
notification daemon
wallpaper daemon
polkit agent
lock screen
```

Examples:

```text
notification daemon:
- Mako
- SwayNC
- desktop-shell notification service
```

A profile should declare which processes it:

- requires
- starts
- stops
- conflicts with
- expects during health checks

System services such as NetworkManager and PipeWire should remain untouched during normal profile switching.

---

## Updates and rollback

Updates must never be applied directly to the active profile build.

The planned update process is:

1. Fetch the new upstream revision
2. Keep the current build active
3. Create a separate worktree or staging checkout
4. Apply the current adapter
5. Import and deduplicate assets
6. Apply the user overlay
7. Run profile migrations if required
8. Build a new profile version
9. Validate the new build
10. Activate it only after successful validation
11. Run runtime health checks
12. Restore the previous build automatically if checks fail

Every installed profile may record:

- upstream repository
- installed commit or release
- update channel
- adapter version
- generated build version
- applied overlay state
- migration state

Old builds may be retained for direct rollback.

Example planned commands:

```bash
dotswitch update example-profile --check
dotswitch update example-profile
dotswitch rollback example-profile
```

System packages continue to be updated through the operating system's package manager.

---

## Storage management

Multiple profiles may contain overlapping files and assets.

dotswitch is planned to reduce unnecessary duplication through:

- shared Git object storage
- Git worktrees
- content-addressed assets
- shared wallpaper collections
- deduplicated fonts and icons
- configurable build retention
- configurable snapshot retention
- unused-asset cleanup

Example planned policy:

```text
keep recent builds: 2
keep snapshots: 3
deduplicate assets: enabled
remove unreferenced cache: enabled
```

---

## Roadmap

The roadmap describes the current direction of the project.

It is not a guarantee that every planned feature or integration will be implemented exactly as described.

### Phase 0: Command-line foundation

**Status: In progress**

Implemented:

- Initial Python project structure
- XDG-based configuration and state paths
- TOML profile definitions
- Basic profile loading and validation
- Profile listing
- Profile status output
- Current-profile state
- Fixed default profiles
- `last-used` default mode
- Experimental profile metadata

Remaining foundation work:

- Stabilise profile and state models
- Improve validation
- Add tests for existing commands
- Document current development behaviour

### Phase 1: Safe local profile core

**Status: Planned**

- Import the existing setup as `system-default`
- Preserve an initial immutable system snapshot
- Define the first stable profile manifest schema
- Classify managed, optional, shared, protected and blocked paths
- Implement isolated profile roots
- Implement staging builds
- Implement atomic active-profile switching
- Implement activation transaction journals
- Implement profile-specific process handling
- Implement static validation
- Implement automatic rollback
- Implement dry-run activation
- Add profile overlays
- Add profile snapshots
- Add TTY-compatible rescue support
- Add panic fallback keybinding support
- Add login health checks
- Add failed-session boot guard

### Phase 2: First external integrations

**Status: Planned**

Potential reference integrations:

- Caelestia Shell
- ML4W Dotfiles

Required supporting work:

- Dependency and capability resolution
- Shared package ownership tracking
- Process conflict groups
- Profile-specific health checks
- Safe external profile removal
- Stable and rolling update channels
- Upstream commit locking
- Attribution and licence tracking

The listed projects are examples and planned targets, not current supported integrations.

### Phase 3: Assets and profile updates

**Status: Planned**

- Global content-addressed asset store
- Wallpaper directory detection
- Automatic wallpaper path mapping
- Shared wallpaper collections
- Font deduplication
- Icon and cursor deduplication
- Theme deduplication
- Side-by-side profile builds
- Update preview
- Update risk reporting
- Rollback to previous builds
- Overlay conflict detection
- Adapter migrations
- Storage cleanup policies

### Phase 4: Developer SDK

**Status: Planned**

- Versioned `dotswitch.toml` schema
- `dotswitch init`
- `dotswitch validate`
- `dotswitch test`
- `dotswitch pack`
- Adapter plugin API
- Local sandbox testing
- Compatibility matrix testing
- Manifest documentation
- Example integration repository
- Maintainer-oriented development workflow

### Phase 5: Registry and user interface

**Status: Planned**

- Community profile registry
- Profile search
- Profile browsing
- Profile installation
- Compatibility-filtered discovery
- Screenshots and profile metadata
- Rofi or Walker interface
- Graphical installation and switching interface
- Automated registry validation
- Licence and attribution checks

### Phase 6: Additional Wayland backends

**Status: Exploratory**

Possible compositor backends:

- niri
- Sway

Possible integration targets:

- DankMaterialShell
- end-4 / illogical-impulse
- HyDE
- JaKooLit Hyprland Dotfiles

Additional concepts:

- host-specific hardware overlays
- cross-compositor shell profiles
- reusable component profiles

These projects and backends are examples under consideration, not promised integrations.

### Phase 7: Desktop environments

**Status: Exploratory**

Possible future backends:

- KDE Plasma
- GNOME
- Cinnamon
- Xfce

Possible later investigations:

- MATE
- Budgie
- COSMIC
- LXQt

Potential functionality includes:

- Plasma Global Theme profiles
- Plasma layout snapshots
- GNOME dconf profiles
- GNOME extension compatibility checks

### Phase 8: Distribution and platform expansion

**Status: Exploratory**

Possible package and platform backends:

- Fedora
- Debian and Ubuntu
- openSUSE
- Gentoo
- NixOS and Home Manager

Potential supporting work:

- distribution-independent capabilities
- package-backend abstraction
- init-system abstraction
- extended compatibility testing

---

## Project status summary

dotswitch is not currently ready for normal desktop use.

The project currently provides an early foundation for:

- profiles
- state
- defaults
- profile metadata
- future activation logic

Real configuration switching must not be considered safe until at least the following exist and have been tested:

- isolated profile roots
- transaction journals
- backups
- rollback
- fallback recovery
- health checks
- failure-injection tests

Until then, dotswitch should be treated as development software.

---

## Long-term vision

dotswitch aims to become a common installation, integration and management platform for Linux desktop setups.

A user should eventually be able to:

```text
detect the current desktop
browse compatible setups
install a setup without overwriting the existing system
test it temporarily
keep customisations attached to each profile
share wallpapers and assets between profiles
update profiles safely
roll back instantly
return to the original desktop at any time
```

For maintainers, the goal is to provide a standard integration format so that new desktop setups can be distributed without requiring another destructive installation script.

The project will begin with a focused and reliable Hyprland implementation before expanding to additional compositors, desktop environments and Linux distributions.

---

## Licence

dotswitch is planned to be released under the GNU General Public License v3.0.

Third-party projects remain owned and licensed by their respective authors and contributors.
