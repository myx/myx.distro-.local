# Commands

[Back to the README](../README.md)

- `DistroLocalTools.fn.sh` — install, upgrade and configure toolsets; generate console launchers.
- `workspace-install.sh` — standalone bootstrap that creates a whole workspace from a config file.


## DistroLocalTools options

`DistroLocalTools.fn.sh` takes options only, and no positional arguments.

- Install and upgrade:
	- `--install-distro-source`, `--install-distro-deploy`, `--install-distro-remote` — install a toolset into the workspace.
	- `--install-distro-agents` — install the agent tooling and create the workspace `agents` data directory.
	- `--install-distro-.local` — upgrade the local `.local` packages to the latest `master` version.
	- `--upgrade-installed-tools` — upgrade the deploy, source, remote and agents toolsets to the latest `master` version, then exit.
- Console and workspace setup:
	- `--make-console-command [--quiet]` — re-create `DistroLocalConsole.sh`, then exit. `--quiet` hides the usage notes.
	- `--make-console-script` — print the console script body that `--make-console-command` uses.
	- `--make-workspace-integrations [--quiet]` — set up every installed toolset, then exit.
	- `--make-clean-fs-garbage [<path>]` — remove known junk files, directories and extended attributes under the workspace or the given path.
	- `--make-setup-mac` — apply the macOS Finder view presets.
- Settings:
	- `--system-config-option`, `--custom-config-option`, `--remote-config-option <remote-id>`, `--agents-config-option <entity-id>` — read and change settings. [Configuration](configuration.md) lists the operations.
- Output and help:
	- `--verbose` — print detailed progress for the rest of the command line. Give it before the option it applies to.
	- `--help` and `--help-install-unix-bare` — print the manual, or the bare-Unix install instructions.

Any number of `--install-distro-*` options combine into one run. The tool collects them, installs them together, and exits after the last one. It rejects any other option that follows them.

`--upgrade-installed-tools` includes each toolset whose package is present under `MDLT_ORIGIN`, whether or not this workspace has installed it. Every install run refreshes `os-myx.common` and `myx.distro-.local`.

`--make-workspace-integrations` creates:

- a `Distro*Console.sh` command in the workspace root for each console.
- the VS Code `.code-workspace` file, when the source tools are installed.
- the VS Code and Claude Code setup for the magic-team agents, when the agent tools are installed.
- the Finder view presets, on macOS.


## Manuals

Each tool has a manual with its full syntax, options and examples.

- [DistroLocalTools-install-unix-bare](../sh-lib/help/Help.DistroLocalTools-install-unix-bare.help.md)
- [DistroLocalTools](../sh-lib/help/Help.DistroLocalTools.help.md)
- [Project.Inf.file](../sh-lib/help/Man.Project.Inf.file.help.md)
