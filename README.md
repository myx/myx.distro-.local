# myx.distro-.local

Creates a myx.distro workspace and installs the `myx.distro-*` toolsets into it —
`myx.distro-source`, `myx.distro-deploy`, `myx.distro-remote`, `myx.distro-agents`,
`myx.distro-system` and `myx.distro-.local` itself. It also generates the
`Distro*Console.sh` launchers you start each toolset with.

Every installed package adds its own `sh-scripts/` directory to the console `PATH`.

## Install

Bootstrap a new workspace from scratch. `TGT_APP_PATH` is required:

	export TGT_APP_PATH=~/Workspaces/ws-myx.devops
	curl -fsSL https://raw.githubusercontent.com/myx/myx.distro-.local/refs/heads/main/sh-scripts/workspace-install.sh \
		| bash -s -- --git-clone --force --config-file ./workspace-config.txt

The workspace config is a text file of directives, one per line. The first column
is the subsystem (`source`, `deploy`, `remote`, `system` or `.local`); the rest is
that subsystem's directive:

	# Repository roots for source projects
	source root lib
	source root myx

	# Initial list of source projects to pull
	source pull myx/my-workspace-project:main:git@github.com:myx/my-workspace-project.git

	# Commands to run once the source subsystem is installed
	source exec Source DistroSourceTools --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN source ""
	source exec Distro DistroImageSync --all-tasks --execute-source-prepare-pull

Pass `--config-stdin` instead of `--config-file <path>` to pipe the config in.
Use `--web-fetch` in place of `--git-clone` to bootstrap from a GitHub ZIP.

For a machine with nothing installed yet, print the bare-Unix instructions:

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --help-install-unix-bare

## Common tasks

Install a toolset into an existing workspace. Several may be listed in one run:

	DistroLocalTools.fn.sh --install-distro-source
	DistroLocalTools.fn.sh --install-distro-source --install-distro-deploy --install-distro-remote

Update every installed toolset to its latest published version:

	DistroLocalTools.fn.sh --upgrade-installed-tools

Re-create the `Distro*Console.sh` launcher script for every installed toolset:

	DistroLocalTools.fn.sh --make-workspace-integration-files

Read and change workspace settings. `--system-` applies to the whole workspace,
`--custom-` to the current user:

	DistroLocalTools.fn.sh --system-config-option --select-all
	DistroLocalTools.fn.sh --system-config-option --upsert MDLT_CONSOLE_HISTORY workspace-shared
	DistroLocalTools.fn.sh --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN source ""
	DistroLocalTools.fn.sh --system-config-option --delete MDLT_CONSOLE_SCRIPT

Clean OS junk files and extended attributes out of the workspace:

	DistroLocalTools.fn.sh --make-clean-fs-garbage

Apply the macOS Finder presets for a workspace:

	DistroLocalTools.fn.sh --make-setup-mac

Open the local console:

	./DistroLocalConsole.sh

From there, `ConsoleSource`, `ConsoleDeploy` and `ConsoleRemote` open the other
consoles for the same workspace.

## Workspace settings

Set these with `--system-config-option` or `--custom-config-option`:

	MDLT_CONSOLE_ORIGIN    where consoles load their tools from: ".local", "source",
	                       or an absolute path to another workspace's ".local"/"source"
	MDLT_CONSOLE_SCRIPT    extra shell script sourced during console startup, after ~/.bashrc
	MDLT_CONSOLE_HISTORY   where console shell history is stored; default workspace-personal
	MDLT_ACTIONS_SH_WRAP   command used to wrap every action run — for remote runners or logging

`MDLT_CONSOLE_HISTORY` accepts:

	workspace-personal   per-user file under <workspace>/.local/home/$USER/.bash_history
	workspace-separate   per-user, one file per subsystem (source, deploy, remote)
	workspace-shared     one shared file at <workspace>/.local/.common_bash_history
	local-machine-home   per-workspace file in $HOME, e.g. ~/.bash_history_<workspace>
	bash-default         reset to Bash's standard ~/.bash_history
	user-default         leave the user's current setting untouched

## Commands

- `DistroLocalTools.fn.sh` — install, upgrade, configure; generate console launchers and integration files.
- `workspace-install.sh` — standalone bootstrap that creates a whole workspace from a config file.

## Getting help

- `DistroLocalTools.fn.sh --help` prints full syntax, options and examples.
- `DistroLocalTools.fn.sh --help-install-unix-bare` prints bare-Unix install instructions.
- `Local --help` and `Require --help` print the local-console dispatcher syntax.
- Press TAB after a command name and a space for shell completion.
- [DistroLocalTools command manual](https://github.com/myx/myx.distro-.local/blob/main/sh-lib/help/Help.DistroLocalTools.help.md)

## Related packages

- [myx.distro](https://github.com/myx/myx.distro) — the distro system overview.
- [myx.distro-system](https://github.com/myx/myx.distro-system) — shared indexing and query tools.
- [myx.distro-source](https://github.com/myx/myx.distro-source) — build source into a distro image.
- [myx.distro-deploy](https://github.com/myx/myx.distro-deploy) — deploy a distro image to hosts.
- [myx.distro-remote](https://github.com/myx/myx.distro-remote) — drive a workspace on another machine.
- [myx.distro-agents](https://github.com/myx/myx.distro-agents) — start an AI-agent CLI console.
