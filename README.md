# myx.distro-.local

Creates a myx.distro workspace and installs the `myx.distro-*` toolsets into it.
It also generates the `Distro*Console.sh` launchers you start each toolset with.

Every installed package adds its own `sh-scripts/` directory to the console `PATH`.

Use it when you set up a new myx.distro workspace, or add, upgrade or configure a toolset in one.

## First command

On a new machine, bootstrap a workspace with `workspace-install.sh`. [Installation](docs/installation.md) shows the command.

In an existing workspace, open the local console:

	./DistroLocalConsole.sh

## Before you upgrade

Installed copies under `.local/` are distributions. An install or upgrade discards local edits and local commits in them. Make your changes in the source tree, not in `.local/`. [Installation](docs/installation.md) has the details.

## Documentation

- [Installation](docs/installation.md) — requirements, install, upgrade and uninstall.
- [Configuration](docs/configuration.md) — settings, profile options and configuration commands.
- [Use](docs/use.md) — getting started, common tasks and selecting what to act on.
- [Commands](docs/commands.md) — the command reference.
- [Formats](docs/formats.md) — file formats, directives, stages and folder layout.
- [Extension](docs/extension.md) — adding your own members, builders, directives and commands.
- [Examples](docs/examples.md) — worked examples from start to finish.
- [Troubleshooting](docs/troubleshooting.md) — symptoms, causes and actions.

## Getting help

- `DistroLocalTools.fn.sh --help` — full syntax, options and examples.
- `DistroLocalTools.fn.sh --help-install-unix-bare` — bare-Unix install instructions.
- `Local --help` and `Require --help` — local-console dispatcher syntax.
- Press TAB after a command name and a space for shell completion.

## Related packages

- [myx.distro](https://github.com/myx/myx.distro) — the distro system overview.
- [myx.distro-system](https://github.com/myx/myx.distro-system) — shared indexing and query tools.
- [myx.distro-source](https://github.com/myx/myx.distro-source) — build source into a distro image.
- [myx.distro-deploy](https://github.com/myx/myx.distro-deploy) — deploy a distro image to hosts.
- [myx.distro-remote](https://github.com/myx/myx.distro-remote) — drive a workspace on another machine.
- [myx.distro-agents](https://github.com/myx/myx.distro-agents) — the magic-team agents and their tooling.
