# Installation

[Back to the README](../README.md)

## Bootstrap a workspace

Bootstrap a new workspace from scratch. `TGT_APP_PATH` is required:

	export TGT_APP_PATH=~/Workspaces/ws-myx.devops
	curl -fsSL https://raw.githubusercontent.com/myx/myx.distro-.local/refs/heads/main/sh-scripts/workspace-install.sh \
		| bash -s -- --git-clone --force --config-file ./workspace-config.txt

Bootstrap flags:

- `--git-clone` — clone the packages over git.
- `--web-fetch` — download and unpack a GitHub ZIP instead. Default.
- `--force` — re-bootstrap even when the workspace is already present.
- `--config-file <path>` — read the workspace config from a file.
- `--config-stdin` — read the workspace config from stdin.
- `--verbose` — print detail while installing.

For a machine with nothing installed yet, print the bare-Unix instructions:

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --help-install-unix-bare

## Toolsets and upgrades

Install a toolset into an existing workspace:

- `DistroLocalTools.fn.sh --install-distro-source` — the source build toolset.
- `DistroLocalTools.fn.sh --install-distro-deploy` — the deploy toolset.
- `DistroLocalTools.fn.sh --install-distro-remote` — the remote-workspace toolset.
- `DistroLocalTools.fn.sh --install-distro-agents` — the agent team and its tooling.
- `DistroLocalTools.fn.sh --install-distro-.local` — this package itself.

Several may be listed in one run:

	DistroLocalTools.fn.sh --install-distro-source --install-distro-deploy --install-distro-remote

Update every installed toolset to its latest published version:

	DistroLocalTools.fn.sh --upgrade-installed-tools
