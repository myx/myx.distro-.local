##
## LocalManagerScreen.Features.py -- the optional features of the tool family (`setup.feature-*` of mdci-packages-myx: local AI and LanceDB), in two places of the console:
## `Optional Features`, a folder of `Installed Subsystems`, which lists them with their parts and installs, updates and uninstalls a part; and `Local AI`, a folder of
## `This Machine`, which lists the parts of the local AI with their size and state, and uses them: a free prompt to a chat model, a voice test, and a `local` preset made
## from a model.
## A part of the manager screen of the agents console (myx.distro-agents, sh-lib/manager/AgentsManagerScreen.py), which executes it, in its own namespace, after its own parts
## (LOCAL_PARTS). It is plain text of the screen and is never run by itself.
##
## IT RENDERS AND DECIDES NOTHING. What a feature is, how big, whether it runs and which command applies to it is what `--manager-feature-list` prints (AgentsTools.ManagerFeature.include,
## which asks each feature's own check fragment); the plan of a part, its needs and its space, is what `--manager-feature-part` prints without `--yes`, and the run is the same
## operation with `--yes`, started only after the plan was shown and Run was pressed. The prompt, the voice test and the preset are `--manager-feature-ask`, `--manager-feature-stt-test`
## and `--manager-feature-preset`. The screen reads no file of a feature and keeps no table of its parts.
##

## ---- the rows of `--manager-feature-list` ----

## The fields of a `feature` or `part` row, after its first.
FEATURE_FIELDS = ("feature", "part", "state", "disk", "memory", "running", "install", "update", "uninstall", "detail")
## How a state reads on the screen.
FEATURE_STATE_WORDS = {"not-installed": "not installed", "unsupported": "not supported here"}
## The commands a row may be offered, in the order they are shown.
FEATURE_COMMANDS = ("install", "update", "uninstall")
## The reads the plan of a command and the dialogs of a use are held by.
FEATURE_PLAN_READ = "full:feature-part"

CALLS["feature-ask"] = ["--manager-feature-ask", "{id}"]
CALLS["feature-preset"] = ["--manager-feature-preset", "{id}"]
CALLS["feature-stt"] = ["--manager-feature-stt-test"]
PLAN_FORMS["feature-plan"] = lambda text: text


def featureStateWords(state):
    return FEATURE_STATE_WORDS.get(state, state)


## The look of a state: an installed part plain bold, a broken one bad, any other dim.
def featureLook(state):
    return BOLD if state == "installed" else (LEVEL_BAD if state == "broken" else DIM)


## What a part is offered besides its commands, by what the tooling says it is (`part=chat`, `part=stt` in its detail): the uses of an installed part.
def featureDetail(held, name):
    for item in unspaced(held["detail"]).split(","):
        key, equals, value = item.partition("=")
        if equals and key.strip() == name:
            return value.strip()
    return ""


FEATURE_USES = {"chat": (("ask", "Ask a prompt"), ("preset", "Make a local preset")), "stt": (("voice", "Voice test"),)}


## What `--manager-feature-list` printed, as rows in the order it printed them: a feature a row with its parts under it, each with the commands the tooling gives it, and
## (`uses`) under an installed part what it can be used for. A line of another name and one too short are left out; `only` keeps one feature.
def parseFeatureLevels(readKey, level, text, only=None, uses=False):
    rows = []
    for printed in text.split("\n"):
        fields = printed.split("\t")
        if fields[0] not in ("feature", "part") or len(fields) <= len(FEATURE_FIELDS):
            continue
        held = dict(zip(FEATURE_FIELDS, fields[1:]))
        if only is not None and held["feature"] != only:
            continue
        isPart = fields[0] == "part"
        row = newRow(held["feature"] + ("/" + held["part"] if isPart else ""), held["part"] if isPart else held["feature"], "feature-part" if isPart else "feature", False, fields)
        row["feature"] = held
        row["isPart"] = isPart
        row["indent"] = 1 if isPart else 0
        row["tail"] = featureStateWords(held["state"]) + (", " + shortBytes(held["disk"]) if held["disk"] not in ("0", "-") else "")
        row["look"] = featureLook(held["state"])
        rows.append(row)
        for what in FEATURE_COMMANDS:
            ## the command as the tooling printed it: its words are its own, and an underscore in one (q4_k_m) is no space
            words = held[what].split()
            if "--manager-feature-part" not in words or len(words) < words.index("--manager-feature-part") + 4:
                continue
            at = words.index("--manager-feature-part")
            command = newRow("%s:%s" % (row["id"], what), what.capitalize() + (" " + held["part"] if isPart else ""), "feature-command", False, fields)
            command["indent"] = 2
            command["featureCommand"] = {"what": what, "words": words[at:at + 4], "feature": words[at + 2], "part": words[at + 3], "state": held["state"]}
            rows.append(command)
        if uses and isPart and held["state"] == "installed":
            for use, label in FEATURE_USES.get(featureDetail(held, "part"), ()):
                useRow = newRow("%s:%s" % (row["id"], use), label, "feature-use", False, fields)
                useRow["indent"] = 2
                useRow["featureUse"] = {"use": use, "part": held["part"], "model": held["part"]}
                rows.append(useRow)
    return {level: rows}


ROW_FORMS["features"] = parseFeatureLevels
ROW_FORMS["features-ai"] = lambda readKey, level, text: parseFeatureLevels(readKey, level, text, "setup.feature-local-ai", True)


## The facts of a feature or a part, for the left pane.
def featureFacts(held):
    return [("feature", held["feature"]), ("part", "" if held["part"] == "-" else held["part"]),
            ("state", featureStateWords(held["state"]), featureLook(held["state"])),
            ("on disk", shortBytes(held["disk"])), ("in memory", ("about " + shortBytes(held["memory"])) if held["memory"] not in ("0", "-") else "-"),
            ("runs", {"yes": "yes", "no": "no"}.get(held["running"], "")),
            ("detail", unspaced(held["detail"]))]


## The folder as a table, for the left pane: every feature and part, its state in its colour, its size on disk and what it takes in memory, and whether it runs.
def featuresSummary(state, path, row, form):
    rows = state.rows.get(levelKey(path))
    if rows is None:
        return None
    held = [one for one in rows if one.get("feature")]
    if not held:
        return [looked("The operation listed no feature.", BOLD)]
    return tableSummaryLines(state, ("FEATURE", "STATE", "DISK", "MEMORY", "RUNS"),
                             [[(one["feature"]["part"] if one["isPart"] else one["feature"]["feature"]), featureStateWords(one["feature"]["state"]),
                               shortBytes(one["feature"]["disk"]), shortBytes(one["feature"]["memory"]), one["feature"]["running"]] for one in held],
                             ("key", "enum", "text", "text", "enum"),
                             looks=[[BOLD, featureLook(one["feature"]["state"]), None, None, None] for one in held])


FEATURE_RUNS = {
    "install": "It installs the part: the plan is shown first, what it needs and the space it takes, and nothing is done until Run is pressed there.",
    "update": "It takes the part out and installs it again: the plan is shown first, and nothing is done until Run is pressed there.",
    "uninstall": "It removes the part: the plan is shown first, and nothing is done until Run is pressed there.",
}
FEATURE_USES_SAY = {
    "ask": "A free prompt to this model, through the chat server it runs. No secret belongs in a prompt.",
    "preset": "A preset of the `local` CLI service made from this model, in one step.",
    "voice": "A speech-to-text test: a voice file read to text, or one second of silence.",
}


## The row selected, for the left pane: a feature or a part by its facts; a command by what it runs; a use by what it does.
def featuresFocus(state, row):
    if row.get("featureCommand"):
        command = row["featureCommand"]
        return [looked("%s %s" % (command["what"].capitalize(), command["part"]), BOLD)] + factLines([
            ("runs", "DistroAgentsTools.fn.sh " + " ".join(command["words"])),
        ], state.viewWidth) + [""] + wrapToCells(FEATURE_RUNS[command["what"]], max(10, state.viewWidth - 1))
    if row.get("featureUse"):
        use = row["featureUse"]
        return [looked(row["label"], BOLD)] + factLines([("model" if use["use"] != "voice" else "part", use["part"])], state.viewWidth) + [""] + wrapToCells(FEATURE_USES_SAY[use["use"]], max(10, state.viewWidth - 1))
    if row.get("feature"):
        return [looked(row["label"], BOLD)] + factLines(featureFacts(row["feature"]), state.viewWidth)
    return None


## ---- a command of a part: the plan first, the run when Run is pressed ----

DIALOGS["feature-part"] = {"title": "Run", "feeds": "feature", "reads": ("full:{kind}",),
                           "controls": ({"name": "about", "kind": "text"},),
                           "buttons": (("run", "Run"), ("cancel", "Cancel"))}
READING_DIALOGS = READING_DIALOGS + ("feature-part",)


## The words of the plan read of a command, as READS would make them: what the dialog is waiting for.
def featurePlanWords(state, command):
    return readWords(READS[FEATURE_PLAN_READ], state, {"id": command["part"], "_operation": ["--manager-feature-part"] + command["words"][1:]}, False)


## What `--manager-feature-part` printed without `--yes`, as the facts of a plan, in the words of a person: what is fetched and freed, the space and the memory, and whether
## the plan is blocked and why. A `need` row is a package, a model or a file the work touches.
def featurePlanLines(text):
    facts, needs, blocked = [], [], ""
    for printed in text.split("\n"):
        fields = printed.split("\t")
        if fields[0] == "plan" and len(fields) >= 11:
            names = ("action", "feature", "part", "download", "reclaim", "free", "ramNeed", "ram", "blocked", "why")
            held = dict(zip(names, fields[1:]))
            facts = [("download", shortBytes(held["download"])), ("freed", shortBytes(held["reclaim"])), ("free space", shortBytes(held["free"])),
                     ("memory it wants", shortBytes(held["ramNeed"])), ("memory of the host", shortBytes(held["ram"]))]
            if held["blocked"] == "yes":
                blocked = unspaced(held["why"]) or "the plan is blocked"
        elif fields[0] == "need" and len(fields) >= 2:
            needs.append(unspaced(fields[1]))
    return facts, needs, blocked


## Enter on a command of a part: its dialog opens and asks for the plan; the plan is the dialog's own.
def askFeature(state, row):
    command = row.get("featureCommand") if row else None
    if command is None:
        return ""
    state.answer = None
    state.plans.pop(FEATURE_PLAN_READ, None)
    state.forced.add(FEATURE_PLAN_READ)
    openDialog(state, "feature-part", {"about": {"lines": [("runs", "%s %s of %s" % (command["what"], command["part"], command["feature"])), "The plan is being read; nothing is changed by reading it."]}},
               {"command": command, "target": {"kind": "feature-part", "id": command["part"], "level": "", "read": ["--manager-feature-part"] + command["words"][1:]},
                "plan": None, "viewKey": viewKeyOf(state)}, "%s %s" % (command["what"].capitalize(), command["part"]))
    return ""


## At every turn while the dialog is open: once the plan has answered, its facts stand in the dialog, or why it could not be made.
def fillFeature(state, dialog):
    about = dialog["about"]
    if about["plan"] is not None:
        return
    plan = state.plans.get(FEATURE_PLAN_READ)
    if plan is None or plan["words"] != featurePlanWords(state, about["command"]):
        return
    state.plans.pop(FEATURE_PLAN_READ, None)
    command = about["command"]
    facts, needs, blocked = featurePlanLines(plan["rows"])
    lines = [("runs", "%s %s of %s" % (command["what"], command["part"], command["feature"]))]
    if not facts:
        about["plan"] = {"blocked": plan["error"] or "the operation printed no plan"}
        lines.append("No plan could be made: %s" % about["plan"]["blocked"])
    else:
        about["plan"] = {"blocked": blocked}
        lines.extend(facts)
        if needs:
            lines.append(("needs", ", ".join(needs)))
        lines.append("Blocked: %s. Run does nothing." % blocked if blocked else "Run does it, in a window that follows what it writes. Cancel and Esc change nothing.")
    dialogControl(dialog, "about")["lines"] = lines


## Run: only with a plan that was shown and is not blocked; the operation with `--yes` runs in the big output dialog, which follows what it writes.
def submitFeature(state, dialog, button):
    about = dialog["about"]
    if about["plan"] is None:
        return "the plan is being read: Run waits for it"
    if about["plan"]["blocked"]:
        return "the plan is blocked: %s" % about["plan"]["blocked"]
    command = about["command"]
    closeDialog(state)
    runFollowed(state, "%s %s" % (command["what"].capitalize(), command["part"]), ["--manager-feature-part"] + command["words"][1:] + ["--yes"])
    return None


DIALOG_HANDLERS["feature-part"] = submitFeature
DIALOG_FILLS["feature-part"] = fillFeature
ACTION_HANDLERS["feature"] = askFeature
ACTION_FITS["feature"] = lambda state, row: bool(row and row.get("featureCommand"))


## ---- the uses of a part of the local AI: a prompt, a voice test, a preset ----

DIALOGS["feature-ask"] = {"title": "Ask", "feeds": "featureuse", "first": "prompt",
                          "controls": ({"name": "about", "kind": "text"},
                                       {"name": "prompt", "kind": "area", "label": "Prompt", "required": "nothing is asked: the prompt is empty"}),
                          "buttons": (("ask", "Ask"), ("cancel", "Cancel"))}
DIALOGS["feature-voice"] = {"title": "Voice test", "feeds": "featureuse", "first": "file",
                            "controls": ({"name": "about", "kind": "text"},
                                         {"name": "file", "kind": "input", "label": "A voice file (.wav), or none for one second of silence"}),
                            "buttons": (("test", "Test"), ("cancel", "Cancel"))}
DIALOGS["feature-preset"] = {"title": "Make a local preset", "feeds": "featureuse", "first": "name",
                             "controls": ({"name": "about", "kind": "text"},
                                          {"name": "name", "kind": "input", "label": "Name of the preset, or none for `local`"}),
                             "buttons": (("make", "Make"), ("cancel", "Cancel"))}


## Enter on a use: its dialog, with what it does.
def askFeatureUse(state, row):
    use = row.get("featureUse") if row else None
    if use is None:
        return ""
    state.answer = None
    openDialog(state, {"ask": "feature-ask", "voice": "feature-voice", "preset": "feature-preset"}[use["use"]],
               {"about": {"lines": [("part", use["part"]), FEATURE_USES_SAY[use["use"]]]}}, {"use": use, "viewKey": viewKeyOf(state)}, row["label"])
    return ""


## Ask, Test or Make: the operation is asked once; a prompt goes on its standard input and never among its words.
def submitFeatureUse(state, dialog, button):
    about = dialog["about"]
    use = about["use"]
    if use["use"] == "ask":
        askCall(state, "feature-use", use["model"], callWords("feature-ask", use["model"]), dialogValue(dialog, "prompt").rstrip("\n") + "\n", {"viewKey": about["viewKey"], "use": "ask", "model": use["model"]})
    elif use["use"] == "voice":
        name = dialogValue(dialog, "file").strip()
        askCall(state, "feature-use", "stt", callWords("feature-stt") + ([name] if name else []), None, {"viewKey": about["viewKey"], "use": "voice", "model": use["model"]})
    else:
        name = dialogValue(dialog, "name").strip()
        askCall(state, "feature-use", use["model"], callWords("feature-preset", use["model"]) + (["--name", name] if name else []), None,
                {"viewKey": about["viewKey"], "use": "preset", "model": use["model"]})
    state.notice = "%s asked of the tooling: %s" % (use["use"], use["model"])
    state.noticeOf = None
    return None


DIALOG_HANDLERS["feature-ask"] = submitFeatureUse
DIALOG_HANDLERS["feature-voice"] = submitFeatureUse
DIALOG_HANDLERS["feature-preset"] = submitFeatureUse
ACTION_HANDLERS["featureuse"] = askFeatureUse
ACTION_FITS["featureuse"] = lambda state, row: bool(row and row.get("featureUse"))


## What the operation printed of a use, for the left pane and one line of the bottom line: the reply of the model, the words of the voice file, or the row of the preset it made.
def featureUseAnswer(text, about, width):
    use = about.get("use", "")
    said = [line for line in text.splitlines() if line.strip()]
    if use == "preset":
        for printed in said:
            fields = printed.split("\t")
            if fields[0] == "created" and len(fields) >= 3:
                return "the preset", fieldLines([("preset", fields[1]), ("model", fields[2])], width), "made the preset %s from %s" % (fields[1], fields[2])
        return "the preset", said, "the operation printed no row of a preset"
    lines = []
    for line in text.splitlines():
        lines.extend(wrapToCells(line, max(10, width - 1)) if line.strip() else [""])
    title = {"ask": "the answer of %s" % about.get("model", ""), "voice": "the voice test"}.get(use, "the use")
    return title, lines or ["the operation printed nothing"], (said[0] if said else "the operation printed nothing")[:120]


ACTION_ANSWERS["feature-use"] = featureUseAnswer


## ---- the plugins ----

registerPlugin({
    "name": "features",
    "mount": "subsystems",
    "root": {"id": "features", "label": "Optional Features"},
    "focus": {"features": "featuresFocus"},
    "summaries": {"features": {"lines": "featuresSummary"}},
    "reads": {
        ## The optional features and their parts, as their own check fragments say: read on entering it and when it is asked for, not on the period.
        "list:features": {"operation": ["--manager-feature-list"], "rows": "features", "once": True},
        ## The plan of one command of a part, for the dialog that asks first: read once, when that dialog is open.
        FEATURE_PLAN_READ: {"operation": ["--manager-feature-part"], "rows": "feature-plan", "kind": "plan", "demand": True},
    },
    "commands": (
        {"name": "feature", "keys": ("ENTER",), "menu": ("view", 3), "label": "R~u~n the command", "status": "Run",
         "views": ("features", "local-ai"), "for": "a command of a part", "on": ("features:feature-command", "local-ai:feature-command"), "only": True, "enters": True, "says": "run",
         "does": ("action", "feature")},
    ),
})

registerPlugin({
    "name": "local-ai",
    "mount": "machine",
    "root": {"id": "local-ai", "label": "Local AI"},
    "focus": {"local-ai": "featuresFocus"},
    "summaries": {"local-ai": {"lines": "featuresSummary"}},
    "reads": {
        ## The parts of the local AI, as its own check fragment says: read on entering it and when it is asked for, not on the period.
        "list:local-ai": {"operation": ["--manager-feature-list"], "rows": "features-ai", "once": True},
    },
    "commands": (
        {"name": "featureuse", "keys": ("ENTER",), "menu": ("view", 3), "label": "~U~se the part", "status": "Use",
         "views": ("local-ai",), "for": "a use of a part of the local AI", "on": ("local-ai:feature-use",), "only": True, "enters": True, "says": "use",
         "does": ("action", "featureuse")},
    ),
})
