##
## LocalManagerScreen.Subsystems.py -- the folder `Installed Subsystems` of the root Configuration: the subsystems of the tool family, which are installed
## here and which are not, and the commands to install and to uninstall one.
## A part of the manager screen of the agents console (myx.distro-agents, sh-lib/manager/AgentsManagerScreen.py), which executes it, in its own namespace,
## after its own parts (LOCAL_PARTS), when this package stands beside it: the first python of `.local` (F11.7 of the refactorings epic). It is plain text of the
## screen and is never run by itself. The folder is `.local`'s: the operations are `.local`'s (--manager-subsystem-list, --manager-subsystem-run, which the
## dispatcher of any console of the family offers), and the screen only draws them and takes the keys.
##

## ---- the subsystems: `Installed Subsystems` ----

## The fields of a `subsystem` row of `--manager-subsystem-list`, after its first.
SUBSYSTEM_FIELDS = ("name", "state", "role", "install", "uninstall")
## What each subsystem is, in the words of its console: one line.
SUBSYSTEM_WORDS = {
    ".local": "local tool management: it installs the rest",
    "system": "the system tools, shared by source and deploy",
    "deploy": "deploy-side operations",
    "source": "source sync, prepare and ingest",
    "remote": "remote operations",
    "agents": "the magic-team agents, and this console",
}
## Why a subsystem has no command of its own, by its <role>.
SUBSYSTEM_ROLES = {
    "base": "the base that installs the rest",
    "shared": "comes with source and deploy",
    "console": "the console that is asking",
}
## What a command of a subsystem does, in words, for the left pane and for the dialog that asks first.
SUBSYSTEM_RUNS = {
    "install": "It installs the toolset: its package is cloned into .local of the workspace and the console command for it is made. It runs at once and unattended, in a window that follows what it writes. Run starts it; Cancel and Esc do nothing.",
    "uninstall": "It removes the installed copy of the toolset from .local of the workspace, and the console command that was made for it. The data of the workspace is not touched. It runs at once and unattended, in a window that follows what it writes. Run starts it; Cancel and Esc do nothing.",
}


## What `--manager-subsystem-list` printed, as rows, in the order they come: a subsystem a row, its state at the end of it, and, indented under it,
## a row for each command it is offered: `Install`, `Uninstall`. A line of another name and one too short are left out.
def parseSubsystemLevels(readKey, level, text):
    rows = []
    for printed in text.split("\n"):
        fields = printed.split("\t")
        if fields[0] != "subsystem" or len(fields) <= len(SUBSYSTEM_FIELDS):
            continue
        held = dict(zip(SUBSYSTEM_FIELDS, fields[1:]))
        row = newRow(held["name"], held["name"], "subsystem", False, fields)
        row["subsystem"] = held
        row["tail"] = held["state"]
        row["look"] = PLAIN if held["state"] == "installed" else DIM
        rows.append(row)
        for what in ("install", "uninstall"):
            if held[what] == "yes":
                command = newRow("%s:%s" % (held["name"], what), what.capitalize(), "subsystem-command", False, fields)
                command["indent"] = 2
                command["subsystemCommand"] = {"name": held["name"], "what": what}
                rows.append(command)
    return {level: rows}


ROW_FORMS["subsystems"] = parseSubsystemLevels


## What the folder holds, for the left pane: every subsystem as a table, its state in its colour, what it is, and the command it is offered or why
## it has none. None until its read has answered.
def subsystemsSummary(state, path, row, form):
    rows = state.rows.get(levelKey(path))
    if rows is None:
        return None
    held = [one["subsystem"] for one in rows if one.get("subsystem")]
    if not held:
        return [looked("The operation listed no subsystem.", BOLD)]
    return tableSummaryLines(state, ("SUBSYSTEM", "STATE", "WHAT", "COMMAND"),
                             [[one["name"], one["state"], SUBSYSTEM_WORDS.get(one["name"], "-"),
                               "install" if one["install"] == "yes" else "uninstall" if one["uninstall"] == "yes" else SUBSYSTEM_ROLES.get(one["role"], "-")] for one in held],
                             ("key", "enum", "text", "text"),
                             looks=[[None, stateLook(one["state"]) if one["state"] != "installed" else None, None, None] for one in held])


## The selected row of the folder for the left pane: a subsystem by what it is, its state and what it is offered; a command by what it does.
def subsystemsFocus(state, row):
    if row.get("subsystemCommand"):
        command = row["subsystemCommand"]
        return [looked("%s %s" % (command["what"].capitalize(), command["name"]), BOLD)] + factLines([
            ("runs", "DistroLocalTools.fn.sh --%s-distro-%s" % (command["what"], command["name"])),
        ], state.viewWidth) + [""] + wrapToCells(SUBSYSTEM_RUNS[command["what"]], max(10, state.viewWidth - 1))
    if row.get("subsystem"):
        one = row["subsystem"]
        offered = ", ".join(what for what in ("install", "uninstall") if one[what] == "yes")
        return [looked(one["name"], BOLD)] + factLines([
            ("what", SUBSYSTEM_WORDS.get(one["name"], "-")),
            ("state", one["state"], stateLook(one["state"]) if one["state"] != "installed" else None),
            ("commands", offered or SUBSYSTEM_ROLES.get(one["role"], "none")),
        ], state.viewWidth)
    return None


## Enter on a command of a subsystem: asked first, by what will run and what it does; the screen writes no command of its own: the tooling runs it.
def askSubsystem(state, row):
    command = row.get("subsystemCommand") if row else None
    if command is None:
        return ""
    openDialog(state, "subsystem", {"about": {"lines": [
        ("runs", "%s %s" % (command["what"], command["name"])), ("by", "--manager-subsystem-run"), SUBSYSTEM_RUNS[command["what"]]]}},
        about={"name": command["name"], "what": command["what"]}, title="%s %s" % (command["what"].capitalize(), command["name"]))
    return ""


## Run: the operation runs in the big output dialog, which follows what it writes; the list is read again when it ends.
def submitSubsystem(state, dialog, button):
    about = dialog["about"]
    closeDialog(state)
    runFollowed(state, "%s %s" % (about["what"].capitalize(), about["name"]), ["--manager-subsystem-run", about["what"], about["name"]])
    return None


DIALOGS["subsystem"] = {"title": "Run", "feeds": "subsystem",
                        "controls": ({"name": "about", "kind": "text"},),
                        "buttons": (("run", "Run"), ("cancel", "Cancel"))}
DIALOG_HANDLERS["subsystem"] = submitSubsystem
ACTION_HANDLERS["subsystem"] = askSubsystem
ACTION_FITS["subsystem"] = lambda state, row: bool(row and row.get("subsystemCommand"))


## ---- the plugin: `Installed Subsystems` ----

registerPlugin({
    "name": "subsystems",
    "mount": "configuration",
    "root": {"id": "subsystems", "label": "Installed Subsystems"},
    "focus": {"subsystems": "subsystemsFocus"},
    "summaries": {
        "subsystems": {"lines": "subsystemsSummary"},
    },
    "reads": {
        ## The subsystems of the family and what may be done with each. Read on entering it and when it is asked for, not on the period.
        "list:subsystems": {"operation": ["--manager-subsystem-list"], "rows": "subsystems", "once": True},
    },
    "commands": (
        {"name": "subsystem", "keys": ("ENTER",), "menu": ("view", 3), "label": "R~u~n the command", "status": "Run",
         "views": ("subsystems",), "for": "a command of a subsystem", "on": ("subsystems:subsystem-command",), "only": True, "enters": True, "says": "run",
         "does": ("action", "subsystem")},
    ),
})
