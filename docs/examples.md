# Examples

[Back to the README](../README.md)

## A complete workspace config file

The package ships a similar example. This one sets up a source workspace. It registers two repository roots, lists one project to pull, and runs two commands once the source subsystem is installed.

	## Repository roots for source projects
		source root lib
		source root myx

	## Initial list of source projects to pull
		source pull myx/util.workspace-myx.devops:main:git@github.com:myx/util.workspace-myx.devops.git

	## Executable commands to setup source sub-system

		# Configuring system to run from source repositories, so we can test local changes...
		source exec Source DistroSourceTools --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN "source" ""

		# Syncing all known project's git repositories...
		source exec Distro DistroImageSync --all-tasks --execute-source-prepare-pull

- `source root <name>` registers a repository root.
- `source pull <project>:<branch>:<repository>` lists a project to pull.
- `source exec <console> <command...>` runs a command after the subsystem installs.

Pass the file to the bootstrap with `--config-file`. [Installation](installation.md) shows the command.

## Run the consoles from source, then undo it

Set `MDLT_CONSOLE_ORIGIN` to `source` only when it is empty:

	Distro DistroSourceTools --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN source ""

Remove it only when it equals `source`:

	Distro DistroSourceTools --system-config-option --delete-if MDLT_CONSOLE_ORIGIN source

Print every configured option:

	DistroSourceTools.fn.sh --system-config-option --select-all

## Install several toolsets in one run

	DistroLocalTools.fn.sh --install-distro-source --install-distro-deploy --install-distro-remote

From the operating system shell, with no console:

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --install-distro-source --install-distro-deploy --install-distro-remote
