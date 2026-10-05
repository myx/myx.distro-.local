# Use

[Back to the README](../README.md)

## Common tasks

Re-create the `Distro*Console.sh` launcher script for every installed toolset:

	DistroLocalTools.fn.sh --make-workspace-integrations

Read and change workspace settings — `--system-` applies to the whole workspace,
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
