##
## LocalManagerScreen.Workspace.py -- the root `Workspace (System)`: the workspace the console runs in, its own facts, the subsystems installed in it, and the blocks the consoles of
## the family add (F11.10 of the refactorings epic).
## A part of the manager screen of the agents console (myx.distro-agents, sh-lib/manager/AgentsManagerScreen.py), which executes it, in its own namespace, after its own parts
## (LOCAL_PARTS), when this package stands beside it. It is plain text of the screen and is never run by itself. The root is `.local`'s: the operation is `.local`'s
## (--manager-workspace-read, which the dispatcher of any console of the family offers), and the screen only draws its rows and takes the keys. It renders and does not compute: the
## blocks a console adds (the agents' mode of the workspace, the members that belong to it) are written by that console's readers, never by this part; a block it knows nothing of is
## drawn as every other, by its label, its facts and its items. Looking only: nothing here changes the workspace.
##

## The fields of an `item` row of `--manager-workspace-read`, after its block.
WORKSPACE_ITEM = ("name", "kind", "state", "detail")
## What the facts are called in the pane: a name the operation gives is shown by these words, any other by its own with the dashes read as blanks.
WORKSPACE_FACT_WORDS = {"tooling": "tooling from", "tooling-path": "tooling path", "account": "runs as"}
## A path stands as it is here, not by the key of the location it lies in (PLACED, Roots.py): this is the view of the workspace itself.
PLACED["real"]["workspace"] = None


def workspaceFactName(name):
    return WORKSPACE_FACT_WORDS.get(name, name.replace("-", " "))


## What `--manager-workspace-read` printed, as the rows of the root: first the workspace, by its name, then each block, by its label with how many things it holds at the end of the
## row, and under it, indented, one row for each of its items with its state at the end of it. The facts of the workspace and of each block stay with their row, for the left pane. A row
## of another name, and one too short, is left out.
def parseWorkspaceRows(readKey, level, text):
    own = []
    blocks = []
    held = {}
    for line in text.split("\n"):
        fields = line.split("\t")
        if fields[0] == "fact" and len(fields) >= 4:
            if fields[1] == "-":
                own.append((workspaceFactName(fields[2]), absent(fields[3])))
            elif fields[1] in held:
                held[fields[1]]["facts"].append((workspaceFactName(fields[2]), absent(fields[3])))
        elif fields[0] == "block" and len(fields) >= 4:
            block = {"id": fields[1], "label": unspaced(fields[2]), "facts": [], "items": [], "fields": fields}
            held[fields[1]] = block
            blocks.append(block)
        elif fields[0] == "item" and len(fields) >= 6 and fields[1] in held:
            held[fields[1]]["items"].append(dict(zip(WORKSPACE_ITEM, [absent(field) for field in fields[2:]])))
    rows = []
    name = next((value for fact, value in own if fact == "name"), "") or "Workspace"
    head = newRow("workspace", name, "workspace", False)
    head["workspace"] = {"facts": own}
    head["look"] = BOLD
    rows.append(head)
    for block in blocks:
        row = newRow(block["id"], block["label"], "workspace-block", False, block["fields"])
        row["workspaceBlock"] = block
        row["look"] = BOLD
        if block["items"]:
            row["tail"] = str(len(block["items"]))
        rows.append(row)
        for item in block["items"]:
            one = newRow("%s:%s" % (block["id"], item["name"]), item["name"], "workspace-item", False)
            one["workspaceItem"] = dict(item, block=block["label"])
            one["indent"] = 2
            one["tail"] = item["state"]
            rows.append(one)
    return {level: rows}


ROW_FORMS["workspace"] = parseWorkspaceRows


## The items of a block as one table of the left pane: the name, its kind, its state in its colour, and where it is.
def workspaceItemTable(state, items, width):
    head, blocks = paneTable(("NAME", "KIND", "STATE", "WHERE"), [[item["name"], item["kind"] or "-", item["state"] or "-", item["detail"] or "-"] for item in items],
                             max(10, width - 1), None, state.wrap, ("key", "enum", "enum", "text"), "  ",
                             looks=[[None, None, stateLook(item["state"]), None] for item in items])
    return head + [line for block in blocks for line in block]


## One block for the left pane: its facts, then its items as a table.
def workspaceBlockLines(state, block, width):
    lines = factLines(block["facts"], width)
    if block["items"]:
        lines = lines + (["" ] if lines else []) + workspaceItemTable(state, block["items"], width)
    return lines


## What the root holds, for the left pane while the section itself is selected: the facts of the workspace, then each block under its label. None until its read has answered.
def workspaceSummary(state, path, row, form):
    rows = state.rows.get(levelKey(path))
    if rows is None:
        return None
    lines = []
    for held in rows:
        if held.get("workspace"):
            lines.extend(factLines(held["workspace"]["facts"], state.viewWidth))
        elif held.get("workspaceBlock"):
            lines.extend(headingLines(held["workspaceBlock"]["label"]) + workspaceBlockLines(state, held["workspaceBlock"], state.viewWidth))
    return lines or [looked("The operation printed nothing of this workspace.", BOLD)]


## The selected row of the root for the left pane: the workspace by its facts; a block by its label, its facts and its items; an item by what it is.
def workspaceFocus(state, row):
    if row.get("workspace"):
        return [looked(row["label"], BOLD)] + factLines(row["workspace"]["facts"], state.viewWidth)
    if row.get("workspaceBlock"):
        return [looked(row["label"], BOLD)] + workspaceBlockLines(state, row["workspaceBlock"], state.viewWidth)
    if row.get("workspaceItem"):
        item = row["workspaceItem"]
        return [looked(item["name"], BOLD)] + factLines([
            ("block", item["block"]),
            ("kind", item["kind"]),
            ("state", item["state"], stateLook(item["state"])),
            ("where", item["detail"]),
        ], state.viewWidth)
    return None


## ---- the plugin: `Workspace (System)` ----

registerPlugin({
    "name": "workspace",
    "root": {"id": "workspace", "label": "Workspace (System)", "go": "~W~orkspace (System)", "group": "places"},
    "focus": {"workspace": "workspaceFocus"},
    "summaries": {"workspace": {"lines": "workspaceSummary"}},
    "reads": {
        ## The workspace the console runs in, with the blocks of every subsystem that adds one. Read on entering it and when it is asked for, not on the period.
        "list:workspace": {"operation": ["--manager-workspace-read"], "rows": "workspace", "once": True},
    },
})
