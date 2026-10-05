# Troubleshooting

[Back to the README](../README.md)

## A tool is missing from a console

Two different faults look alike. Tell them apart before you decide a tool is broken or gone.

- The family's directory is on `PATH` and the command is missing. The package is not installed in this workspace.
- The family's directory is absent from `PATH`. This console does not expose that family.

Run `command -v <Tool>.fn.sh` to see whether the tool is reachable from where you stand.

The consoles expose these families:

- The local and agents consoles expose every family.
- The source and deploy consoles expose every family except remote.
- The remote console exposes every family except agents.

Each console lists its families in its own start-up file. Nothing adds a family to `PATH` later.

## A command failed but the pipeline reports success

A failing command prints `⛔ ERROR: exited with error status (1)` on stderr. The console pipeline still returns 0, so the exit status proves nothing.

Check the result instead. Look for a non-empty answer, or for the file the command should have made. Read stderr for the error line.

## Tab completion offers a command that does not run

Consoles register completion for every family, whatever their own `PATH` carries. A name that completes does not prove the command resolves. Use `command -v <Tool>.fn.sh`.

## Update the installed tools

Update every installed toolset to its latest published version:

	DistroLocalTools.fn.sh --upgrade-installed-tools

The command covers each toolset whose package is present under `MDLT_ORIGIN`. To refresh only this package, use `--install-distro-.local`.

## A console launcher is missing or out of date

Re-create the `Distro*Console.sh` launchers for every installed toolset:

	DistroLocalTools.fn.sh --make-workspace-integrations

This replaces the launcher only. It does not change which families a console puts on `PATH`.
