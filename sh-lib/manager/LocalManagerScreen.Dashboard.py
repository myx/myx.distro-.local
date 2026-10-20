##
## LocalManagerScreen.Dashboard.py -- the Dashboard of the console and the drawing of panels (F11.4 of the refactorings epic). The Dashboard is a super-system of the
## local tools, common to every console of the family: each subsystem registers its own panels, and the submenus that show more of one, in the plain list file
## of its console, and `--manager-dashboard-read` (LocalTools.ManagerDashboard.include) prints them with no python. This part draws them and takes the keys: the
## panels, the blocks of figures with their levels and gauges, drawn for the Dashboard and for the root `Team Data` of the agents (which calls this drawing), and
## the root `Dashboard (Monitor)` with its submenus.
## A part of the manager screen of the agents console (myx.distro-agents, sh-lib/manager/AgentsManagerScreen.py), which executes it, in its own namespace, ahead
## of the part of the sessions (LOCAL_PARTS_BEFORE) so that the Dashboard stands first in the list, when this package stands beside it. It is plain text of
## the screen and is never run by itself.
##

## ---- the drawing of panels: blocks of figures ----

## What the root `Dashboard (Monitor)` shows: blocks of figures, each block and each figure
## as its operation prints it; the screen knows no block and no figure by its name, and
## draws whatever comes. "block" and "figure": the names of the fields of such a row after
## the first, as the family writes them, `_` for a blank and `-` for absent; what stands
## after them in a row is left alone. "units": how a value shows by its unit, the name of
## the function that makes it short for the eye; a value of another unit shows as it is
## printed. "levels": the levels of a figure in their order, the worst last, each with
## the look its value is drawn in and the mark that stands ahead of the value where the
## style has no colours, so that bold and a mark tell it there. "bar": how many cells the
## bar of a figure that is a share takes beside its value. "least": the least width of a
## block: as many columns as blocks of that width fit are set side by side. "gap": the
## cells between two columns.
DASHBOARD = {
    "block": ("key", "label", "figures"),
    "figure": ("block", "key", "label", "value", "unit", "level", "share"),
    "units": {"count": "shortCount", "bytes": "shortBytes", "seconds": "shortSpan"},
    "levels": (("ok", {"look": LEVEL_OK, "mark": "+"}),
               ("warn", {"look": LEVEL_WARN, "mark": "!"}),
               ("bad", {"look": LEVEL_BAD, "mark": "!!"})),
    "bar": 10, "least": 34, "gap": 1,
}


## What `--manager-dashboard-read` printed, as rows: a row for each `block`, in the order
## they come, which keeps the `figure` rows that name it, in theirs. A figure of a block
## that was not printed, and a row too short to be either, is left out; what a row holds
## after the fields DASHBOARD names is left alone. A block shows by its label, and at the
## end of its line the level of its worst figure, as the operation names it, where that is
## not the first of the levels.
def parseBlockRows(text):
    rows = []
    byKey = {}
    for line in text.split("\n"):
        fields = line.split("\t")
        if fields[0] == "block" and len(fields) > len(DASHBOARD["block"]):
            block = dict(zip(DASHBOARD["block"], fields[1:]), figures=[])
            row = newRow(block["key"], unspaced(block["label"]) or block["key"], "record", False, fields)
            row["block"] = block
            byKey[block["key"]] = row
            rows.append(row)
        elif fields[0] == "figure" and len(fields) > len(DASHBOARD["figure"]) and fields[1] in byKey:
            byKey[fields[1]]["block"]["figures"].append(dict(zip(DASHBOARD["figure"], fields[1:])))
    order = [name for name, level in DASHBOARD["levels"]]
    for row in rows:
        worst = max([order.index(figure["level"]) for figure in row["block"]["figures"] if figure["level"] in order] + [0])
        if worst:
            row["tail"] = order[worst]
    return rows


## What a figure shows as its value: short for the eye by its unit (DASHBOARD), else as it
## is printed.
def figureValue(figure):
    shorten = DASHBOARD["units"].get(figure["unit"])
    return globals()[shorten](figure["value"]) if shorten else figure["value"]


## One block as a box of exactly that many cells a line: its label in the top border, and
## a line a figure, its label at the left and its value at the right, in the look of its
## level; where the style has no colours the mark of the level stands ahead of the value.
## A figure that is a share has a bar and its hundredths after its value, or, where they
## do not fit beside it, a bar of its own under it, as wide as the box. A value too long
## to stand beside its label stands under it, at the right; one longer than a line stands
## there whole, from the left, on as many lines as it takes. `place` is the rule of the locations for a value, where the view takes it: the
## key of a location in a value then stands in its own look, while the value is whole.
## Gives the lines and, for each, what of it is drawn in a look of its own.
def blockBox(block, width, place=None):
    frame = MARKS["frame"]
    inner = max(1, width - 4)
    levels = dict(DASHBOARD["levels"])
    label = fitToCells(unspaced(block["label"]) or block["key"], max(1, width - 6))
    top = frame[0] + frame[1] + " " + label.rstrip() + " "
    lines = [cutToCells(top + frame[1] * max(0, width - textWidth(top) - 1), width - 1) + frame[2]]
    looks = [[(3, textWidth(label.rstrip()), BOLD)]]

    def put(body, spans=()):
        lines.append(frame[3] + " " + cutToCells(body, inner) + " " + frame[3])
        looks.append([(2 + start, cells, look) for start, cells, look in spans if cells > 0])

    for figure in block["figures"]:
        level = levels.get(figure["level"])
        look = level["look"] if level else BOLD
        name = unspaced(figure["label"]) or figure["key"]
        value, keys = place(figureValue(figure)) if place else (figureValue(figure), [])
        if level and level["mark"] and not STYLE["colours"]:
            keys = [(start + textWidth(level["mark"]) + 1, cells, keyLook) for start, cells, keyLook in keys]
            value = level["mark"] + " " + value
        share = min(100, int(figure["share"])) if figure["share"].isdigit() else None
        bar = min(DASHBOARD["bar"], inner - 5)
        beside = share is not None and bar > 0 and textWidth(name) + 2 + textWidth(value) + bar + 6 <= inner
        room = inner - (bar + 6 if beside else 0)
        if textWidth(name) + 2 + textWidth(value) > room:
            ## the value under its label: at the right, or whole on its own lines
            put(name)
            name = ""
            pieces = areaLines(value, room) if textWidth(value) > room else []
            for number, piece in enumerate(pieces):
                put(piece, [(0, textWidth(piece), look)] + [span for span in keys if not number and span[0] + span[1] <= textWidth(piece)])
            if pieces:
                value = None
        if value is not None:
            valueAt = room - textWidth(value)
            spans = [(valueAt, textWidth(value), look)] + [(valueAt + start, cells, keyLook) for start, cells, keyLook in keys]
            body = cutToCells(name, valueAt) + value
            if beside:
                filled = (share * bar + 50) // 100
                body += " " + MARKS["barThumb"] * filled + MARKS["barTrack"] * (bar - filled) + " %3d%%" % share
                spans += [(room + 1, filled, look), (room + 1 + filled, bar - filled, DIM)]
            put(body, spans)
        if share is not None and not beside and inner > 8:
            bar = inner - 5
            filled = (share * bar + 50) // 100
            put(MARKS["barThumb"] * filled + MARKS["barTrack"] * (bar - filled) + " %3d%%" % share,
                [(0, filled, look), (filled, bar - filled, DIM)])
    lines.append(frame[4] + frame[1] * max(0, width - 2) + frame[5])
    looks.append([])
    return lines, looks


## Blocks as a grid that fills that many cells: as many columns as blocks of the least
## width fit, all of one width but the last, which takes what is left; each block is set
## under the column that is the shortest so far, in the order the blocks come. Gives the
## lines and what of each is drawn in a look of its own, by the number of the line.
def blockGrid(blocks, width, place=None):
    gap = DASHBOARD["gap"]
    columns = max(1, min(len(blocks), (width + gap) // (DASHBOARD["least"] + gap)))
    widths = [(width - gap * (columns - 1)) // columns] * columns
    widths[-1] = width - gap * (columns - 1) - sum(widths[:-1])
    stacks = [[] for column in range(columns)]
    for block in blocks:
        column = min(range(columns), key=lambda index: len(stacks[index]))
        stacks[column].extend(zip(*blockBox(block, widths[column], place)))
    lines = []
    looks = {}
    for index in range(max(len(stack) for stack in stacks)):
        text = ""
        spans = []
        for column, stack in enumerate(stacks):
            left = sum(widths[:column]) + gap * column
            boxText, boxSpans = stack[index] if index < len(stack) else (" " * widths[column], ())
            text += (" " * gap if column else "") + boxText
            spans.extend((left + start, cells, look) for start, cells, look in boxSpans)
        lines.append(text.rstrip())
        if spans:
            looks[index] = spans
    return lines, looks


## The dashboard for the left pane: every block the operation gave, as a grid; or the one
## block of the selected row, as wide as the window. None until its read has answered,
## and while what it would set out is what stands there already: the same rows, at the
## same width, in the same style, with the same locations known. Panels have no cut mode:
## they are set out to the pane as it stands on the terminal, whatever `w` is, and the
## view says it shows them (panelsShown).
def blocksView(state, only=None, level=None):
    rows = state.rows.get(level or pluginLevel("dashboard"))
    if rows is None:
        return None
    places = state.rows.get(pluginLevel("places"))
    stamp = (only, state.paneWidth, STYLE["name"], MARKS["plain"])
    kept = state.view.get("blocksFor")
    if kept is not None and kept[0] is rows and kept[1] is places and kept[2] == stamp:
        return None
    state.view["blocksFor"] = (rows, places, stamp)
    blocks = [row["block"] for row in rows if row.get("block") and only in (None, row["id"])]
    state.view["panels"] = bool(blocks)
    if not blocks:
        state.view["looks"] = {}
        return ["Nothing to show here: the operation gave no block."]
    place = (lambda text: placedLine(state, text)) if placedShown(state) else None
    return panelLines(blocks, max(20, state.paneWidth - 2), place)


## Whether the left pane shows panels (blocksView): its lines are then wrapped, whatever `w` is.
def panelsShown(state):
    return bool(state.view.get("panels"))


## The dashboard as a folder: all its blocks (the root `Dashboard (Monitor)`, which the local tools register).
def dashboardSummary(state, path, row, form):
    return blocksView(state)


## What the left pane shows of the block selected: that block alone, as wide as the window (the dashboard and its submenus, and the blocks of Team Data).
def dashboardFocus(state, row):
    return blocksView(state, row["id"], levelKey(state.path)) if row.get("block") else None


## ---- the Dashboard and its submenus ----

## The fields of a `group` row of `--manager-dashboard-read`, after its first: a Dashboard submenu a subsystem registers, and how many panels it holds.
DASHBOARD_GROUP_FIELDS = ("key", "label", "panels")


## What `--manager-dashboard-read` printed for the Dashboard itself, as rows: its blocks, as the screen reads blocks anywhere (parseLevels, form "blocks"), and, after
## them, a row for each submenu that applies, which opens a level of its own. A line of another name and one too short are left out.
def parseDashboardLevels(readKey, level, text):
    levels = parseLevels(readKey, "blocks", text)
    for printed in text.split("\n"):
        fields = printed.split("\t")
        if fields[0] != "group" or len(fields) <= len(DASHBOARD_GROUP_FIELDS):
            continue
        held = dict(zip(DASHBOARD_GROUP_FIELDS, fields[1:]))
        row = newRow(held["key"], unspaced(held["label"]) or held["key"], "dashboard-group", True, fields)
        row["group"] = held
        row["tail"] = "%s panel%s" % (held["panels"], "" if held["panels"] == "1" else "s")
        levels[level].append(row)
    return levels


## What a submenu printed, as rows: its blocks alone. They are the rows of the level of the submenu, and no other level is filled from them.
def parseDashboardPanelLevels(readKey, level, text):
    return {level: parseBlockRows(text)}


ROW_FORMS["dashboard"] = parseDashboardLevels
ROW_FORMS["dashboard-panels"] = parseDashboardPanelLevels


## What the left pane shows of a submenu, selected at the Dashboard or opened: all its panels, as a grid.
def dashboardGroupSummary(state, path, row, form):
    return blocksView(state, None, levelKey(path))


## ---- the plugin: `Dashboard (Monitor)` ----

registerPlugin({
    "name": "dashboard",
    "root": {"id": "dashboard", "label": "Dashboard (Monitor)", "go": "~D~ashboard (Monitor)", "group": "watch"},
    "focus": {"dashboard": "dashboardFocus", "dashboard/*": "dashboardFocus"},
    "summaries": {
        "dashboard": {"lines": "dashboardSummary"},
        "dashboard/*": {"lines": "dashboardGroupSummary"},
    },
    "reads": {
        ## The blocks of the dashboard, each with its figures, and the submenus that apply, all from the one operation. It is
        ## read on the period only while its root is selected or opened, and never else.
        "list:dashboard": {"operation": ["--manager-dashboard-read"], "rows": "dashboard", "peek": True},
        ## The blocks of one submenu, {level} being its key. Read as the Dashboard is, with the same period.
        "list:dashboard/*": {"operation": ["--manager-dashboard-read", "--group", "{level}"], "rows": "dashboard-panels", "peek": True},
    },
})
