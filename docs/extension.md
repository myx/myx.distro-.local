# Extension

[Back to the README](../README.md)

The installer and the local console are extended by declaration. A package states what it contributes in its own files, and the tools read every installed package's. Nothing is added by editing the installer.

## Declare a place

A place is a workspace or a directory the console can name. A project declares one line per host, in its `project.inf` `Declares`:

	magic-team:workspace:<name>:<path>:<host-glob>
	magic-team:directory:<name>:<ceiling-read|ceiling-write>:<path>:<host-glob>

- A path is absolute, `~/...`, or relative to the declaring workspace.
- Registering a place grants nothing. Its ceiling decides what may be written, and the permission model decides who may.
- Each workspace rewrites only its own rows, and it does so under its own lock.

`sh-lib/places/LocalTools.Places.include` holds the whole contract, the registry files included.

## Declare a console setting

A package declares its changeable settings beside their labels, in `sh-lib/config/settings-rows.list` and `settings-labels.list`. A row is one line, its fields parted by a pipe. `--manager-config-digest` reads both files from each installed package that declares them.

## Declare a manager screen part

The manager screen is assembled from the parts each package contributes. List them in `sh-lib/config/screen-parts.list`, one file name a line, in the order they load.

- `LocalManagerScreen.Constants.py` is the screen's vocabulary, and a screen without it refuses to start.
- `sh-lib/manager/LocalManagerScreen.py` reads the list, and each declared part loads in the screen's own namespace.

## The `project.inf` grammar

This package carries the family's `project.inf` grammar, in `sh-lib/help/Man.Project.Inf.file.help.md`. Read it before adding a directive, a line continuation or an escape.
