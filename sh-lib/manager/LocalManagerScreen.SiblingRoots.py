##
## LocalManagerScreen.SiblingRoots.py -- the roots `Configuration` and `Settings` of the four sibling consoles (S7.24).
## A part of the manager screen (LocalManagerScreen.py of this package, sh-lib/manager): that file executes it, in its own namespace,
## and it is never run by itself. In the agents console those two roots are the agents package's own plugins, with their screens
## (AgentsManagerScreen.Configuration.py, AgentsManagerScreen.Settings.py), and they are kept for the agents app alone. A sibling kept
## neither, so the plugins of this package that mount under them, `Installed Subsystems` under Configuration and `Scope Settings`
## under Settings, had nowhere to stand there and were left unmounted. Each root here is a container alone, for the siblings alone:
## no read, no row of its own, and nothing of the agents' screens under the same names. It loads ahead of those two plugins.
##

for siblingRoot, siblingLabel in (("configuration", "Configuration"), ("settings", "Settings")):
    registerPlugin({
        "name": siblingRoot,
        "apps": ("local", "source", "deploy", "remote"),
        "root": {"id": siblingRoot, "label": siblingLabel, "group": "setup"},
    })
