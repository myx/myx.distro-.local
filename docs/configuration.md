# Configuration

[Back to the README](../README.md)

## Workspace config file

The workspace config is a text file of directives, one per line. The first column
is the subsystem (`source`, `remote`, `deploy`, `agents` or `.local`); the rest is
that subsystem's directive. The installer installs that subsystem's toolset first,
where the workspace does not have it yet, then runs the directives. Any other first
column is refused there, so `system` is not one.

	# Repository roots for source projects
	source root lib
	source root myx

	# Initial list of source projects to pull
	source pull myx/my-workspace-project:main:git@github.com:myx/my-workspace-project.git

	# Commands to run once the source subsystem is installed
	source exec Source DistroSourceTools --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN source ""
	source exec Distro DistroImageSync --all-tasks --execute-source-prepare-pull

## Config operations

Both `--system-config-option` and `--custom-config-option` take one of:

- `--select <name>` — read one value.
- `--select-default <name> <default>` — read one value, falling back to a default.
- `--select-all` — read every value.
- `--upsert <name> <value>` — set a value.
- `--upsert-if <name> <value> <if-value>` — set it only when it currently equals `<if-value>`.
- `--delete <name>` — remove a value.
- `--delete-if <name> <if-value>` — remove it only when it currently equals `<if-value>`.

## Workspace settings

- `MDLT_CONSOLE_ORIGIN` — where consoles load their tools from.
	- `.local` — this workspace's installed copy.
	- `source` — this workspace's own source tree.
	- an absolute path to another workspace's `.local` or `source` directory.
- `MDLT_CONSOLE_SCRIPT` — extra shell script sourced during console startup, after `~/.bashrc`.
- `MDLT_CONSOLE_HISTORY` — where console shell history is stored. Default `workspace-personal`.
	- `workspace-personal` — per-user file under `<workspace>/.local/home/$USER/.bash_history`.
	- `workspace-separate` — per-user, one file per subsystem (source, deploy, remote).
	- `workspace-shared` — one shared file at `<workspace>/.local/.common_bash_history`.
	- `local-machine-home` — per-workspace file in `$HOME`, e.g. `~/.bash_history_<workspace>`.
	- `bash-default` — reset to Bash's standard `~/.bash_history`.
	- `user-default` — leave the user's current setting untouched.
- `MDLT_MANAGER_STYLE` — the interface style of the manager screen, `<style>-<colours>`. Default `tv-system`. Declared with the mouse and the spacers in `sh-lib/manager/LocalTools.ManagerInterface.include`.
- `MDLT_MANAGER_SPACERS` — the blank lines between the groups of the agents console screen's lists. `disable` turns them off. Default: on.
- `MDLT_MANAGER_MOUSE` — the mouse of the agents console screen. `disable` leaves the mouse to the terminal, so that its own selection copies text. Default: on.
- `MDLT_ACTIONS_SH_WRAP` — command used to wrap every action run, for remote runners or logging.


## Config scopes

The config operations come in four scopes:

- `--system-config-option` — applies to the whole workspace.
- `--custom-config-option` — applies to the current user.
- `--remote-config-option <remote-id>` — applies to one registered remote.
- `--agents-config-option <entity-id>` — applies to one agent entity. Only its owner and group can access it.

`--remote-config-option` and `--agents-config-option` need their id straight after the scope option.

To set a value without putting it on the command line, give the operation `--upsert-from-stdin <name>`. The tool reads the value from standard input. It rejects an empty value and a value that contains a newline.

## Context variables

The local tools use these variables:

- `MMDAPP` — the workspace root path.
- `MDLT_ORIGIN` — the source root for distro command libraries and scripts.
- `MDLC_INMODE` — the detected console input mode: `.local`, `source` or `extern`.
- `MDSC_DETAIL` — debug verbosity: empty, `true` or `full`.
- `MYXROOT` — the resolved `myx.common` root, used by helper fallbacks.
