# Configuration

[Back to the README](../README.md)

## Workspace config file

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
- `MDLT_ACTIONS_SH_WRAP` — command used to wrap every action run, for remote runners or logging.
