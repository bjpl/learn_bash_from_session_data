"""
Enrichment data for Package Management, Compression, Git tools, and Miscellaneous commands.

This module provides additional metadata (use_cases, gotchas, man_url, related, difficulty,
and extra_flags) for commands that exist in COMMAND_DB but have thin entries missing these
fields. Merge this data into COMMAND_DB to complete the knowledge base.
"""

from typing import Dict, Any

ENRICHMENT_DATA: Dict[str, Dict[str, Any]] = {

    # =========================================================================
    # PACKAGE MANAGEMENT -- System-level
    # =========================================================================

    "apt": {
        "man_url": "https://manpages.debian.org/bookworm/apt/apt.8.en.html",
        "use_cases": [
            "Update package list and upgrade all packages: apt update && apt upgrade -y",
            "Search for packages matching a keyword: apt search nginx",
            "Show detailed information about a package before installing: apt show package-name",
            "List all installed packages for auditing: apt list --installed",
            "Remove a package and its configuration files: apt purge package-name",
        ],
        "gotchas": [
            "apt is designed for interactive terminal use; scripts should use apt-get for a stable CLI interface that will not change output format between releases",
            "Running apt without sudo gives permission errors -- most operations require root",
            "apt update only refreshes the package index; it does not install anything -- you must follow with apt upgrade to actually apply updates",
            "apt autoremove can remove packages that other software still depends on if dependency metadata is stale -- review the list before confirming",
        ],
        "related": ["apt-get", "apt-cache", "dpkg", "snap"],
        "difficulty": "beginner",
        "extra_flags": {
            "--no-install-recommends": "Do not install recommended packages as dependencies",
            "--fix-broken": "Attempt to fix broken dependencies",
            "-f": "Alias for --fix-broken",
            "--dry-run": "Simulate the operation without making changes",
        },
    },

    "apt-get": {
        "man_url": "https://manpages.debian.org/bookworm/apt/apt-get.8.en.html",
        "use_cases": [
            "Install a package non-interactively in a script: apt-get install -y nginx",
            "Upgrade all packages without removing anything: apt-get upgrade -y",
            "Full distribution upgrade that handles dependency changes: apt-get dist-upgrade",
            "Download package source code for inspection: apt-get source package-name",
            "Clean downloaded package cache to free disk space: apt-get clean",
        ],
        "gotchas": [
            "apt-get install will not upgrade already-installed packages to the latest version unless you explicitly pass --only-upgrade or run apt-get upgrade first",
            "apt-get dist-upgrade may remove packages to resolve dependency conflicts -- always review what it proposes before confirming",
            "The -y flag auto-confirms prompts, which is useful in scripts but dangerous if you have not reviewed the planned changes first",
        ],
        "related": ["apt", "apt-cache", "dpkg", "aptitude"],
        "difficulty": "beginner",
        "extra_flags": {
            "--only-upgrade": "Only upgrade already-installed packages, do not install new ones",
            "--no-install-recommends": "Do not install recommended packages",
            "--reinstall": "Reinstall packages that are already installed",
            "-d": "Download only, do not install or unpack",
            "--purge": "Remove packages and their configuration files",
        },
    },

    "apt-cache": {
        "man_url": "https://manpages.debian.org/bookworm/apt/apt-cache.8.en.html",
        "use_cases": [
            "Search for available packages by keyword: apt-cache search web server",
            "Show all available versions of a package: apt-cache showpkg nginx",
            "Display dependencies of a package before installing: apt-cache depends nginx",
            "Find which packages depend on a given package: apt-cache rdepends libssl3",
            "Display package metadata including description and size: apt-cache show nginx",
        ],
        "gotchas": [
            "apt-cache searches the local package index, not the remote repositories -- run apt update first to get current results",
            "apt-cache search uses regex by default, so special characters like + in package names (e.g., g++) need escaping",
        ],
        "related": ["apt", "apt-get", "dpkg", "aptitude"],
        "difficulty": "beginner",
        "extra_flags": {
            "policy": "Show installed and candidate versions plus repository priority",
            "madison": "Show available versions in a tabular format",
            "--names-only": "Search only package names, not descriptions",
        },
    },

    "dpkg": {
        "man_url": "https://man7.org/linux/man-pages/man1/dpkg.1.html",
        "use_cases": [
            "Install a locally downloaded .deb file: dpkg -i package.deb",
            "List all installed packages matching a pattern: dpkg -l 'nginx*'",
            "Find which package owns a specific file: dpkg -S /usr/bin/python3",
            "Show contents of a .deb file without installing: dpkg -c package.deb",
            "Reconfigure a package after installation: dpkg-reconfigure tzdata",
        ],
        "gotchas": [
            "dpkg does not resolve dependencies automatically -- if a .deb requires missing packages, dpkg -i will fail and you must run apt-get install -f to fix the broken state",
            "dpkg --purge removes configuration files too, while dpkg -r leaves them behind -- use --purge only when you want a clean removal",
            "dpkg -l output truncates long package names by default -- pipe through 'dpkg -l | cat' or set COLUMNS=200 for full output",
        ],
        "related": ["apt", "apt-get", "apt-cache"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-i": "Install a .deb package file",
            "-r": "Remove an installed package (leave config files)",
            "-P": "Purge: remove package and configuration files",
            "-l": "List packages matching a pattern",
            "-L": "List files installed by a package",
            "-S": "Search for a package that owns the given file path",
            "-s": "Display status and details of an installed package",
            "-c": "List contents of a .deb archive file",
            "--configure": "Configure an unpacked but not yet configured package",
        },
    },

    "snap": {
        "man_url": "https://snapcraft.io/docs",
        "use_cases": [
            "Install an application as a snap: snap install vlc",
            "List all installed snaps and their versions: snap list",
            "Update all installed snaps to latest versions: snap refresh",
            "Remove a snap application: snap remove vlc",
            "Revert a snap to its previous version after a bad update: snap revert vlc",
        ],
        "gotchas": [
            "Snaps auto-update in the background, which can restart running applications unexpectedly -- use snap refresh --hold to pause updates",
            "Snaps run in a sandboxed environment and may not have access to all system files -- use snap connect to grant additional permissions",
            "Snap applications may start slower than native packages because they mount a squashfs image on each launch",
            "The snap store is Canonical-controlled; not all snaps are open-source even if the snap format is",
        ],
        "related": ["flatpak", "apt", "apt-get"],
        "difficulty": "beginner",
        "extra_flags": {
            "info": "Show detailed information about a snap",
            "find": "Search for snaps in the store",
            "--classic": "Install with classic confinement (full system access)",
            "--channel": "Install from a specific channel (stable, beta, edge)",
            "connections": "Show interface connections for a snap",
        },
    },

    "flatpak": {
        "man_url": "https://www.man7.org/linux/man-pages/man1/flatpak.1.html",
        "use_cases": [
            "Install an application from Flathub: flatpak install flathub org.gimp.GIMP",
            "Run an installed Flatpak application: flatpak run org.gimp.GIMP",
            "Update all installed Flatpak applications: flatpak update",
            "List installed applications and runtimes: flatpak list",
            "Add the Flathub repository: flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
        ],
        "gotchas": [
            "Flatpak uses application IDs (reverse DNS like org.gimp.GIMP) not simple names -- you must know or search for the full ID",
            "Flatpak apps are sandboxed and may not see your home directory or USB drives -- use Flatseal or flatpak override to manage permissions",
            "Runtimes take significant disk space since each app bundles its own dependencies -- use flatpak uninstall --unused to remove orphaned runtimes",
        ],
        "related": ["snap", "apt", "apt-get"],
        "difficulty": "beginner",
        "extra_flags": {
            "search": "Search for available applications by keyword",
            "uninstall": "Remove an installed application",
            "override": "Override application permissions",
            "--user": "Perform the operation for the current user only",
            "--system": "Perform the operation system-wide",
        },
    },

    "yum": {
        "man_url": "https://man7.org/linux/man-pages/man8/yum.8.html",
        "use_cases": [
            "Install a package with automatic dependency resolution: yum install httpd",
            "Update all packages on the system: yum update -y",
            "Search for a package by keyword: yum search web server",
            "List available updates: yum check-update",
            "View transaction history to audit changes: yum history",
        ],
        "gotchas": [
            "yum is replaced by dnf on Fedora 22+ and RHEL 8+ -- on newer systems 'yum' is often just a symlink to dnf",
            "yum localinstall is deprecated; use yum install ./package.rpm instead to install local RPM files",
            "yum update will update the kernel too -- use yum update --exclude=kernel* to skip kernel updates if needed",
        ],
        "related": ["dnf", "rpm", "zypper"],
        "difficulty": "beginner",
        "extra_flags": {
            "info": "Show detailed information about a package",
            "provides": "Find which package provides a given file or capability",
            "groupinstall": "Install a group of related packages",
            "clean all": "Remove all cached package data",
            "history": "View or undo past transactions",
        },
    },

    "dnf": {
        "man_url": "https://man7.org/linux/man-pages/man8/dnf.8.html",
        "use_cases": [
            "Install a package on Fedora or RHEL: dnf install nginx",
            "Upgrade all packages on the system: dnf upgrade --refresh",
            "Search for packages by keyword: dnf search text editor",
            "List all installed packages: dnf list installed",
            "Remove unneeded dependency packages: dnf autoremove",
        ],
        "gotchas": [
            "dnf upgrade is the modern replacement for yum update -- dnf update exists as an alias but upgrade is the canonical command",
            "dnf module commands manage modular content streams (e.g., different Node.js versions) -- forgetting to enable a module stream before installing can give you an unexpected version",
            "dnf history undo can roll back a transaction but may fail if other packages now depend on what was installed",
        ],
        "related": ["yum", "rpm", "zypper"],
        "difficulty": "beginner",
        "extra_flags": {
            "provides": "Find which package provides a file or capability",
            "repolist": "List enabled repositories",
            "module": "Manage modular content streams",
            "group": "Manage package groups",
            "--refresh": "Force refresh of repository metadata before operating",
            "--best": "Try to install the best available version of packages",
            "downgrade": "Downgrade a package to an earlier available version",
        },
    },

    "rpm": {
        "man_url": "https://man7.org/linux/man-pages/man8/rpm.8.html",
        "use_cases": [
            "Install an RPM package file: rpm -ivh package.rpm",
            "Query all installed packages: rpm -qa",
            "Find which package owns a file: rpm -qf /usr/bin/vim",
            "List all files in an installed package: rpm -ql nginx",
            "Verify integrity of installed package files: rpm -V nginx",
        ],
        "gotchas": [
            "rpm does not resolve dependencies -- installing with rpm -i will fail if dependencies are missing; use dnf or yum for dependency resolution",
            "rpm -U (upgrade) removes the old version before installing the new one -- for the kernel, use rpm -i instead so you keep the old kernel as a fallback",
            "rpm -e (erase) will refuse to remove a package if others depend on it -- use --nodeps to force removal, but this can break the system",
        ],
        "related": ["dnf", "yum", "zypper", "rpmbuild"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-i": "Install a package",
            "-U": "Upgrade (or install if not present)",
            "-e": "Erase (remove) a package",
            "-q": "Query mode",
            "-qa": "Query all installed packages",
            "-qf": "Query which package owns a file",
            "-ql": "Query list of files in a package",
            "-V": "Verify installed package against RPM database",
            "-K": "Check package signature and integrity",
            "--import": "Import a GPG public key for package verification",
            "-ivh": "Install with verbose output and progress hash marks",
        },
    },

    "zypper": {
        "man_url": "https://en.opensuse.org/SDB:Zypper_manual",
        "use_cases": [
            "Install a package on openSUSE: zypper install nginx",
            "Refresh all repositories: zypper refresh",
            "Update all installed packages: zypper update",
            "Search for packages by pattern: zypper search pattern",
            "Perform a full distribution upgrade: zypper dist-upgrade",
        ],
        "gotchas": [
            "zypper dist-upgrade (dup) can change vendors and remove packages -- always review the proposed changes and use --dry-run first",
            "zypper locks can prevent packages from being updated -- use zypper locks list to see if any are blocking upgrades",
            "Unlike apt, zypper refresh must be run manually to update repository metadata before searching or installing",
        ],
        "related": ["rpm", "dnf", "yum"],
        "difficulty": "intermediate",
        "extra_flags": {
            "lr": "List all configured repositories",
            "ar": "Add a new repository",
            "rr": "Remove a repository",
            "patch": "Install available patches",
            "se": "Shorthand for search",
            "in": "Shorthand for install",
        },
    },

    "pacman": {
        "man_url": "https://man.archlinux.org/man/pacman.8",
        "use_cases": [
            "Synchronize package databases and upgrade system: pacman -Syu",
            "Install a package from the repositories: pacman -S nginx",
            "Search for a package by name: pacman -Ss web server",
            "Remove a package and its orphaned dependencies: pacman -Rns package-name",
            "Query which package owns a file: pacman -Qo /usr/bin/vim",
        ],
        "gotchas": [
            "Arch is a rolling release -- always run pacman -Syu (full sync) rather than pacman -Sy package, which can cause partial upgrades and break the system",
            "pacman -R will not remove dependencies that were pulled in; use -Rns to also remove orphaned dependencies and config backups",
            "Package signing is enforced by default; if you get signature errors, update the keyring first with pacman -S archlinux-keyring",
        ],
        "related": ["yay", "paru", "makepkg"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-S": "Synchronize: install or upgrade packages from repositories",
            "-R": "Remove an installed package",
            "-Q": "Query the local installed package database",
            "-Syu": "Full system upgrade (sync databases + upgrade)",
            "-Ss": "Search remote repositories for a package",
            "-Qs": "Search locally installed packages",
            "-Qi": "Show detailed info about an installed package",
            "-Qo": "Query which package owns a given file",
            "-Sc": "Clean old packages from the cache",
            "-U": "Install a local package file (.pkg.tar.zst)",
        },
    },

    "yay": {
        "man_url": "https://github.com/Jguer/yay",
        "use_cases": [
            "Install a package from AUR or official repos: yay -S package-name",
            "Full system upgrade including AUR packages: yay -Syu",
            "Search for packages across repos and AUR: yay search-term",
            "Upgrade only AUR packages: yay -Sua",
            "Remove a package: yay -R package-name",
        ],
        "gotchas": [
            "AUR packages are user-submitted and not officially reviewed -- always inspect the PKGBUILD before installing to avoid malicious code",
            "yay builds AUR packages from source, which can take significant time and disk space for large projects",
            "Running yay without arguments triggers a full -Syu upgrade, which may not be intended",
        ],
        "related": ["pacman", "paru", "makepkg"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--gendb": "Generate a development package database for devel updates",
            "--devel": "Check development packages for updates using git",
            "--cleanafter": "Remove build files after installation",
            "--editmenu": "Show a menu to edit PKGBUILDs before building",
        },
    },

    "paru": {
        "man_url": "https://github.com/Morganamilo/paru",
        "use_cases": [
            "Install a package from AUR or official repos: paru -S package-name",
            "Full system upgrade including AUR packages: paru (defaults to -Syu)",
            "Search for packages interactively: paru search-term",
            "View and edit PKGBUILD before installing: paru -S --review package-name",
            "Clean unneeded build dependencies: paru -c",
        ],
        "gotchas": [
            "paru opens the PKGBUILD for review by default before building, which is safer but slower -- set SkipReview in paru.conf to disable",
            "Like yay, running paru without arguments performs a full system upgrade (-Syu)",
            "paru is written in Rust and must be built from source via makepkg since it is an AUR package itself",
        ],
        "related": ["pacman", "yay", "makepkg"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--review": "Review PKGBUILD and related files before building",
            "--skipreview": "Skip PKGBUILD review",
            "--devel": "Update VCS (git/svn) packages",
            "--removemake": "Remove makedepends after installation",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- macOS / BSD
    # =========================================================================

    "brew": {
        "man_url": "https://docs.brew.sh/Manpage",
        "use_cases": [
            "Install a command-line tool: brew install wget",
            "Install a macOS GUI application: brew install --cask firefox",
            "Update Homebrew and upgrade all packages: brew update && brew upgrade",
            "Search for available packages: brew search keyword",
            "List installed packages and check for issues: brew list && brew doctor",
            "Pin a formula to prevent it from being upgraded: brew pin postgresql",
        ],
        "gotchas": [
            "brew update refreshes the formula index; brew upgrade actually installs newer versions -- mixing them up leads to confusion",
            "Homebrew installs into /opt/homebrew on Apple Silicon and /usr/local on Intel Macs -- scripts referencing hardcoded paths may break across architectures",
            "brew doctor reports potential issues and should be run when things break -- it catches common problems like outdated Xcode CLT",
            "Cask apps (--cask) are macOS .app bundles, not CLI tools -- they go to /Applications and may require manual updates",
        ],
        "related": ["port", "apt", "dnf"],
        "difficulty": "beginner",
        "extra_flags": {
            "install": "Install a formula or cask",
            "uninstall": "Remove an installed formula or cask",
            "upgrade": "Upgrade outdated formulae and casks",
            "update": "Fetch the newest version of Homebrew and all formulae",
            "search": "Search for formulae and casks",
            "info": "Display information about a formula or cask",
            "doctor": "Check your system for potential problems",
            "list": "List all installed formulae and casks",
            "pin": "Pin a formula to prevent upgrades",
            "unpin": "Unpin a formula to allow upgrades",
            "cleanup": "Remove old versions of installed formulae",
            "tap": "Add a third-party repository of formulae",
            "services": "Manage background services with macOS launchd",
        },
    },

    "port": {
        "man_url": "https://man.macports.org/port.1.html",
        "use_cases": [
            "Install a package on macOS via MacPorts: sudo port install wget",
            "Update the port tree and upgrade installed packages: sudo port selfupdate && sudo port upgrade outdated",
            "Search for available ports: port search keyword",
            "List installed ports: port installed",
            "Remove inactive (old) versions of ports: sudo port uninstall inactive",
        ],
        "gotchas": [
            "MacPorts installs everything under /opt/local, which means you need to add /opt/local/bin to PATH to find installed commands",
            "MacPorts compiles from source by default, which can be slow -- Homebrew uses prebuilt bottles and is often faster for common packages",
            "Mixing MacPorts and Homebrew on the same system can cause path conflicts and library version mismatches",
        ],
        "related": ["brew", "apt", "dpkg"],
        "difficulty": "intermediate",
        "extra_flags": {
            "selfupdate": "Update MacPorts itself and the port tree",
            "upgrade": "Upgrade installed ports to latest versions",
            "outdated": "List ports that have available upgrades",
            "contents": "List files installed by a port",
            "variants": "Show available build variants for a port",
            "deps": "Show dependencies of a port",
        },
    },

    "pkg": {
        "man_url": "https://man.freebsd.org/cgi/man.cgi?query=pkg&sektion=8",
        "use_cases": [
            "Install a package on FreeBSD: pkg install nginx",
            "Update the package repository catalog: pkg update",
            "Upgrade all installed packages: pkg upgrade",
            "Search for packages by name: pkg search keyword",
            "Remove a package and its unused dependencies: pkg delete -a package-name && pkg autoremove",
        ],
        "gotchas": [
            "On a fresh FreeBSD install, pkg must be bootstrapped on first run -- it will prompt to install itself",
            "pkg lock can prevent accidental upgrades of critical packages but can also block security updates if forgotten",
        ],
        "related": ["apt", "dnf", "pacman"],
        "difficulty": "intermediate",
        "extra_flags": {
            "info": "Display information about an installed package",
            "audit": "Check installed packages for known vulnerabilities",
            "autoremove": "Remove automatically installed orphan packages",
            "lock": "Lock a package to prevent upgrades",
            "which": "Find which package installed a given file",
        },
    },

    "apk": {
        "man_url": "https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper",
        "use_cases": [
            "Install a package in an Alpine Docker container: apk add --no-cache curl",
            "Update package index and upgrade all packages: apk update && apk upgrade",
            "Search for available packages: apk search nginx",
            "Show info about a package: apk info -a nginx",
            "Remove a package: apk del nginx",
        ],
        "gotchas": [
            "Always use --no-cache in Dockerfiles to avoid storing the package index in the image layer, keeping images small",
            "Alpine uses musl libc instead of glibc, so some precompiled binaries from other distros will not work -- you may need to compile from source",
            "apk has no separate update+install step like apt; apk add always fetches the latest index unless you explicitly separate it",
        ],
        "related": ["apt", "dnf", "pacman"],
        "difficulty": "beginner",
        "extra_flags": {
            "--no-cache": "Do not use or update the local package cache",
            "-s": "Simulate the operation without making changes",
            "--virtual": "Create a virtual package for easy grouped removal",
            "-U": "Update repository indexes before operating",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- JavaScript / Node.js
    # =========================================================================

    "npm": {
        "man_url": "https://docs.npmjs.com/cli",
        "use_cases": [
            "Initialize a new project with npm init -y and install dependencies with npm install express",
            "Run project scripts defined in package.json like npm test or npm run build",
            "Audit dependencies for known vulnerabilities with npm audit and fix them with npm audit fix",
            "Publish a package to the npm registry: npm publish",
            "View outdated dependencies: npm outdated",
        ],
        "gotchas": [
            "npm install without --save-dev puts everything in dependencies -- use --save-dev for test/build tools to keep production installs lean",
            "Running npm install without a lockfile or with different npm versions can produce different dependency trees -- always commit package-lock.json",
            "Global installs (npm install -g) can cause permission errors on Linux/macOS if Node was installed via system package manager -- use nvm or configure npm prefix",
            "npm run silently swallows exit codes by default in some cases -- use npm run --if-present for optional scripts",
        ],
        "related": ["npx", "yarn", "pnpm", "bun"],
        "difficulty": "beginner",
        "extra_flags": {
            "ci": "Clean install from lockfile only, ideal for CI/CD pipelines",
            "outdated": "Check for outdated packages",
            "audit": "Run a security audit of installed dependencies",
            "link": "Symlink a local package for development testing",
            "pack": "Create a tarball of the package without publishing",
            "exec": "Run a command from a local or remote npm package",
            "--legacy-peer-deps": "Ignore peerDependency conflicts during install",
            "--omit=dev": "Skip devDependencies during install (replaces --production)",
            "cache clean --force": "Clear the npm cache when troubleshooting installs",
        },
    },

    "npx": {
        "man_url": "https://docs.npmjs.com/cli/commands/npx",
        "use_cases": [
            "Run a package without installing it globally: npx create-react-app my-app",
            "Execute a specific version of a tool: npx node@18 --version",
            "Run a locally installed binary: npx jest --coverage",
            "Initialize a project with a scaffolding tool: npx degit user/repo my-project",
        ],
        "gotchas": [
            "npx downloads packages to a temporary cache and executes them -- this means it may run arbitrary code from npm; always verify what you are running",
            "If the package is not installed locally, npx prompts for confirmation (use -y to auto-confirm or --no to reject)",
            "npx resolves commands from local node_modules/.bin first, then global, then downloads -- behavior can be surprising if a local version differs from what you expect",
        ],
        "related": ["npm", "yarn", "pnpm", "bun"],
        "difficulty": "beginner",
        "extra_flags": {
            "-p": "Specify additional packages to install alongside the command",
            "--no": "Refuse to install any packages not already present",
            "-c": "Execute a string as a shell command with the package available",
        },
    },

    "yarn": {
        "man_url": "https://yarnpkg.com/getting-started",
        "use_cases": [
            "Install all project dependencies: yarn install",
            "Add a new package to the project: yarn add express",
            "Add a development dependency: yarn add --dev typescript",
            "Run a script defined in package.json: yarn run build",
            "Upgrade all dependencies to latest: yarn upgrade-interactive",
        ],
        "gotchas": [
            "Yarn Classic (v1) and Yarn Berry (v2+) have significantly different behaviors -- Berry uses Plug'n'Play by default which eliminates node_modules and may break tools expecting it",
            "yarn install --frozen-lockfile should be used in CI to fail fast if the lockfile is out of date rather than silently updating it",
            "Mixing yarn and npm in the same project creates conflicting lockfiles (yarn.lock vs package-lock.json) -- pick one and stick with it",
            "Yarn workspaces require proper configuration in package.json; forgetting to declare a workspace means its dependencies are not hoisted",
        ],
        "related": ["npm", "pnpm", "bun", "npx"],
        "difficulty": "beginner",
        "extra_flags": {
            "why": "Show why a package is installed (dependency chain)",
            "workspace": "Run a command in a specific workspace",
            "dlx": "Download and execute a package (like npx) in Yarn Berry",
            "dedupe": "Deduplicate dependencies in the lockfile",
            "info": "Show information about a package",
        },
    },

    "pnpm": {
        "man_url": "https://pnpm.io/cli/add",
        "use_cases": [
            "Install all project dependencies: pnpm install",
            "Add a new dependency: pnpm add express",
            "Add a development dependency: pnpm add -D typescript",
            "Run a script from package.json: pnpm run build",
            "Install dependencies in a monorepo workspace: pnpm install --filter @my-org/package-name",
        ],
        "gotchas": [
            "pnpm uses a content-addressable store and hard links, so node_modules has a different structure than npm -- some tools that walk node_modules directly may not work",
            "pnpm is strict about peer dependencies by default, which catches real issues but can be annoying when libraries have sloppy peer dependency declarations -- use --shamefully-hoist as a last resort",
            "pnpm does not hoist packages to the root node_modules by default, so accessing undeclared dependencies fails immediately -- this is by design to enforce correctness",
        ],
        "related": ["npm", "yarn", "bun", "npx"],
        "difficulty": "intermediate",
        "extra_flags": {
            "--filter": "Run commands for specific packages in a monorepo",
            "--shamefully-hoist": "Hoist all packages to root (compatibility escape hatch)",
            "--frozen-lockfile": "Fail if lockfile needs updating (CI mode)",
            "store prune": "Remove unused packages from the content-addressable store",
            "dlx": "Download and execute a package (like npx)",
            "why": "Show why a package is installed",
        },
    },

    "bun": {
        "man_url": "https://bun.sh/docs",
        "use_cases": [
            "Install all project dependencies (fast): bun install",
            "Add a dependency: bun add express",
            "Run a TypeScript file directly without compilation: bun run index.ts",
            "Run tests with the built-in test runner: bun test",
            "Initialize a new project: bun init",
        ],
        "gotchas": [
            "Bun is not 100% Node.js compatible -- some Node.js APIs and native modules may behave differently or be missing; check compatibility before migrating production code",
            "Bun uses its own bun.lockb binary lockfile which is not interchangeable with package-lock.json or yarn.lock",
            "bun run interprets .ts files natively, so TypeScript errors may appear that tsc would catch differently -- Bun transpiles rather than type-checks",
        ],
        "related": ["npm", "yarn", "pnpm", "npx"],
        "difficulty": "beginner",
        "extra_flags": {
            "add": "Add a dependency to the project",
            "remove": "Remove a dependency from the project",
            "update": "Update dependencies to the latest compatible versions",
            "link": "Link a local package for development",
            "pm": "Package manager subcommands (cache, ls, hash)",
            "x": "Execute a package (like npx)",
            "--hot": "Enable hot reloading for development server",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- Python
    # =========================================================================

    "pip": {
        "man_url": "https://pip.pypa.io/en/stable/",
        "use_cases": [
            "Install a package with pip install requests and pin versions with pip install requests==2.31.0",
            "Export current environment dependencies with pip freeze > requirements.txt for reproducibility",
            "Install all project dependencies from a requirements file with pip install -r requirements.txt",
            "Install a package in editable mode for development: pip install -e .",
            "Check for outdated packages: pip list --outdated",
        ],
        "gotchas": [
            "Installing without a virtual environment modifies system Python packages and can break OS tools -- always use python -m venv or conda first",
            "pip install upgrades are not automatic -- use pip install --upgrade package to get the latest version; pip install alone skips already-installed packages",
            "pip does not have a true dependency resolver lock file -- use pip-tools, poetry, or uv for reproducible builds",
            "pip install --user is the fallback when you cannot use a virtual environment, but it puts packages in ~/.local which can cause version conflicts",
        ],
        "related": ["pip3", "pipx", "conda", "poetry", "uv"],
        "difficulty": "beginner",
        "extra_flags": {
            "--user": "Install to the user site-packages directory",
            "--no-deps": "Do not install package dependencies",
            "--pre": "Include pre-release and development versions",
            "--index-url": "Use a custom package index URL",
            "--trusted-host": "Trust a host for package downloads (skip SSL)",
            "show": "Show information about installed packages",
            "check": "Verify installed packages have compatible dependencies",
            "download": "Download packages without installing",
        },
    },

    "pip3": {
        "man_url": "https://pip.pypa.io/en/stable/",
        "use_cases": [
            "Explicitly use Python 3 pip when both Python 2 and 3 are installed: pip3 install flask",
            "Install packages in the user directory: pip3 install --user package-name",
            "Upgrade pip itself: pip3 install --upgrade pip",
        ],
        "gotchas": [
            "On most modern systems, pip and pip3 are the same command since Python 2 is EOL -- but on older systems they may point to different Python versions",
            "Use python3 -m pip instead of pip3 for clarity about which Python interpreter is being used, especially in scripts",
        ],
        "related": ["pip", "pipx", "python3"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "pipx": {
        "man_url": "https://pipx.pypa.io/stable/",
        "use_cases": [
            "Install a Python CLI tool in its own isolated environment: pipx install black",
            "Run a tool once without installing: pipx run cowsay hello",
            "Upgrade an installed tool: pipx upgrade black",
            "List all pipx-installed applications: pipx list",
            "Inject an extra package into a tool's isolated environment: pipx inject black click",
        ],
        "gotchas": [
            "pipx is for end-user applications (CLI tools), not libraries -- if you need a library in your project, use pip inside a virtual environment instead",
            "pipx creates one virtual environment per tool, so disk usage can add up with many tools installed",
            "pipx uses the Python version it was installed with -- if you need a tool to use a specific Python, pass --python python3.12",
        ],
        "related": ["pip", "pip3", "uv"],
        "difficulty": "beginner",
        "extra_flags": {
            "ensurepath": "Add pipx binary directory to PATH if not already present",
            "inject": "Add additional packages into an existing pipx application's environment",
            "reinstall-all": "Reinstall all pipx-managed packages (useful after Python upgrade)",
            "--python": "Specify which Python interpreter to use for the virtual environment",
        },
    },

    "conda": {
        "man_url": "https://docs.conda.io/projects/conda/en/stable/",
        "use_cases": [
            "Create a new environment with specific Python version: conda create -n myenv python=3.11",
            "Activate an environment: conda activate myenv",
            "Install a package: conda install numpy",
            "Export an environment for reproducibility: conda env export > environment.yml",
            "Recreate an environment from a file: conda env create -f environment.yml",
        ],
        "gotchas": [
            "Mixing pip and conda in the same environment can break dependency resolution -- install everything with conda first, then use pip only for packages not in conda channels",
            "conda environments can be large (gigabytes) because conda installs compiled binaries for everything including the Python interpreter itself",
            "The default channel may have older versions -- use conda-forge channel (conda install -c conda-forge package) for more up-to-date packages",
            "conda activate does not work in shell scripts by default -- you must run 'eval \"$(conda shell.bash hook)\"' first or use conda run",
        ],
        "related": ["pip", "poetry", "uv", "mamba"],
        "difficulty": "intermediate",
        "extra_flags": {
            "create": "Create a new environment",
            "activate": "Activate an environment",
            "deactivate": "Deactivate the current environment",
            "env list": "List all environments",
            "env remove": "Delete an environment",
            "clean": "Remove unused packages and caches",
            "-c": "Specify a channel to search for packages",
            "--override-channels": "Ignore default channels",
            "config": "Manage conda configuration",
        },
    },

    "poetry": {
        "man_url": "https://python-poetry.org/docs/",
        "use_cases": [
            "Create a new Python project with pyproject.toml: poetry new my-project",
            "Add a dependency: poetry add requests",
            "Add a development dependency: poetry add --group dev pytest",
            "Install all dependencies from the lock file: poetry install",
            "Build and publish a package to PyPI: poetry build && poetry publish",
        ],
        "gotchas": [
            "Poetry manages its own virtual environments and may create them in unexpected locations -- use poetry env info to find the active environment path",
            "poetry install recreates the virtual environment from poetry.lock, not pyproject.toml -- run poetry lock first if you edited pyproject.toml manually",
            "Poetry does not interoperate well with conda environments -- use one or the other, not both",
            "The poetry shell command spawns a new subshell rather than activating in-place like conda activate",
        ],
        "related": ["pip", "pipx", "conda", "uv"],
        "difficulty": "intermediate",
        "extra_flags": {
            "lock": "Generate the poetry.lock file without installing",
            "show": "Show information about installed packages",
            "run": "Run a command within the project's virtual environment",
            "shell": "Spawn a shell within the project's virtual environment",
            "env": "Manage the project's virtual environment",
            "export": "Export the lock file to other formats (e.g., requirements.txt)",
            "self update": "Update Poetry itself to the latest version",
        },
    },

    "uv": {
        "man_url": "https://docs.astral.sh/uv/",
        "use_cases": [
            "Create a virtual environment and install packages extremely fast: uv venv && uv pip install flask",
            "Install packages from requirements.txt: uv pip install -r requirements.txt",
            "Create a new Python project: uv init my-project",
            "Run a Python script with automatic dependency resolution: uv run script.py",
            "Install and manage Python versions: uv python install 3.12",
        ],
        "gotchas": [
            "uv is written in Rust and is 10-100x faster than pip, but it is a newer tool and may have edge cases with complex dependency trees",
            "uv pip compile generates locked requirements from pyproject.toml, similar to pip-tools -- but the output format may differ slightly",
            "uv automatically downloads Python versions if needed, which is convenient but may be unexpected in air-gapped environments",
        ],
        "related": ["pip", "poetry", "pipx", "conda"],
        "difficulty": "beginner",
        "extra_flags": {
            "venv": "Create a virtual environment",
            "pip install": "Install packages (pip-compatible interface)",
            "pip compile": "Compile requirements.in to requirements.txt",
            "pip sync": "Sync environment to match requirements exactly",
            "run": "Run a command or script in a project environment",
            "add": "Add a dependency to the project",
            "lock": "Generate a lockfile for the project",
            "python": "Manage Python installations",
            "tool": "Install and run Python CLI tools (like pipx)",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- Rust
    # =========================================================================

    "cargo": {
        "man_url": "https://doc.rust-lang.org/cargo/",
        "use_cases": [
            "Create a new Rust project: cargo new my-project",
            "Build the project in debug mode: cargo build",
            "Build an optimized release binary: cargo build --release",
            "Run tests: cargo test",
            "Add a dependency from crates.io: cargo add serde",
            "Check code without producing a binary (fast feedback): cargo check",
            "Generate and open documentation: cargo doc --open",
        ],
        "gotchas": [
            "cargo build defaults to debug mode with no optimizations -- always use --release for production builds or benchmarks",
            "Cargo.lock should be committed for binaries but not for libraries -- libraries let downstream consumers resolve versions",
            "cargo update updates Cargo.lock to latest compatible versions but does not change Cargo.toml version constraints",
            "Large dependency trees can make initial builds slow -- use cargo check instead of cargo build during development for faster feedback",
        ],
        "related": ["rustup", "rustc"],
        "difficulty": "intermediate",
        "extra_flags": {
            "new": "Create a new Cargo project (binary or library)",
            "init": "Initialize Cargo in an existing directory",
            "build": "Compile the current project",
            "run": "Build and execute the binary",
            "test": "Run the test suite",
            "check": "Analyze code without producing binary output",
            "clippy": "Run the Clippy linter for idiomatic Rust suggestions",
            "fmt": "Format source code according to Rust style guidelines",
            "doc": "Generate HTML documentation for the project",
            "add": "Add a dependency to Cargo.toml",
            "remove": "Remove a dependency from Cargo.toml",
            "publish": "Publish the crate to crates.io",
            "bench": "Run benchmarks",
            "update": "Update Cargo.lock to latest compatible versions",
            "--workspace": "Operate on all workspace members",
        },
    },

    "rustup": {
        "man_url": "https://rust-lang.github.io/rustup/",
        "use_cases": [
            "Install the stable Rust toolchain: rustup install stable",
            "Switch to the nightly toolchain: rustup default nightly",
            "Add a compilation target for cross-compiling: rustup target add wasm32-unknown-unknown",
            "Update all installed toolchains: rustup update",
            "Install a specific component like Clippy: rustup component add clippy",
        ],
        "gotchas": [
            "rustup override set nightly applies only to the current directory -- it does not change your global default",
            "Nightly toolchains can break between days -- use rustup run nightly-2024-01-15 to pin a specific date",
            "rustup self update updates rustup itself, while rustup update updates the Rust toolchains -- they are different operations",
        ],
        "related": ["cargo", "rustc"],
        "difficulty": "intermediate",
        "extra_flags": {
            "show": "Show the active and installed toolchains",
            "default": "Set the default toolchain",
            "override": "Set a directory-level toolchain override",
            "target": "Manage compilation targets",
            "component": "Manage toolchain components (clippy, rustfmt, etc.)",
            "self update": "Update rustup itself",
            "toolchain": "Manage installed toolchains",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- Ruby
    # =========================================================================

    "gem": {
        "man_url": "https://guides.rubygems.org/rubygems-basics/",
        "use_cases": [
            "Install a Ruby gem: gem install rails",
            "List installed gems: gem list",
            "Update a specific gem: gem update nokogiri",
            "Search for available gems: gem search json",
            "Uninstall a gem: gem uninstall rails",
        ],
        "gotchas": [
            "Installing gems without a version manager (rbenv, rvm) can pollute the system Ruby and require sudo -- always use a Ruby version manager",
            "gem install does not respect Gemfile constraints -- use bundle install for project-level dependency management",
            "Some gems require native C extensions and need build tools (gcc, make) and system libraries to compile during installation",
        ],
        "related": ["bundle", "ruby", "rbenv"],
        "difficulty": "beginner",
        "extra_flags": {
            "-v": "Install a specific version of a gem",
            "--no-document": "Skip generating documentation during install (faster)",
            "environment": "Show RubyGems environment info (paths, config)",
            "pristine": "Restore installed gems to their original state",
            "cleanup": "Remove old versions of installed gems",
        },
    },

    "bundle": {
        "man_url": "https://bundler.io/man/bundle.1.html",
        "use_cases": [
            "Install all gems listed in the Gemfile: bundle install",
            "Execute a command in the context of the bundle: bundle exec rails server",
            "Update all gems to latest allowed versions: bundle update",
            "Add a gem to the Gemfile and install it: bundle add nokogiri",
            "Generate a Gemfile.lock for reproducible installs: bundle lock",
        ],
        "gotchas": [
            "Always use bundle exec to run project commands (e.g., bundle exec rake) to ensure the correct gem versions are loaded from Gemfile.lock",
            "bundle install in deployment mode (--deployment) installs to vendor/bundle and is strict about the lockfile -- this is what CI/CD should use",
            "Gemfile.lock must be committed to version control for applications (not for libraries) to ensure reproducible builds",
        ],
        "related": ["gem", "ruby", "rbenv"],
        "difficulty": "intermediate",
        "extra_flags": {
            "exec": "Run a command using the gems in the Gemfile",
            "--deployment": "Install in deployment mode (strict lockfile, vendor directory)",
            "--without": "Exclude gem groups from installation",
            "--jobs": "Number of parallel gem installation jobs",
            "--path": "Install gems to a specific directory",
            "config": "Manage bundler configuration",
            "outdated": "List gems with newer versions available",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- PHP
    # =========================================================================

    "composer": {
        "man_url": "https://getcomposer.org/doc/",
        "use_cases": [
            "Install all dependencies from composer.json: composer install",
            "Add a package: composer require monolog/monolog",
            "Add a development dependency: composer require --dev phpunit/phpunit",
            "Update all dependencies: composer update",
            "Create a new project from a package: composer create-project laravel/laravel my-app",
        ],
        "gotchas": [
            "composer install installs from composer.lock (reproducible); composer update resolves new versions and rewrites the lock file -- do not use update in production deployments",
            "Composer installs packages to vendor/ and generates an autoloader -- always include vendor/autoload.php in your code",
            "Running Composer as root is discouraged and will display a warning -- it can lead to file permission issues",
        ],
        "related": ["php", "pecl"],
        "difficulty": "intermediate",
        "extra_flags": {
            "require": "Add a package to composer.json and install it",
            "remove": "Remove a package from composer.json",
            "dump-autoload": "Regenerate the autoloader files",
            "show": "Show information about installed packages",
            "outdated": "List packages with available updates",
            "--no-dev": "Skip installing packages from require-dev",
            "--optimize-autoloader": "Generate optimized autoloader for production",
            "global": "Run commands in the global composer directory",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- Go
    # =========================================================================

    "go": {
        "man_url": "https://pkg.go.dev/cmd/go",
        "use_cases": [
            "Initialize a new Go module: go mod init github.com/user/project",
            "Build and run a Go program: go run main.go",
            "Run all tests in the project: go test ./...",
            "Add a dependency: go get github.com/gin-gonic/gin",
            "Tidy up unused dependencies: go mod tidy",
            "Build a static binary: CGO_ENABLED=0 go build -o myapp",
        ],
        "gotchas": [
            "go get now only updates go.mod -- use go install to install executables; go get no longer builds and installs binaries",
            "go mod tidy can remove indirect dependencies that are actually needed -- always run tests after tidying",
            "Go module proxy (GOPROXY) caches modules and can serve stale versions -- set GONOSUMCHECK or GOFLAGS=-mod=mod when debugging dependency issues",
        ],
        "related": ["gofmt", "golint", "delve"],
        "difficulty": "intermediate",
        "extra_flags": {
            "mod init": "Initialize a new Go module in the current directory",
            "mod tidy": "Add missing and remove unused dependencies",
            "install": "Compile and install a Go executable to GOPATH/bin",
            "vet": "Report suspicious constructs in Go code",
            "generate": "Run code generation directives in source files",
            "work": "Manage Go workspaces for multi-module development",
            "-ldflags": "Pass flags to the linker (e.g., to set version at build time)",
            "-trimpath": "Remove filesystem paths from compiled binary",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- .NET
    # =========================================================================

    "nuget": {
        "man_url": "https://learn.microsoft.com/en-us/nuget/reference/nuget-exe-cli-reference",
        "use_cases": [
            "Restore packages for a .NET project: nuget restore solution.sln",
            "Install a package to a project: nuget install Newtonsoft.Json",
            "Pack a project into a .nupkg file: nuget pack MyProject.nuspec",
            "Push a package to the NuGet gallery: nuget push package.nupkg -Source nuget.org",
            "List package sources: nuget sources list",
        ],
        "gotchas": [
            "For .NET Core and .NET 5+ projects, prefer dotnet nuget commands over nuget.exe -- nuget.exe is primarily for .NET Framework projects",
            "nuget.exe is Windows-only by default; on macOS/Linux use dotnet CLI or Mono-based nuget",
            "NuGet package restore can fail in CI if the package source is not configured -- ensure nuget.config is committed with the project",
        ],
        "related": ["dotnet", "msbuild"],
        "difficulty": "intermediate",
        "extra_flags": {
            "restore": "Restore packages for a solution or project",
            "pack": "Create a NuGet package from a project or nuspec",
            "push": "Publish a package to a NuGet server",
            "sources": "Manage NuGet package sources",
            "config": "Get or set NuGet configuration values",
            "-Source": "Specify the package source URL",
            "-ApiKey": "API key for publishing packages",
        },
    },

    "dotnet": {
        "man_url": "https://learn.microsoft.com/en-us/dotnet/core/tools/",
        "use_cases": [
            "Create a new project from a template: dotnet new webapi -n MyApi",
            "Build the project: dotnet build",
            "Run the application: dotnet run",
            "Run tests: dotnet test",
            "Publish a self-contained application: dotnet publish -c Release --self-contained",
            "Add a NuGet package: dotnet add package Newtonsoft.Json",
        ],
        "gotchas": [
            "dotnet run compiles and runs in debug mode by default -- use -c Release for production-like performance during development testing",
            "dotnet restore is run implicitly by build, run, and test -- explicit restore is only needed in CI environments with --no-restore later",
            "Self-contained deployments (--self-contained) bundle the runtime and can be very large; use trimming (--self-contained -p:PublishTrimmed=true) to reduce size",
        ],
        "related": ["nuget", "msbuild"],
        "difficulty": "intermediate",
        "extra_flags": {
            "new": "Create a new project, solution, or file from a template",
            "restore": "Restore NuGet dependencies",
            "publish": "Publish the application for deployment",
            "add package": "Add a NuGet package reference to the project",
            "add reference": "Add a project-to-project reference",
            "tool install": "Install a .NET global or local tool",
            "ef": "Entity Framework Core CLI commands (migrations, database)",
            "--runtime": "Specify the target runtime identifier (e.g., linux-x64)",
            "watch": "Watch for file changes and rerun the command",
        },
    },

    # =========================================================================
    # PACKAGE MANAGEMENT -- Java / JVM
    # =========================================================================

    "mvn": {
        "man_url": "https://maven.apache.org/run.html",
        "use_cases": [
            "Compile the project: mvn compile",
            "Run tests: mvn test",
            "Package the project as a JAR or WAR: mvn package",
            "Install the artifact to the local Maven repository: mvn install",
            "Clean build artifacts and rebuild: mvn clean install",
            "Generate a project from an archetype: mvn archetype:generate",
        ],
        "gotchas": [
            "Maven downloads the entire internet on first run (all dependencies) -- use mvn dependency:go-offline to pre-download for air-gapped builds",
            "mvn install puts artifacts in ~/.m2/repository which can grow very large over time -- periodically clean it manually",
            "Maven's verbose output makes errors hard to find -- use mvn -q for quiet mode or pipe through grep to find ERROR lines",
            "The pom.xml is XML and easy to make syntax errors in -- use mvn validate to check for basic POM errors",
        ],
        "related": ["gradle", "java", "javac"],
        "difficulty": "intermediate",
        "extra_flags": {
            "clean": "Delete the target directory with build artifacts",
            "verify": "Run integration tests",
            "deploy": "Copy the artifact to a remote repository",
            "-DskipTests": "Skip running tests during build",
            "-pl": "Build specific modules in a multi-module project",
            "-am": "Also build dependent modules",
            "-U": "Force update of snapshots from remote repositories",
            "-o": "Work offline (use only local repository)",
            "-B": "Run in non-interactive batch mode",
            "-X": "Enable debug output for troubleshooting",
        },
    },

    "gradle": {
        "man_url": "https://docs.gradle.org/current/userguide/command_line_interface.html",
        "use_cases": [
            "Build the project: gradle build",
            "Run tests: gradle test",
            "Run the application: gradle run",
            "Clean build artifacts and rebuild: gradle clean build",
            "List available tasks: gradle tasks",
            "Build multiple subprojects in parallel: gradle build --parallel",
        ],
        "gotchas": [
            "Use the Gradle wrapper (./gradlew) instead of the system gradle command to ensure the correct Gradle version for each project",
            "Gradle's daemon stays in memory between builds for speed but can consume significant RAM -- use gradle --stop to kill it",
            "Gradle uses Groovy DSL (build.gradle) or Kotlin DSL (build.gradle.kts) -- they are not interchangeable and have different syntax",
            "The --continuous flag watches for file changes and re-runs tasks automatically, but it can miss changes in some edge cases",
        ],
        "related": ["mvn", "java", "javac"],
        "difficulty": "intermediate",
        "extra_flags": {
            "tasks": "List all available tasks in the project",
            "dependencies": "Display dependency tree",
            "--daemon": "Run using the Gradle daemon (default)",
            "--no-daemon": "Run without the Gradle daemon",
            "--stop": "Stop the Gradle daemon",
            "--refresh-dependencies": "Force refresh of all dependencies",
            "--scan": "Create a build scan for debugging build issues",
            "-x": "Exclude a task from execution",
            "--stacktrace": "Print full stack trace on error",
        },
    },

    # =========================================================================
    # COMPRESSION COMMANDS
    # =========================================================================

    "gzip": {
        "man_url": "https://www.gnu.org/software/gzip/manual/gzip.html",
        "use_cases": [
            "Compress a file (replaces original with .gz): gzip file.txt",
            "Compress while keeping the original: gzip -k file.txt",
            "Compress with best compression ratio: gzip -9 file.txt",
            "Decompress a .gz file: gzip -d file.txt.gz",
            "Compress all files in a directory recursively: gzip -r directory/",
            "View compression ratio without decompressing: gzip -l file.txt.gz",
        ],
        "gotchas": [
            "gzip replaces the original file by default -- use -k to keep the original, or redirect: gzip -c file > file.gz",
            "gzip only compresses single files; it does not create archives of multiple files -- use tar czf for multiple files",
            "gzip compression level (-1 to -9) trades speed for compression ratio; the default -6 is usually a good balance",
        ],
        "related": ["gunzip", "zcat", "bzip2", "xz", "zstd"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Write to stdout, keep original files",
            "-r": "Recursively compress files in a directory",
            "-l": "List compression statistics",
            "-t": "Test compressed file integrity",
            "-f": "Force compression even if output file exists",
            "-1": "Fastest compression (least compression ratio)",
            "-6": "Default compression level (balanced)",
        },
    },

    "gunzip": {
        "man_url": "https://www.gnu.org/software/gzip/manual/gzip.html",
        "use_cases": [
            "Decompress a .gz file: gunzip file.txt.gz",
            "Decompress and keep the original .gz file: gunzip -k file.txt.gz",
            "View compression statistics without decompressing: gunzip -l file.gz",
            "Test file integrity: gunzip -t file.gz",
        ],
        "gotchas": [
            "gunzip is equivalent to gzip -d -- they are the same program; use whichever is more readable in your context",
            "gunzip deletes the .gz file after decompression by default -- use -k to keep both files",
            "If the output file already exists, gunzip will refuse to overwrite unless -f is passed",
        ],
        "related": ["gzip", "zcat", "bzip2", "xz"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "bzip2": {
        "man_url": "https://sourceware.org/bzip2/manual/manual.html",
        "use_cases": [
            "Compress a file with higher ratio than gzip: bzip2 file.txt",
            "Compress while keeping the original: bzip2 -k file.txt",
            "Decompress a .bz2 file: bzip2 -d file.txt.bz2",
            "Test integrity of a compressed file: bzip2 -t file.bz2",
        ],
        "gotchas": [
            "bzip2 is significantly slower than gzip for both compression and decompression -- use it only when the better compression ratio matters",
            "bzip2 replaces the original file by default, just like gzip -- use -k to keep the original",
            "bzip2 does not support compression levels like gzip; its block size (-1 through -9) controls memory usage, not compression quality in the same way",
        ],
        "related": ["bunzip2", "bzcat", "gzip", "xz", "zstd"],
        "difficulty": "beginner",
        "extra_flags": {
            "-c": "Write to stdout, keep original files",
            "-v": "Verbose: show compression ratio for each file",
            "-f": "Force overwrite of output files",
            "-s": "Reduce memory usage at the cost of compression ratio",
        },
    },

    "bunzip2": {
        "man_url": "https://sourceware.org/bzip2/manual/manual.html",
        "use_cases": [
            "Decompress a .bz2 file: bunzip2 file.txt.bz2",
            "Decompress and keep the original: bunzip2 -k file.txt.bz2",
            "Decompress to stdout for piping: bunzip2 -c file.bz2 | grep pattern",
        ],
        "gotchas": [
            "bunzip2 is equivalent to bzip2 -d -- they are the same program",
            "bunzip2 removes the .bz2 file after decompression by default -- use -k to keep it",
        ],
        "related": ["bzip2", "bzcat", "gunzip", "unxz"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "xz": {
        "man_url": "https://man7.org/linux/man-pages/man1/xz.1.html",
        "use_cases": [
            "Compress a file with very high compression ratio: xz file.txt",
            "Compress while keeping the original: xz -k file.txt",
            "Decompress an .xz file: xz -d file.txt.xz",
            "Use multiple CPU cores for compression: xz -T0 file.txt",
            "Compress with maximum ratio: xz -9 file.txt",
        ],
        "gotchas": [
            "xz achieves the best compression ratio of common tools but is much slower than gzip or zstd -- use it for archival, not real-time compression",
            "xz -9 uses significant memory (up to ~674 MB) -- on low-memory systems, use -6 or lower",
            "xz replaces the original file by default -- use -k to keep the original",
            "Threaded compression (-T0) produces different output than single-threaded, so checksums will differ for the same input",
        ],
        "related": ["unxz", "xzcat", "gzip", "bzip2", "zstd"],
        "difficulty": "beginner",
        "extra_flags": {
            "-T": "Set number of compression threads (0 = auto-detect CPU count)",
            "-c": "Write to stdout, keep original files",
            "-l": "List information about .xz files",
            "-t": "Test compressed file integrity",
            "-e": "Use extreme compression (slower but slightly smaller)",
        },
    },

    "unxz": {
        "man_url": "https://man7.org/linux/man-pages/man1/xz.1.html",
        "use_cases": [
            "Decompress an .xz file: unxz file.txt.xz",
            "Decompress while keeping the original: unxz -k file.txt.xz",
        ],
        "gotchas": [
            "unxz is equivalent to xz --decompress -- they are the same program",
            "unxz removes the .xz file after decompression by default",
        ],
        "related": ["xz", "xzcat", "gunzip", "bunzip2"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "zip": {
        "man_url": "https://linux.die.net/man/1/zip",
        "use_cases": [
            "Create a zip archive from multiple files: zip archive.zip file1.txt file2.txt",
            "Recursively zip a directory: zip -r archive.zip directory/",
            "Add files to an existing zip archive: zip archive.zip newfile.txt",
            "Create a password-protected zip: zip -e secure.zip secrets.txt",
            "Exclude specific patterns: zip -r archive.zip dir/ -x '*.log'",
        ],
        "gotchas": [
            "zip does not compress as well as gzip, bzip2, or xz for individual files -- its advantage is the archive format that Windows and macOS natively support",
            "zip -r is required for directories; without -r, zip only adds files in the current directory level",
            "zip encryption (-e) uses the legacy ZipCrypto algorithm which is weak -- use 7z or gpg for real security",
            "File permissions and symlinks may not be preserved in zip archives across different operating systems",
        ],
        "related": ["unzip", "tar", "gzip", "7z"],
        "difficulty": "beginner",
        "extra_flags": {
            "-j": "Junk (do not record) directory names -- store just the filenames",
            "-u": "Update existing entries only if newer",
            "-d": "Delete entries from a zip archive",
            "-x": "Exclude files matching the given patterns",
            "-q": "Quiet mode (suppress output)",
            "-0": "Store only (no compression)",
            "-T": "Test archive integrity after creation",
            "-s": "Create a split archive with specified size",
        },
    },

    "unzip": {
        "man_url": "https://linux.die.net/man/1/unzip",
        "use_cases": [
            "Extract all files from a zip archive: unzip archive.zip",
            "Extract to a specific directory: unzip archive.zip -d /tmp/output",
            "List contents of a zip without extracting: unzip -l archive.zip",
            "Extract only specific files: unzip archive.zip '*.txt'",
            "Test archive integrity: unzip -t archive.zip",
        ],
        "gotchas": [
            "unzip extracts to the current directory by default, which can be messy -- always use -d to specify a target directory",
            "unzip will prompt before overwriting existing files unless -o (overwrite) is passed",
            "Zip archives created on Windows may have filenames in non-UTF-8 encoding, causing garbled names on Linux -- use unzip -O CP437 as a workaround",
            "unzip cannot handle .gz or .tar.gz files -- those require gunzip or tar xzf respectively",
        ],
        "related": ["zip", "tar", "7z"],
        "difficulty": "beginner",
        "extra_flags": {
            "-q": "Quiet mode (suppress output except errors)",
            "-n": "Never overwrite existing files",
            "-j": "Junk paths (extract flat without directory structure)",
            "-p": "Extract to stdout (for piping)",
            "-Z": "Display archive information in zipinfo format",
        },
    },

    "7z": {
        "man_url": "https://linux.die.net/man/1/7z",
        "use_cases": [
            "Create a 7z archive: 7z a archive.7z file1.txt file2.txt",
            "Extract a 7z archive: 7z x archive.7z",
            "List contents of an archive: 7z l archive.7z",
            "Create a password-protected archive: 7z a -p archive.7z sensitive/",
            "Create a zip-format archive with 7z: 7z a archive.zip directory/",
        ],
        "gotchas": [
            "7z achieves the best compression but is slower than gzip or zstd -- use it for archival and distribution, not real-time compression",
            "7z e extracts files flat (no directory structure); use 7z x to preserve the directory tree",
            "The 7z format does not preserve Unix file permissions or ownership -- use tar inside 7z for Unix systems",
            "Different 7z packages exist on Linux: p7zip-full provides 7z, while p7zip provides only 7za (fewer formats)",
        ],
        "related": ["7za", "zip", "unzip", "tar"],
        "difficulty": "intermediate",
        "extra_flags": {
            "a": "Add files to an archive (create or append)",
            "x": "Extract with full directory paths",
            "e": "Extract files to current directory (flat, no paths)",
            "l": "List contents of an archive",
            "t": "Test archive integrity",
            "u": "Update files in an archive",
            "-p": "Set password for encryption/decryption",
            "-mx": "Set compression level (0=store, 9=ultra)",
            "-t": "Set archive type (7z, zip, gzip, bzip2, tar)",
            "-v": "Create multi-volume (split) archives",
        },
    },

    "7za": {
        "man_url": "https://linux.die.net/man/1/7za",
        "use_cases": [
            "Create a 7z archive with the standalone version: 7za a archive.7z files/",
            "Extract an archive: 7za x archive.7z",
            "Test archive integrity: 7za t archive.7z",
        ],
        "gotchas": [
            "7za is a standalone version of 7z with fewer supported formats -- it handles 7z, xz, lzma, and a few others but not all formats 7z supports",
            "For full format support (zip, rar, cab, etc.), install p7zip-full which provides 7z instead of 7za",
        ],
        "related": ["7z", "zip", "tar"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "rar": {
        "man_url": "https://linux.die.net/man/1/rar",
        "use_cases": [
            "Create a RAR archive: rar a archive.rar file1.txt file2.txt",
            "Create a password-protected archive: rar a -p archive.rar secret/",
            "Create a split archive: rar a -v100m archive.rar largefile.bin",
            "Update an existing archive: rar u archive.rar newfile.txt",
        ],
        "gotchas": [
            "RAR is a proprietary format; the rar command for creating archives is not free software and requires a license",
            "For extraction only, use unrar which is available as freeware on most Linux distributions",
            "RAR format is less common on Unix systems; prefer tar+gzip/xz/zstd for Unix-to-Unix transfers",
        ],
        "related": ["unrar", "7z", "zip", "tar"],
        "difficulty": "intermediate",
        "extra_flags": {
            "a": "Add files to archive",
            "x": "Extract with full path",
            "e": "Extract to current directory (flat)",
            "t": "Test archive files",
            "-v": "Create split volumes of specified size",
            "-r": "Recurse into subdirectories",
            "-m5": "Set maximum compression",
        },
    },

    "unrar": {
        "man_url": "https://linux.die.net/man/1/unrar",
        "use_cases": [
            "Extract a RAR archive: unrar x archive.rar",
            "Extract to a specific directory: unrar x archive.rar /tmp/output/",
            "List contents of a RAR archive: unrar l archive.rar",
            "Test archive integrity: unrar t archive.rar",
        ],
        "gotchas": [
            "unrar x preserves directory structure; unrar e extracts all files flat to the current directory",
            "unrar is freeware but not open source (there is also an open-source unrar-free with less format support)",
        ],
        "related": ["rar", "7z", "unzip"],
        "difficulty": "beginner",
        "extra_flags": {
            "x": "Extract with full path",
            "e": "Extract to current directory (flat, no paths)",
            "l": "List archive contents",
            "t": "Test archive integrity",
            "-o+": "Overwrite existing files without prompting",
            "-o-": "Never overwrite existing files",
        },
    },

    "zstd": {
        "man_url": "https://facebook.github.io/zstd/zstd_manual.html",
        "use_cases": [
            "Compress a file: zstd file.txt",
            "Compress with best ratio: zstd -19 file.txt",
            "Compress ultra-fast: zstd --fast file.txt",
            "Decompress a .zst file: zstd -d file.txt.zst",
            "Use multiple CPU cores: zstd -T0 file.txt",
            "Compress while keeping the original: zstd -k file.txt",
        ],
        "gotchas": [
            "zstd supports compression levels from -7 (fast) to 22 (ultra) plus --fast levels -- the default level 3 is usually optimal for most use cases",
            "zstd replaces the original file by default -- use -k to keep the original",
            "While zstd is faster than gzip at comparable compression ratios, the .zst format is not as universally supported -- check that your target systems have zstd installed",
            "The --train option creates a dictionary from sample files for better compression of small, similar files (like JSON logs)",
        ],
        "related": ["gzip", "bzip2", "xz", "lz4"],
        "difficulty": "beginner",
        "extra_flags": {
            "-T": "Number of compression threads (0 = auto)",
            "--fast": "Ultra-fast compression (trade ratio for speed)",
            "--train": "Train a dictionary from sample files",
            "-D": "Use a dictionary for compression/decompression",
            "--rm": "Remove source file after compression (explicit default)",
            "-c": "Write to stdout",
            "--long": "Enable long-distance matching for large files",
            "-19": "High compression level (slower, smaller output)",
        },
    },

    "compress": {
        "man_url": "https://linux.die.net/man/1/compress",
        "use_cases": [
            "Compress a file (creates .Z file): compress file.txt",
            "Decompress a .Z file: compress -d file.Z",
            "Write compressed output to stdout: compress -c file.txt > file.Z",
        ],
        "gotchas": [
            "compress uses the LZW algorithm and is largely obsolete -- gzip, bzip2, xz, and zstd all provide better compression",
            "compress creates .Z files which are rarely seen on modern systems",
            "compress may not be installed by default on modern Linux distributions",
        ],
        "related": ["uncompress", "gzip", "bzip2"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-c": "Write to stdout, keep original file",
            "-f": "Force compression even if .Z file already exists",
            "-v": "Verbose: print compression ratio",
        },
    },

    "uncompress": {
        "man_url": "https://linux.die.net/man/1/uncompress",
        "use_cases": [
            "Decompress a .Z file: uncompress file.Z",
            "Decompress to stdout for piping: uncompress -c file.Z | grep pattern",
        ],
        "gotchas": [
            "uncompress is equivalent to compress -d -- it decompresses .Z files created by the compress command",
            "If you encounter .Z files, gzip can also decompress them: gunzip file.Z",
        ],
        "related": ["compress", "gunzip"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "lz4": {
        "man_url": "https://github.com/lz4/lz4/blob/dev/programs/lz4.1.md",
        "use_cases": [
            "Compress a file extremely fast: lz4 file.txt",
            "Decompress a .lz4 file: lz4 -d file.lz4",
            "Compress with higher ratio (slower): lz4 -9 file.txt",
            "Compress and keep the original: lz4 -k file.txt",
            "Benchmark compression speed: lz4 -b file.txt",
        ],
        "gotchas": [
            "lz4 prioritizes speed over compression ratio -- files will be larger than gzip output but compress/decompress much faster",
            "lz4 is ideal for real-time applications like filesystem compression (btrfs/zfs), database pages, and network compression",
            "lz4 replaces the original file by default -- use -k to keep it",
        ],
        "related": ["zstd", "gzip", "lzop"],
        "difficulty": "beginner",
        "extra_flags": {
            "-b": "Benchmark mode: measure compression/decompression speed",
            "-B": "Set block size for compression",
            "--content-size": "Store original content size in the frame header",
        },
    },

    "lzop": {
        "man_url": "https://www.lzop.org/lzop_man.php",
        "use_cases": [
            "Compress a file fast: lzop file.txt",
            "Decompress a .lzo file: lzop -d file.lzo",
            "Compress with best ratio: lzop -9 file.txt",
            "Test archive integrity: lzop -t file.lzo",
        ],
        "gotchas": [
            "lzop is an older speed-focused compressor; lz4 and zstd have largely replaced it for most use cases",
            "lzop replaces the original file by default -- use -k to keep it",
        ],
        "related": ["lz4", "gzip", "zstd"],
        "difficulty": "intermediate",
        "extra_flags": {},
    },

    "zcat": {
        "man_url": "https://www.gnu.org/software/gzip/manual/gzip.html",
        "use_cases": [
            "View compressed log file without decompressing: zcat access.log.gz",
            "Pipe compressed data to grep: zcat file.gz | grep pattern",
            "Count lines in a compressed file: zcat file.gz | wc -l",
        ],
        "gotchas": [
            "zcat is equivalent to gzip -dc (decompress to stdout) -- it does not modify the original .gz file",
            "On some systems (macOS), zcat expects a .Z suffix; use gzcat or gzip -dc for .gz files instead",
        ],
        "related": ["gzip", "gunzip", "bzcat", "xzcat"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "bzcat": {
        "man_url": "https://sourceware.org/bzip2/manual/manual.html",
        "use_cases": [
            "View a bzip2-compressed file without decompressing: bzcat file.bz2",
            "Pipe compressed data to another command: bzcat data.bz2 | sort | uniq",
        ],
        "gotchas": [
            "bzcat is equivalent to bzip2 -dc -- it decompresses to stdout without modifying the original file",
        ],
        "related": ["bzip2", "bunzip2", "zcat", "xzcat"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "xzcat": {
        "man_url": "https://man7.org/linux/man-pages/man1/xz.1.html",
        "use_cases": [
            "View an xz-compressed file without decompressing: xzcat file.xz",
            "Pipe compressed data to grep: xzcat data.xz | grep pattern",
            "Extract a tar archive compressed with xz: xzcat archive.tar.xz | tar xf -",
        ],
        "gotchas": [
            "xzcat is equivalent to xz --decompress --stdout -- it does not modify the original file",
        ],
        "related": ["xz", "unxz", "zcat", "bzcat"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    # =========================================================================
    # GIT-RELATED TOOLS
    # =========================================================================

    "gh": {
        "man_url": "https://cli.github.com/manual/",
        "use_cases": [
            "Clone a repo by shorthand: gh repo clone owner/repo",
            "Create a pull request from the current branch: gh pr create --fill",
            "List and filter issues: gh issue list --label bug --state open",
            "View CI/CD workflow run status: gh run list",
            "Make an authenticated GitHub API request: gh api repos/owner/repo/releases",
            "Create a new repo from the current directory: gh repo create my-repo --public --source=.",
        ],
        "gotchas": [
            "gh requires authentication first -- run gh auth login before any operations; it supports both browser-based OAuth and personal access tokens",
            "gh pr create uses the current branch's diff against the default branch -- make sure you have committed and pushed your changes first",
            "gh api returns raw JSON; pipe to jq for filtering: gh api repos/owner/repo/issues | jq '.[].title'",
        ],
        "related": ["git", "hub", "tig"],
        "difficulty": "beginner",
        "extra_flags": {
            "pr view": "View details of a pull request",
            "pr merge": "Merge a pull request",
            "pr checkout": "Check out a pull request branch locally",
            "release create": "Create a new GitHub release",
            "repo fork": "Fork a repository",
            "codespace": "Manage GitHub Codespaces",
            "secret": "Manage repository secrets",
            "variable": "Manage repository variables",
            "--json": "Output specific fields in JSON format",
            "--jq": "Filter JSON output with jq expressions",
        },
    },

    "hub": {
        "man_url": "https://hub.github.com/hub.1.html",
        "use_cases": [
            "Clone a repo by shorthand: hub clone owner/repo",
            "Fork the current repo and add a remote: hub fork",
            "Create a pull request: hub pull-request -m 'My PR title'",
            "Open the repo page in a browser: hub browse",
            "Create a new GitHub repository: hub create my-new-repo",
        ],
        "gotchas": [
            "hub is deprecated in favor of GitHub CLI (gh) -- GitHub recommends migrating to gh for active support and new features",
            "hub can be aliased to git (alias git=hub) to seamlessly extend git commands, but this can cause confusion when sharing scripts",
            "hub uses GITHUB_TOKEN environment variable for authentication, while gh uses its own credential store",
        ],
        "related": ["gh", "git", "tig"],
        "difficulty": "intermediate",
        "extra_flags": {
            "ci-status": "Show CI status of the current commit",
            "sync": "Fetch and fast-forward the default branch",
            "release": "Manage GitHub releases",
            "issue": "Create and list GitHub issues",
        },
    },

    "tig": {
        "man_url": "https://jonas.github.io/tig/doc/tig.1.html",
        "use_cases": [
            "Browse commit history interactively: tig",
            "View blame annotation for a file: tig blame file.py",
            "Check working tree status with staging support: tig status",
            "View stash entries: tig stash",
            "Browse commits for a specific file: tig -- path/to/file",
        ],
        "gotchas": [
            "tig is read-mostly -- you can stage changes from the status view but most operations still require the git CLI",
            "Navigation uses Vim-like keys (j/k for movement, Enter to open, q to quit) which can be unfamiliar",
            "tig requires ncurses and may not be available by default on minimal server installs",
        ],
        "related": ["git", "gitk", "gh"],
        "difficulty": "intermediate",
        "extra_flags": {
            "log": "Start in log view",
            "show": "Start in diff view for a specific commit",
            "refs": "Browse all references (branches, tags)",
            "grep": "Search through repository content",
        },
    },

    "gitk": {
        "man_url": "https://git-scm.com/docs/gitk",
        "use_cases": [
            "View the entire commit history graphically: gitk --all",
            "Inspect history of a specific file: gitk -- path/to/file",
            "View recent commits: gitk --since='2 weeks ago'",
            "Explore merge conflicts: gitk --merge",
        ],
        "gotchas": [
            "gitk requires a graphical display (X11/Wayland) -- it will not work over SSH without X forwarding or on headless servers",
            "gitk is part of the git-gui package, which may not be installed by default -- install it separately on some distributions",
            "gitk can be slow on repositories with very large histories -- use --max-count to limit",
        ],
        "related": ["git", "tig", "git-gui"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "git-lfs": {
        "man_url": "https://git-lfs.com/",
        "use_cases": [
            "Initialize LFS in a repository: git lfs install",
            "Track large file patterns: git lfs track '*.psd' '*.zip'",
            "List all files tracked by LFS: git lfs ls-files",
            "Migrate existing large files to LFS: git lfs migrate import --include='*.bin'",
            "Pull LFS files after cloning: git lfs pull",
        ],
        "gotchas": [
            "git lfs track only updates .gitattributes -- you still need to git add and commit the .gitattributes file",
            "LFS requires a compatible remote server (GitHub, GitLab, Bitbucket all support it) -- self-hosted Git servers need a separate LFS server",
            "Cloning an LFS repo downloads all LFS pointers but fetches only the current revision's files -- use git lfs fetch --all to get all versions",
            "LFS has storage and bandwidth limits on GitHub free plans -- large projects may need paid plans or self-hosted LFS",
        ],
        "related": ["git", "gh"],
        "difficulty": "intermediate",
        "extra_flags": {
            "env": "Display the LFS environment configuration",
            "prune": "Delete old LFS files that are no longer referenced",
            "status": "Show the status of LFS files in the working tree",
            "logs": "Show LFS error logs for debugging",
        },
    },

    # =========================================================================
    # MISCELLANEOUS / SHELL BUILTINS
    # =========================================================================

    "date": {
        "man_url": "https://man7.org/linux/man-pages/man1/date.1.html",
        "use_cases": [
            "Display current date and time: date",
            "Format date for filenames: date +%Y-%m-%d_%H%M%S",
            "Get ISO 8601 formatted date: date -I or date --iso-8601",
            "Display a specific date: date -d 'next Friday'",
            "Calculate time differences: date -d '3 days ago' +%Y-%m-%d",
            "Get Unix epoch timestamp: date +%s",
        ],
        "gotchas": [
            "The -d flag (display a specific date) is a GNU extension and does not work on macOS/BSD -- use gdate from coreutils or the -v flag on macOS instead",
            "date format specifiers are case-sensitive: %m is month, %M is minute; %d is day-of-month, %D is mm/dd/yy",
            "Setting the system date (date -s) requires root privileges and does not update the hardware clock -- use hwclock to sync",
        ],
        "related": ["cal", "timedatectl", "hwclock"],
        "difficulty": "beginner",
        "extra_flags": {
            "+%FORMAT": "Display date using custom format string",
            "-R": "Output RFC 2822 formatted date",
            "--rfc-3339": "Output RFC 3339 formatted date",
            "-r": "Display last modification time of a file",
        },
    },

    "sleep": {
        "man_url": "https://man7.org/linux/man-pages/man1/sleep.1.html",
        "use_cases": [
            "Pause execution for 5 seconds: sleep 5",
            "Wait for half a second: sleep 0.5",
            "Wait for 2 minutes: sleep 2m",
            "Add a delay between retries: while ! curl -s http://localhost:8080; do sleep 1; done",
            "Rate-limit a loop: for i in $(seq 1 100); do command; sleep 0.1; done",
        ],
        "gotchas": [
            "sleep accepts suffixes: s (seconds, default), m (minutes), h (hours), d (days) -- these are GNU extensions not available on all systems",
            "Fractional seconds (sleep 0.5) work on GNU/Linux but not on all BSD/macOS versions -- check your system",
            "sleep in a script keeps the process alive and counts toward active processes -- do not use sleep for very long delays in production scripts; use cron or at instead",
        ],
        "related": ["watch", "timeout", "wait"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "time": {
        "man_url": "https://man7.org/linux/man-pages/man1/time.1.html",
        "use_cases": [
            "Measure how long a command takes: time make -j4",
            "Time a complex pipeline: time (find . -name '*.py' | xargs wc -l)",
            "Benchmark a script: time ./run-tests.sh",
        ],
        "gotchas": [
            "There are two 'time' commands: the bash builtin (outputs to stderr) and /usr/bin/time (more detailed output) -- use \\time or command time to invoke the external version",
            "The three values reported are: real (wall clock), user (CPU in user mode), sys (CPU in kernel mode) -- real >= user + sys due to I/O waits and process scheduling",
            "/usr/bin/time -v (verbose) gives memory usage, page faults, and more -- useful for profiling resource-intensive commands",
        ],
        "related": ["timeout", "watch", "perf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-p": "Use POSIX output format",
            "-v": "Verbose output with resource usage details (external time only)",
            "-o": "Write output to a file (external time only)",
        },
    },

    "watch": {
        "man_url": "https://man7.org/linux/man-pages/man1/watch.1.html",
        "use_cases": [
            "Monitor disk space every 2 seconds: watch df -h",
            "Watch a directory for new files: watch -n 1 ls -lt /tmp/",
            "Highlight differences between updates: watch -d free -h",
            "Monitor a Kubernetes deployment: watch kubectl get pods",
            "Exit when the output changes: watch -g 'cat /proc/loadavg'",
        ],
        "gotchas": [
            "watch runs the command in sh, not bash, so bash-specific syntax like arrays or [[ ]] may fail -- wrap complex commands in quotes",
            "watch passes the entire command string to sh -c, so pipes and redirects work, but quoting can be tricky",
            "The default interval is 2 seconds; intervals below 0.1s may cause excessive system load on resource-intensive commands",
            "watch -g (exit on change) is a GNU extension not available on macOS -- use brew install watch for GNU watch on macOS",
        ],
        "related": ["sleep", "timeout", "top"],
        "difficulty": "beginner",
        "extra_flags": {
            "-g": "Exit when the output of the command changes",
            "-t": "Turn off the header showing interval, command, and current time",
            "-e": "Freeze on command error and exit on keypress",
            "-c": "Interpret ANSI color and style sequences",
            "-x": "Pass the command to exec instead of sh -c",
        },
    },

    "history": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html",
        "use_cases": [
            "Search command history: history | grep docker",
            "Re-execute the last command: !!",
            "Re-execute command number 42: !42",
            "Re-execute the most recent command starting with 'git': !git",
            "Delete a sensitive entry from history: history -d 42",
            "Prevent a command from being saved to history: prepend a space (requires HISTCONTROL=ignorespace)",
        ],
        "gotchas": [
            "history -c clears the in-memory history but does not erase ~/.bash_history -- to fully clear, run history -c && history -w",
            "Commands prefixed with a space are not saved to history only if HISTCONTROL contains ignorespace or ignoreboth",
            "In multi-terminal sessions, history is written when the shell exits, so the last-to-close terminal's history wins unless you set shopt -s histappend",
            "!! and !n expansions are evaluated before the command runs -- pipe through echo first to see what will execute: echo !!",
        ],
        "related": ["fc", "alias", "bash"],
        "difficulty": "beginner",
        "extra_flags": {
            "-a": "Append new history lines to the history file",
            "-r": "Read the history file and append its contents to the history list",
            "-w": "Write the current history list to the history file",
            "-d": "Delete a specific history entry by line number",
            "-p": "Perform history expansion and display the result without executing",
        },
    },

    "alias": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Create a shortcut: alias ll='ls -la'",
            "Shorten a git command: alias gs='git status'",
            "Override a dangerous command with safety: alias rm='rm -i'",
            "List all defined aliases: alias",
            "Make aliases persistent by adding them to ~/.bashrc or ~/.bash_aliases",
        ],
        "gotchas": [
            "Aliases defined in a terminal session are lost when the shell exits -- add them to ~/.bashrc or ~/.bash_aliases to persist",
            "Aliases are not expanded in shell scripts by default (only interactive shells) -- use functions instead for script portability",
            "Aliasing a command to itself with flags (alias ls='ls --color') works, but complex logic should use a shell function instead",
            "unalias name removes an alias; unalias -a removes all aliases in the current session",
        ],
        "related": ["unalias", "history", "function"],
        "difficulty": "beginner",
        "extra_flags": {
            "-p": "Print all defined aliases in a reusable format",
        },
    },

    "test": {
        "man_url": "https://man7.org/linux/man-pages/man1/test.1.html",
        "use_cases": [
            "Check if a file exists: test -f /etc/passwd && echo 'exists'",
            "Check if a directory exists: test -d /tmp && echo 'is a directory'",
            "Compare two numbers: test $count -gt 10 && echo 'more than 10'",
            "Check if a string is non-empty: test -n \"$var\" && echo 'has value'",
            "Use bracket syntax in scripts: [ -f file.txt ] && cat file.txt",
        ],
        "gotchas": [
            "[ is an alias for test and requires a closing ] -- forgetting the space before ] causes syntax errors",
            "Always quote variables in test expressions: [ -f \"$file\" ] -- unquoted variables with spaces or empty values cause errors",
            "test uses -eq, -ne, -lt, -gt for numeric comparison and =, != for string comparison -- mixing them gives wrong results",
            "Prefer [[ ]] in bash scripts over [ ] -- it handles quoting better, supports regex with =~, and does not require escaping && and ||",
        ],
        "related": ["[", "[[", "if"],
        "difficulty": "beginner",
        "extra_flags": {
            "-s": "File exists and has size greater than zero",
            "-L": "File exists and is a symbolic link",
            "-eq": "Integer equal comparison",
            "-ne": "Integer not equal comparison",
            "-lt": "Integer less than comparison",
            "-gt": "Integer greater than comparison",
            "-le": "Integer less than or equal",
            "-ge": "Integer greater than or equal",
            "-a": "Logical AND (deprecated; use && with [[ ]] instead)",
            "-o": "Logical OR (deprecated; use || with [[ ]] instead)",
        },
    },

    "read": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html",
        "use_cases": [
            "Prompt user for input: read -p 'Enter your name: ' name",
            "Read a password without echoing: read -s -p 'Password: ' password",
            "Read with a timeout: read -t 5 -p 'Quick! Enter value: ' val",
            "Read a file line by line: while IFS= read -r line; do echo \"$line\"; done < file.txt",
            "Split input into multiple variables: read first last <<< 'John Doe'",
        ],
        "gotchas": [
            "Always use -r to prevent backslash interpretation -- without it, read treats backslash as an escape character and eats them",
            "read splits input on IFS (whitespace by default) -- set IFS= before read to preserve leading/trailing whitespace and read the entire line",
            "read in a pipeline runs in a subshell, so variables set by read are lost after the pipeline ends -- use process substitution or while loop with redirection instead",
            "read -t (timeout) returns non-zero if the timeout expires -- check the exit code to distinguish timeout from empty input",
        ],
        "related": ["echo", "printf", "select"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-a": "Read words into an array variable",
            "-d": "Use specified delimiter instead of newline",
            "-n": "Read exactly N characters without waiting for Enter",
            "-N": "Read exactly N characters (ignore delimiter)",
            "-u": "Read from file descriptor instead of stdin",
            "-e": "Use readline for input (enables line editing)",
            "-i": "Use specified text as initial input (with -e only)",
        },
    },

    "seq": {
        "man_url": "https://man7.org/linux/man-pages/man1/seq.1.html",
        "use_cases": [
            "Generate numbers from 1 to 10: seq 10",
            "Generate a range with step: seq 0 2 20",
            "Generate zero-padded numbers: seq -w 01 10",
            "Use a custom separator: seq -s ', ' 5",
            "Use in a for loop: for i in $(seq 1 5); do echo $i; done",
        ],
        "gotchas": [
            "seq is not POSIX -- for portability in scripts, use: for i in $(( ... )) or bash brace expansion {1..10}",
            "seq handles floating point numbers: seq 0.1 0.1 1.0 -- but rounding errors can cause unexpected results",
            "Brace expansion {1..10} is expanded at parse time and cannot use variables; seq can: seq 1 $n",
        ],
        "related": ["for", "while", "printf"],
        "difficulty": "beginner",
        "extra_flags": {
            "-f": "Use printf-style format for output numbers",
        },
    },

    "stat": {
        "man_url": "https://man7.org/linux/man-pages/man1/stat.1.html",
        "use_cases": [
            "Show all metadata for a file: stat file.txt",
            "Display file permissions in octal: stat -c '%a %n' file.txt",
            "Show file size in bytes: stat -c '%s' file.txt",
            "Get the last modification time: stat -c '%y' file.txt",
            "Script-friendly output of multiple files: stat -c '%a %U %s %n' *",
        ],
        "gotchas": [
            "stat format strings differ between GNU/Linux (-c '%a') and macOS/BSD (-f '%A') -- scripts that use stat are not portable without checking the OS first",
            "stat shows inode metadata, which reflects the file on disk -- recently written data in buffers may not be reflected until flushed",
        ],
        "related": ["file", "ls", "find"],
        "difficulty": "intermediate",
        "extra_flags": {
            "-c": "Use specified format string (GNU/Linux)",
            "-f": "Display filesystem status instead of file status",
            "--printf": "Like -c but interpret backslash escapes and no trailing newline",
            "-L": "Follow symbolic links and report the target's status",
            "-t": "Print information in terse (machine-readable) form",
        },
    },

    "file": {
        "man_url": "https://man7.org/linux/man-pages/man1/file.1.html",
        "use_cases": [
            "Determine the type of a file: file mystery_file",
            "Check all files in a directory: file *",
            "Get the MIME type for a web server: file -i document.pdf",
            "Check if a file is a text file or binary: file script.sh",
            "Identify encoding of a text file: file -i textfile.txt",
        ],
        "gotchas": [
            "file examines file content, not the extension -- renaming a .jpg to .txt will still identify it as an image",
            "file uses magic number databases (/usr/share/misc/magic or /usr/share/file/magic) -- results may vary between systems with different magic databases",
            "file -i returns MIME types with charset info (e.g., text/plain; charset=utf-8), while -I is used on macOS for the same purpose",
        ],
        "related": ["stat", "ls", "find", "strings"],
        "difficulty": "beginner",
        "extra_flags": {
            "-z": "Look inside compressed files",
            "-L": "Follow symbolic links",
            "-s": "Read block or character special files",
            "-k": "Keep going after the first match (show all matches)",
            "--mime-type": "Output only the MIME type without charset",
        },
    },

    "less": {
        "man_url": "https://man7.org/linux/man-pages/man1/less.1.html",
        "use_cases": [
            "View a file with scrolling: less file.txt",
            "View command output with paging: command | less",
            "Search for a pattern while viewing: /pattern then n for next match",
            "View a log file and follow new output: less +F logfile.log (press Ctrl+C to stop, F to resume)",
            "View a file with line numbers: less -N file.txt",
        ],
        "gotchas": [
            "less is not cat -- do not use 'cat file | less'; use 'less file' directly for proper seeking and performance",
            "less +F is similar to tail -f but lets you switch back to scrolling with Ctrl+C -- then press F to resume following",
            "Use -R or --RAW-CONTROL-CHARS to properly display colored output (e.g., from grep --color) in less",
            "Type q to quit, / to search forward, ? to search backward, g to go to beginning, G to go to end",
        ],
        "related": ["more", "cat", "head", "tail"],
        "difficulty": "beginner",
        "extra_flags": {
            "+F": "Follow mode (like tail -f, but interactive)",
            "-X": "Do not clear the screen when exiting",
            "-F": "Exit immediately if content fits one screen",
            "-i": "Case-insensitive search",
            "-I": "Case-insensitive search even for uppercase patterns",
            "-g": "Highlight only the current search match",
            "-J": "Display a status column at the left edge",
            "--follow-name": "Follow by filename, not file descriptor",
        },
    },

    "more": {
        "man_url": "https://man7.org/linux/man-pages/man1/more.1.html",
        "use_cases": [
            "View a file one page at a time: more file.txt",
            "View command output paged: command | more",
        ],
        "gotchas": [
            "more only scrolls forward, not backward -- use less for bidirectional scrolling and better features",
            "On modern systems, more is often a symlink to less or a minimal implementation -- less is almost always the better choice",
        ],
        "related": ["less", "cat", "head", "tail"],
        "difficulty": "beginner",
        "extra_flags": {
            "-d": "Display user-friendly prompts instead of ringing the bell",
            "-s": "Squeeze multiple blank lines into one",
            "+/pattern": "Start displaying at the first occurrence of pattern",
            "-num": "Set the screen size to num lines",
        },
    },

    "clear": {
        "man_url": "https://man7.org/linux/man-pages/man1/clear.1.html",
        "use_cases": [
            "Clear the terminal screen: clear",
            "Clear the screen in a script: clear (or use printf '\\033[2J\\033[H')",
        ],
        "gotchas": [
            "clear does not erase scrollback history in most terminals -- use clear -x or Ctrl+L for just visual clearing, or reset for a full terminal reset",
            "Ctrl+L is a keyboard shortcut that does the same thing as clear in most shells and is faster to type",
        ],
        "related": ["reset", "tput"],
        "difficulty": "beginner",
        "extra_flags": {
            "-x": "Do not attempt to clear the terminal scrollback buffer",
        },
    },

    "man": {
        "man_url": "https://man7.org/linux/man-pages/man1/man.1.html",
        "use_cases": [
            "View the manual page for a command: man ls",
            "Search for commands by keyword: man -k compress",
            "View a specific section of the manual: man 5 crontab",
            "View the manual for a C library function: man 3 printf",
            "Display the location of a man page: man -w ls",
        ],
        "gotchas": [
            "Manual sections matter: man printf shows the shell command, while man 3 printf shows the C library function -- specify the section when ambiguous",
            "man -k (or apropos) searches the whatis database which may need to be rebuilt with mandb or makewhatis",
            "man uses your PAGER environment variable (usually less) -- set PAGER=less or MANPAGER=less for consistent behavior",
            "Some commands (bash builtins like cd, export) do not have standalone man pages -- use help cd or man bash and search within",
        ],
        "related": ["info", "help", "apropos", "whatis"],
        "difficulty": "beginner",
        "extra_flags": {
            "-k": "Search manual page descriptions for a keyword (equivalent to apropos)",
            "-f": "Display a short description of a command (equivalent to whatis)",
            "-a": "Display all matching manual pages, not just the first",
            "-w": "Display the location of the man page file",
            "-K": "Search all man pages for a string (slow but thorough)",
        },
    },

    "cal": {
        "man_url": "https://man7.org/linux/man-pages/man1/cal.1.html",
        "use_cases": [
            "Display the current month: cal",
            "Display the whole year: cal -y",
            "Show 3 months (previous, current, next): cal -3",
            "Display a specific month and year: cal 12 2025",
            "Show week numbers: cal -w",
        ],
        "gotchas": [
            "cal 2024 shows the entire year 2024, not the calendar for the year 2024 BC -- this is rarely an issue but worth noting for scripts",
            "cal starts weeks on Sunday by default in the US locale; use ncal or set locale to change the start day",
            "cal output width is fixed and may not align properly in narrow terminal windows",
        ],
        "related": ["date", "ncal"],
        "difficulty": "beginner",
        "extra_flags": {
            "-j": "Display Julian day numbers (day of year)",
            "-m": "Start the week on Monday",
            "-w": "Display ISO week numbers",
        },
    },

    "yes": {
        "man_url": "https://man7.org/linux/man-pages/man1/yes.1.html",
        "use_cases": [
            "Auto-confirm prompts: yes | apt-get install package-name",
            "Auto-decline prompts: yes n | rm -i *",
            "Generate repeated output for testing: yes 'test line' | head -1000",
            "Stress test output handling: yes > /dev/null &",
        ],
        "gotchas": [
            "yes runs forever until killed or its output pipe closes -- always pipe it to a command or use Ctrl+C to stop",
            "Most package managers have their own -y flag (apt -y, yum -y) which is safer and more explicit than piping yes",
            "yes outputs at maximum speed and can spike CPU usage -- do not run it unpiped as a background process",
        ],
        "related": ["true", "false", "echo"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "whoami": {
        "man_url": "https://man7.org/linux/man-pages/man1/whoami.1.html",
        "use_cases": [
            "Check which user you are logged in as: whoami",
            "Guard a script against running as root: [ $(whoami) = 'root' ] && echo 'Do not run as root' && exit 1",
            "Include username in log messages: echo \"$(whoami) ran this script at $(date)\"",
        ],
        "gotchas": [
            "whoami prints the effective user, which may differ from the login user if you used sudo or su -- use logname for the original login name",
            "In containers, whoami usually returns root unless a USER directive was set in the Dockerfile",
        ],
        "related": ["id", "who", "logname"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "hostname": {
        "man_url": "https://man7.org/linux/man-pages/man1/hostname.1.html",
        "use_cases": [
            "Display the system hostname: hostname",
            "Display the fully qualified domain name: hostname -f",
            "Display all IP addresses of the host: hostname -I",
            "Use hostname in a script for per-server behavior: case $(hostname) in web*) start_nginx;; db*) start_postgres;; esac",
        ],
        "gotchas": [
            "Setting the hostname with 'hostname newname' is temporary and resets on reboot -- use hostnamectl set-hostname on systemd systems for persistence",
            "hostname -I (capital I) shows all IPs without DNS lookup; hostname -i (lowercase) does a DNS lookup and may fail if DNS is misconfigured",
            "In containers, hostname returns the container ID by default unless explicitly set",
        ],
        "related": ["hostnamectl", "uname", "whoami"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "uname": {
        "man_url": "https://man7.org/linux/man-pages/man1/uname.1.html",
        "use_cases": [
            "Show all system information: uname -a",
            "Get the kernel version: uname -r",
            "Detect the CPU architecture for cross-compilation: uname -m",
            "Check if running on Linux vs macOS in a script: case $(uname -s) in Linux) echo linux;; Darwin) echo mac;; esac",
        ],
        "gotchas": [
            "uname -m returns the kernel architecture, not necessarily the userspace -- a 64-bit kernel can run a 32-bit userspace",
            "On WSL, uname -r returns a Linux kernel version but the actual host is Windows -- check for 'microsoft' in uname -r to detect WSL",
        ],
        "related": ["hostname", "lsb_release", "hostnamectl"],
        "difficulty": "beginner",
        "extra_flags": {
            "-o": "Print the operating system name",
            "-p": "Print the processor type (or 'unknown')",
        },
    },

    "uptime": {
        "man_url": "https://man7.org/linux/man-pages/man1/uptime.1.html",
        "use_cases": [
            "Check how long the system has been running: uptime",
            "Get human-readable uptime duration: uptime -p",
            "See when the system was last booted: uptime -s",
            "Check load averages for monitoring: uptime | awk '{print $NF}'",
        ],
        "gotchas": [
            "Load averages are 1-min, 5-min, and 15-min averages of processes in runnable or uninterruptible state -- they are NOT CPU percentages and scale with the number of cores",
            "A load average equal to the number of CPU cores means the system is fully utilized; above that means processes are waiting",
        ],
        "related": ["free", "top", "w"],
        "difficulty": "beginner",
        "extra_flags": {},
    },

    "free": {
        "man_url": "https://man7.org/linux/man-pages/man1/free.1.html",
        "use_cases": [
            "Display memory usage in human-readable format: free -h",
            "Show memory usage in megabytes: free -m",
            "Continuously monitor memory every 5 seconds: free -h -s 5",
            "Show total line combining RAM and swap: free -h -t",
        ],
        "gotchas": [
            "The 'available' column (not 'free') is what matters for new processes -- Linux uses free memory for caches, so 'free' will be low even on healthy systems",
            "The 'buff/cache' memory is automatically released when applications need it -- a system with low 'free' but high 'available' is healthy",
            "free shows swap usage which can indicate memory pressure -- if swap is heavily used, the system is likely thrashing",
        ],
        "related": ["top", "htop", "vmstat", "uptime"],
        "difficulty": "beginner",
        "extra_flags": {
            "-w": "Wide output (separate buffers and cache columns)",
            "-l": "Show detailed low and high memory statistics",
            "--si": "Use powers of 1000 instead of 1024",
        },
    },

    "env": {
        "man_url": "https://man7.org/linux/man-pages/man1/env.1.html",
        "use_cases": [
            "Display all environment variables: env",
            "Filter environment variables: env | grep PATH",
            "Run a command with a modified environment: env VAR=value command",
            "Run a command with a clean environment: env -i /bin/bash",
            "Set environment for a single command without affecting current shell: env LANG=C sort file.txt",
        ],
        "gotchas": [
            "env -i starts with an empty environment, which can break most commands since PATH, HOME, and other critical variables are unset",
            "env is commonly used in shebang lines (#!/usr/bin/env python3) to find commands in PATH regardless of installation location",
            "env shows exported variables only, not shell-local variables -- use set to see all variables",
        ],
        "related": ["export", "printenv", "set"],
        "difficulty": "beginner",
        "extra_flags": {
            "-0": "Null-terminate output lines (for use with xargs -0)",
            "-u": "Remove a variable from the environment for the command",
            "-S": "Split a single string into arguments (useful in shebangs)",
        },
    },

    "export": {
        "man_url": "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html",
        "use_cases": [
            "Make a variable available to child processes: export PATH=$PATH:/usr/local/bin",
            "Set an environment variable for a session: export NODE_ENV=production",
            "Export a variable at definition time: export DATABASE_URL='postgres://localhost/mydb'",
            "List all exported variables: export -p",
            "Un-export a variable (remove from environment): export -n MYVAR",
        ],
        "gotchas": [
            "export only affects child processes started AFTER the export -- already-running processes do not see the change",
            "Variables set in a script without export are local to that script and invisible to commands it calls",
            "export in a subshell or child process does not affect the parent shell -- modifications are lost when the subshell exits",
            "To persist environment variables across sessions, add export statements to ~/.bashrc, ~/.bash_profile, or ~/.profile",
        ],
        "related": ["env", "set", "unset", "source"],
        "difficulty": "beginner",
        "extra_flags": {
            "-f": "Export a shell function, not a variable",
        },
    },

}
