##
## LocalManagerScreen.Machine.py -- the root `This Machine`: the machine the console runs on, as the two panels of the Dashboard that are about it show it, The Machine (the load against the
## processors, the memory, how long it has been up) and Disk Space (the volumes the workspace and the console use). Moved, not rebuilt: the panels are the Dashboard's own (their readers are
## `.local`'s, LocalToolsManagerDashboardMachine and LocalToolsManagerDashboardDisk, and --manager-dashboard-read prints them by their names), and the drawing is the one the Dashboard and Team Data
## use (blocksView, panelLines); this part only gives them a root of their own, so that they are looked at without the rest of the Dashboard.
## A part of the manager screen of the agents console (myx.distro-agents, sh-lib/manager/AgentsManagerScreen.py), which executes it, in its own namespace, after `Workspace (System)`
## (LOCAL_PARTS_BEFORE). It is plain text of the screen and is never run by itself. Looking only.
##

## The panels of the Dashboard that are about the machine, by their names in the list that registers them.
MACHINE_PANELS = ("machine", "disk")


## What `--manager-dashboard-read` printed of those panels, as the rows of the root: a block each, as the Dashboard's submenus have them.
def parseMachineRows(readKey, level, text):
    return {level: parseBlockRows(text)}


ROW_FORMS["machine"] = parseMachineRows


## The root for the left pane while it is selected or open: the two panels as a grid, as the Dashboard draws them.
def machineSummary(state, path, row, form):
    return blocksView(state, None, levelKey(path))


## A panel selected: that panel alone, as wide as the window.
def machineFocus(state, row):
    return blocksView(state, row["id"], levelKey(state.path)) if row.get("block") else None


registerPlugin({
    "name": "machine",
    "root": {"id": "machine", "label": "This Machine", "go": "Th~i~s Machine", "group": "places"},
    "focus": {"machine": "machineFocus"},
    "summaries": {"machine": {"lines": "machineSummary"}},
    "reads": {
        ## The two panels, read as the Dashboard is: on the period only while the root is selected or opened, and never else.
        "list:machine": {"operation": ["--manager-dashboard-read"] + list(MACHINE_PANELS), "rows": "machine", "peek": True},
    },
})
