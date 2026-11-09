##
## LocalManagerScreen.Constants.py -- the vocabulary every part of the manager screen reads: where a list
## starts, the line that goes up, the words a row of the team data and of the grants is keyed by, the
## calls the screen offers, and the registries each part writes its own entries into (`READS`, `ROW_FORMS`,
## `PLAN_FORMS`, `VIEW_FORMS`, `DIALOGS`, `DIALOG_HANDLERS`, `VIEW_PARTS`, `COMMANDS`). It is loaded before every other
## part, so nothing a part writes can arrive before the thing it writes into exists.
##
## This file is the screen's vocabulary and stays so. Every registry is defined here and nowhere else: a
## second assignment in any part would replace the dict and silently drop every registration made before it.
## The load order is necessary and not sufficient for that reason.
##

## The root the selection is on when the screen starts: the manuals, whose help is where a user starts.
START_ROOT = "manuals"

## The console user's own setting of .local, beside MDLT_CONSOLE_HISTORY and no setting of
## the agents, that turns every spacer of the list off where it reads `disable`; the
## spacers are there where it names nothing else. Read from the environment of the start,
## where the start of the screen (`--manager`) puts what the user saved.
SPACERS_VARIABLE = "MDLT_MANAGER_SPACERS"

## What the root `Team Data` shows, from two reads that give it: the blocks of the
## dashboard it holds as rows of its own, read with the dashboard ("blocks"); the block and the figure that say that its team data is there ("present",
## with that value), and the figure of its root; the prefix of the figures that count the
## items of the board by state ("board"); and the lines of the digest of the settings it
## shows, each by its subject, its group (None: any) and its key: the mode of the
## workspace, whether it is a full team rig, the remote and the branch of the team data.
## "teamRig": the mode in which the team data is maintained here, the one mode an operation
## that needs a rig is offered in (CLEANUPS). "data", "git", "loop": the blocks of the team
## data, of its git state, and of the main loop; "blocks", those the dashboard's own read
## gives the root too, so that it knows from the start whether the team data is there.
TEAM_DATA = {
    "blocks": ("team-data", "loop"),
    "data": "team-data", "git": "team-data-git", "loop": "loop",
    "present": ("team-data", "present", "yes"),
    "root": "root",
    "board": "board-",
    "mode": ("workspace", "mode", "MDAT_WORKSPACE_MODE"),
    "full": ("workspace", "mode", "full-team-rig"),
    "remote": ("scopes", None, "TEAM_DATA_GIT_REMOTE"),
    "branch": ("scopes", None, "TEAM_DATA_BRANCH"),
    "teamRig": "team-rig",
    "justAgents": "just-agents",
}

ROOT_TITLE = "/"

ROW_UP = ".."

## What each action asks the tooling for: the operation with its arguments, {id} the id of
## what it acts on. The screen itself signals no process and starts no CLI. A session's id
## finishes that session: every live run of it is ended, its questions that wait are
## dismissed and its records left open are closed; `--run` takes the id as a run's own, so on the row of an
## agent that agent alone is ended, the founder too, whose id is its session's. A start
## names its routine by its selector, or takes the standing default routine with what was
## typed as its task text, which goes on standard input and is never a word of the command.
## One member is started by its name, with what was typed as its prompt, on standard input too.
## The control thread of a session is started again by the id of that session: whether one
## is started is the operation's to say, which starts none where one lives or none is needed.
CALLS = {
    "kill:session": ["--manager-session-kill", "--session-id", "{id}"],
    "kill:run": ["--manager-session-kill", "--session-id", "{id}", "--run"],
    "control": ["--manager-session-control-start", "--session-id", "{id}"],
    ## a session is paused, and resumed, by its id: its runs hold at their next pause point, and nothing of them ends (S19.1)
    "pause": ["--manager-session-pause", "--session-id", "{id}"],
    "resume": ["--manager-session-resume", "--session-id", "{id}"],
    ## the soft stop: the runs are dismissed and end themselves at their next Wait; the hard one is the kill
    "stop:session": ["--manager-session-stop", "--session-id", "{id}"],
    "stop:run": ["--manager-session-stop", "--session-id", "{id}", "--run"],
    ## the restart: a start again of what has stopped or finished, never of what runs
    "restart:session": ["--manager-session-restart", "--session-id", "{id}"],
    "restart:run": ["--manager-session-restart", "--session-id", "{id}", "--run"],
    "launch": ["--spawn-session", "--routine", "{id}"],
    "prompt": ["--spawn-session", "--routine-default"],
    "start": ["--manager-spawn-member", "{id}"],
    ## a pending question is answered, rejected by the negative answer of its kind, or
    ## dismissed, by its id; the answer chosen or typed is the word after --answer
    "answer": ["--manager-pending-reply-answer", "--id", "{id}", "--answer"],
    "reject": ["--manager-pending-reply-answer", "--id", "{id}", "--reject"],
    "dismiss": ["--manager-pending-reply-dismiss", "--id", "{id}"],
    ## a setting is saved by its key, the value chosen or typed being the word after it,
    ## as it was chosen or typed; whom it is saved for is the operation's to say
    "set": ["--manager-config-set", "{id}"],
    ## clearing one key of a scope: the tier assignment of a member is a key of its own scope, and until
    ## this existed the screen had no way to take it back -- a member pinned to a preset could not be
    ## returned to inheriting the team's. The operation deletes the key; the caller names the scope bare.
    "clear": ["--agents-config-option", "{id}", "--delete"],
}

## The word that confirms a kill, typed whole.
KILL_WORD = "yes"

## Where what a read of a store says of the store itself is kept, and the whole help of a
## member, beside the rows of their level: under the level, behind these words.
STORE_OF = "store:"

WHOLE_OF = "whole:"

## Where the chapters of the help are kept, by the level whose read gave them (parseHelpChapters).
CHAPTERS_OF = "chapters:"

## What the read of a member printed of its grants, as kept: the grants, which the folder of `Permissions` makes its rows of
## (memberGrantRows) each time it is drawn, since what a grant shows of its session is what that session is now.
GRANTS_OF = "store:grants:"

## The private place of the rows of the sessions of the last read of the list, among the rows the screen holds (state.rows):
## no level of the list is its own. Every list of `Activity` is made from these rows, and so is every list of the
## sessions of a member (the lists of ACTIVITY_LISTS, derivedRows).
SESSIONS_OF = "store:sessions"


## The rule of the locations: a path that lies in a registered location shows as the key
## of that location, a colon and what follows it there, `<place key>:rest`, the location
## itself as its key alone, the longest location winning, the key in the look of a folder. It is a rule of the drawing alone: what the
## screen holds, what it sends to an operation, a link and a command are never changed by
## it. "real": the views where a path stands as it is, each by the root it is under and,
## where that is not the whole root, by the ids of the rows and levels under it: the table
## of the locations and the summary of one; the subject of the workspace's paths, in the
## settings and in the configuration; and what is started with the whole terminal, whose
## folder and command are exact. The raw mode of a log is such a view too, wherever it
## is. In the summary of a location, the folder of a member that lies in another location
## takes the rule all the same (placeLines). "dialogs": the dialogs whose text takes the rule,
## the path as it is standing under its paragraph as a line of its own: the answers to a
## pending question.
PLACED = {
    "real": {"places": None, "consoles": None, "settings": ("workspace",), "configuration": ("workspace",)},
    "dialogs": ("answer", "answer-many", "reply", "reject", "dismiss", "confirm"),
}


## ---- the screen's shared vocabulary: the registries every part writes into ----

## The forms of rows an app feature adds to those parseLevels reads: by the name an entry of READS gives under "rows", the function (readKey, level, text)
## that gives the levels that read fills, as parseLevels returns them.
ROW_FORMS = {}

## The forms of what a read that is no list and no view gives, which an app feature adds (applyResult): by the name an entry of READS gives under "rows",
## the function (text) that gives what the read printed as the screen keeps it, in the plan of the read (state.plans), with its words and its error.
## The form registries: a row states every fact the engine needs of its form, and the registry is given the
## list of those facts. A row that omits one is refused here, naming the form and the fact, so no site can
## store one and no reader has to check.
class FormRegistry(dict):
    def __init__(self, needs):
        dict.__init__(self)
        self.needs = needs

    def __setitem__(self, name, row):
        for need in self.needs:
            if not isinstance(row, dict) or not row.get(need):
                raise SystemExit("⛔ ERROR: LocalManagerScreen.Constants: the form %s states no %s, so nothing was started" % (name, need))
        if "applies" in self.needs and row["applies"] not in ("always", "reading-dialog"):
            raise SystemExit("⛔ ERROR: LocalManagerScreen.Constants: the form %s states no applies value, so nothing was started" % name)
        dict.__setitem__(self, name, row)


PLAN_FORMS = FormRegistry(("parse", "applies"))

## The forms of what a view fills, which an app feature adds (applyResult): the function (text) that gives
## what the read printed, and under "fills" the part of the view (state.view) it fills.
VIEW_FORMS = FormRegistry(("parse", "applies", "fills"))

## Two kinds of registry live here. The three of forms above carry a schema, and FormRegistry validates a row as it is
## stored. A registry of bare callables carries no fact to validate and stays a plain dict: its mis-keying is caught
## where it is used, and not here.

## What each level of the list and each view of the left pane asks the tooling for: the operation with its arguments, as the
## dispatcher takes them, and under "active" what the `a` filter adds. None: no operation yet, the task of that level or view
## names it. A level below a record is named with `*` in the place of that record's id, and {level} in an argument is that id. A view
## is named by its level and the kind of the row that is selected there, and {id} in an argument is the id of that row. An entry
## with "always" is read whatever is shown, since a status line counts by it, and "kind" then names the kind it runs as, beside
## the one list and the one view that are shown. "rows" names the form of what a list operation prints (parseLevels). A level with
## "from" has no read of its own: the read named there fills it. Beside the "view" of a row, its facts, stands its "feed", its
## lines, read as a kind of its own; "log" is what `l` adds to it. "needs" names what a row must carry for the read to be made at
## all. "acts" is what can be done with a row, read as one more part of it (VIEW_PARTS). "once": it is read when it is asked for, and
## never again because its period has passed (startDueReads). "seldom": a list that is read whatever is shown is read once, when
## the screen starts; it is read again, on the period and when a read is asked for, only while it is the list shown (seldomNow).
## "count": the name of a counter; the operation of the list with `--count` added, which prints only the number of its rows, is read whatever is
## shown, on the period, as a read of its own, "count:<name>", and the number it printed is kept as that counter (applyResult, state.counters).
## "peek": a list that is read also while its section is the row the root stands on, since the left window then shows that
## section from its rows (wantedReads). "also": the reads made beside the list of a level, by their keys, while that level is
## shown and while the folder that opens it has the focus, as a kind of their own. "recheck": a read that is forced at every readNow (an action ended, a refresh, a followed command ended), for what decides what stands in
## the list at all, with "always" and "seldom". "demand": it is read only when its command asks
## for it ("demand" in COMMANDS), never because it was not read yet or its period has passed, and "said" is what the status line
## says of it then. {parent} in an argument is the id of the level above the level read: the member of a folder of a member.
## "each": a read that is made for every row of the level it is named by that carries what it "needs", by the id of that row;
## its key is its name and, after a `|`, that id (readEntry). The list of a level is read also while the row that opens that level
## is the row selected, a folder that has the focus, as it would be on entering it (focusReads): once the selection has rested on
## that row (REST_SECONDS), so a selection that runs down a list starts none, and one such read at a time, as the kind "focus",
## beside the list shown, and once for each time the selection comes to rest there: while it stays, the period reads that list no
## more, and coming back reads it again only when its period has passed since. "peek" is read with no rest, and on the period.
## One that is read on "demand" alone is never started by the focus: its command asks for it there too.
VIEW_PARTS = ("view", "feed", "acts", "fact")

READS = {"view::section": None}

## The commands of the engine, declared in Windows.py; COMMANDS is built from them and from every command of the plugins, in the
## order they stand in, with a command of the Go menu for each root. The levels, besides the roots, that have a number key and a
## command of the Go menu (the plugins' "go").
COMMANDS = []

## The dialogs, each declared once by its name. "title": what stands in its top border,
## where the one that opens it gives no other. "controls": its controls from the top, each
## with its name, its kind of CONTROL_KINDS and, for one that is not a text, its "label",
## the line above it. "buttons": its buttons, the name of each and what it shows as between
## brackets; the first is the one Enter presses, and one named "cancel" does what Esc does.
## "feeds": the command of COMMANDS it asks for, or the commands, whose operations its
## handler calls (DIALOG_HANDLERS); a dialog with none only says something. "first": the
## control the keys are on when it opens, where that is not its first one. "reads": the entries of
## READS that are read while it is open, since it offers what they give (DIALOG_FILLS); a
## name there that holds {kind} is the entry of the kind of what the dialog was opened on,
## its "target", and that one is asked by the id of the target (dialogReads).
## A control may be declared "required": what the dialog says, and does not do, while that
## control holds nothing, a field only blanks, boxes none checked, or, with "exactly", while
## a field does not hold that very word. The engine holds it for every dialog (dialogMissing):
## no handler is called, the buttons that would act are greyed, and Enter presses none.
## A control of options may say under "empty" what stands in it while it has none, and
## under "digits" that a digit typed while the keys are on it picks the option whose id is
## that digit. What a
## dialog cannot know before it is opened, a text, the options of a list, comes from the
## one that opens it (openDialog). One engine draws them all and gives them the keys, in every style: adding
## a dialog is adding an entry here and, where it does something, its handler.
DIALOGS = {
    ## what the screen refuses, and what an operation answered when it failed, whole; "level":
    ## what it is of, which a style may draw it by (STYLES "levels"), "bad" what was refused
    ## or failed, and the one who opens it may say another (tell)
    "message": {"title": "Message", "controls": ({"name": "text", "kind": "text"},),
                "buttons": (("ok", "OK"),), "level": "bad"},
    ## why something cannot be done with what is selected, set out by its facts
    "information": {"title": "Information", "controls": ({"name": "text", "kind": "text"},),
                    "buttons": (("ok", "OK"),), "level": "bad"},
    ## the members a routine that any member executes is started with, in one session, and
    ## what that session is to work on
    "members": {"title": "Start the routine with members", "feeds": "launch", "reads": ("list:team",),
                "controls": ({"name": "about", "kind": "text"},
                             {"name": "members", "kind": "checks", "label": "Members",
                              "empty": "the members are being read",
                              "required": "no member is checked: check one at least, with Space"},
                             {"name": "task", "kind": "input", "label": "Comments/Scope"}),
                "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## the confirmation of a kill: exactly what will be killed, dismissed and closed, as
    ## the plan of that kill gives it, and the word that confirms it, typed whole
    "kill": {"title": "Kill", "feeds": "kill", "reads": ("plan:kill:{kind}",),
             "controls": ({"name": "about", "kind": "text"},
                          {"name": "word", "kind": "input", "label": "Type %s to kill" % KILL_WORD, "exactly": KILL_WORD,
                           "required": "nothing is killed: the word typed is not %s" % KILL_WORD}),
             "buttons": (("kill", "Kill"), ("cancel", "Cancel"))},
    ## the same confirmation where nothing of the session lives: it is closed, and its
    ## title, its button and its word say so (fillKill)
    "close": {"title": "Close", "feeds": "kill", "reads": ("plan:kill:{kind}",),
              "controls": ({"name": "about", "kind": "text"},
                           {"name": "word", "kind": "input", "label": "Type %s to close" % KILL_WORD, "exactly": KILL_WORD,
                            "required": "nothing is closed: the word typed is not %s" % KILL_WORD}),
              "buttons": (("kill", "Close"), ("cancel", "Cancel"))},
    ## the start of a routine the spawner starts as its executors: what its session is to
    ## work on, and the name of that session
    "routine": {"title": "Start the routine", "feeds": "launch",
                "controls": ({"name": "about", "kind": "text"},
                             {"name": "task", "kind": "input", "label": "Comments/Scope"},
                             {"name": "name", "kind": "input", "label": "Name of the session, or none"}),
                "buttons": (("start", "Start"), ("cancel", "Cancel"))},
    ## a prompt and who runs it: the free prompt of `Launchpad`, and the start of one
    ## member; the keys are on the prompt first
    "prompt": {"title": "Free prompt", "feeds": ("prompt", "start"), "reads": ("list:team",), "first": "prompt",
               "controls": ({"name": "about", "kind": "text"},
                            {"name": "who", "kind": "list", "label": "Who runs it"},
                            {"name": "prompt", "kind": "area", "label": "Prompt",
                             "required": "nothing is started: the prompt is empty"},
                            {"name": "name", "kind": "input", "label": "Name of the session, or none"}),
               "buttons": (("start", "Start"), ("cancel", "Cancel"))},
    ## the answer to a pending question that has answers of its own: the question as it was
    ## posted, its answers with what each does, and words to go with the one picked
    "answer": {"title": "Answer", "feeds": "answer", "first": "answers",
               "controls": ({"name": "about", "kind": "text"},
                            {"name": "answers", "kind": "list", "label": "Answers", "digits": True},
                            {"name": "words", "kind": "input", "label": "Words to go with it, or none"}),
               "buttons": (("answer", "Answer"), ("cancel", "Cancel"))},
    ## the answer to a question that takes several of its answers (its form `many`): the same, with
    ## boxes in place of the list, and at least one checked
    "answer-many": {"title": "Answer", "feeds": "answer", "first": "answers",
                    "controls": ({"name": "about", "kind": "text"},
                                 {"name": "answers", "kind": "checks", "label": "Answers",
                                  "required": "nothing is answered: no answer is checked: check one at least, with Space"},
                                 {"name": "words", "kind": "input", "label": "Words to go with them, or none"}),
                    "buttons": (("answer", "Answer"), ("cancel", "Cancel"))},
    ## the answer to a plain question: the words typed are its answer
    "reply": {"title": "Answer", "feeds": "answer",
              "controls": ({"name": "about", "kind": "text"},
                           {"name": "words", "kind": "input", "label": "The answer",
                            "required": "nothing is answered: the answer is empty"}),
              "buttons": (("answer", "Answer"), ("cancel", "Cancel"))},
    ## the confirmation of a reject, and of a dismissal, of a pending question
    "reject": {"title": "Reject", "feeds": "reject",
               "controls": ({"name": "about", "kind": "text"},
                            {"name": "words", "kind": "input", "label": "Words to go with it, or none"}),
               "buttons": (("reject", "Reject"), ("cancel", "Cancel"))},
    "dismiss": {"title": "Dismiss", "feeds": "dismiss",
                "controls": ({"name": "about", "kind": "text"},
                             {"name": "words", "kind": "input", "label": "Reason, or none"}),
                "buttons": (("dismiss", "Dismiss"), ("cancel", "Cancel"))},
    ## the confirmation of an approving answer (F6.10): an allow of a permission, the yes of a
    ## confirmation; only its OK gives the answer
    "confirm": {"title": "Confirm", "feeds": "answer",
                "controls": ({"name": "about", "kind": "text"},),
                "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## an operation refused for the authority it needs (F6.10): the same operation again, asking
    ## the one who holds it, and waiting for the answer, or returning at once with the request made
    "escalate": {"title": "Authority", "feeds": ("answer", "reject", "dismiss", "kill"),
                 "controls": ({"name": "about", "kind": "text"},),
                 "buttons": (("wait", "Request and wait"), ("enqueue", "Enqueue"), ("cancel", "Cancel"))},
    ## a public key of this server whole, to copy: its line, read while the box is open
    "keyline": {"title": "Public key", "reads": ("full:{kind}",),
                "controls": ({"name": "text", "kind": "text"},),
                "buttons": (("ok", "OK"),)},
    ## the confirmation of a cleanup of `Team Data`: what will run, and that it runs at once
    "cleanup": {"title": "Run", "feeds": "cleanup",
                "controls": ({"name": "about", "kind": "text"},),
                "buttons": (("run", "Run"), ("cancel", "Cancel"))},
    ## the confirmation of a command of a workspace: what will run, where, and how
    "placecommand": {"title": "Run", "feeds": "placecommand",
                     "controls": ({"name": "about", "kind": "text"},),
                     "buttons": (("run", "Run"), ("cancel", "Cancel"))},
    ## the big dialog that runs an operation and follows what it writes, both its streams
    ## in the order they came, to the end unless it is scrolled up ("follow": its lines are
    ## the end of the text while nothing scrolled them, "raw": each line as it was written);
    ## then the result in a line of its own. "big": it takes most of the screen, and its
    ## first text the room the rest leaves. The one way for any command whose output is to
    ## be watched (runFollowed); its buttons are its handler's while it runs (OUTPUT_SAYS).
    "output": {"title": "Output", "big": True,
               "controls": ({"name": "output", "kind": "text", "raw": True, "follow": True},
                            {"name": "result", "kind": "text"}),
               "buttons": (("stop", "Stop"),)},
    ## a setting that offers choices: what it is now, and its choices, one of them chosen
    "setting": {"title": "Setting", "feeds": "setting", "first": "choice",
                "controls": ({"name": "about", "kind": "text"},
                             {"name": "choice", "kind": "radios", "label": "Choices"}),
                "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## a tier of the team or of a member: the preset and the effort, one of each chosen, saved as one value, `<preset>[:<effort>]`
    "setting-tier": {"title": "Setting", "feeds": "setting", "first": "preset",
                     "controls": ({"name": "about", "kind": "text"},
                                  {"name": "preset", "kind": "radios", "label": "Preset"},
                                  {"name": "effort", "kind": "radios", "label": "Effort"}),
                     "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## the style of the interface: what it is now, the style and the colours, one of each chosen
    "setting-style": {"title": "Setting", "feeds": "setting", "first": "style",
                      "controls": ({"name": "about", "kind": "text"},
                                   {"name": "style", "kind": "radios", "label": "Style"},
                                   {"name": "colours", "kind": "radios", "label": "Colours"}),
                      "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## a setting that is a number: what it is now, and the number typed, which the one
    ## that opens it labels with the range of the row (askSetting)
    "setting-number": {"title": "Setting", "feeds": "setting", "first": "number",
                       "controls": ({"name": "about", "kind": "text"},
                                    {"name": "number", "kind": "input", "label": "A whole number",
                                     "required": "nothing is saved: no number is typed"}),
                       "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## a setting of any other kind: a short text, typed
    "setting-text": {"title": "Setting", "feeds": "setting", "first": "words",
                     "controls": ({"name": "about", "kind": "text"},
                                  {"name": "words", "kind": "input", "label": "Its value",
                                   "required": "nothing is saved: nothing is typed"}),
                     "buttons": (("ok", "OK"), ("cancel", "Cancel"))},
    ## a credential: what it is, its value in the form of a credential in a field of a short text, and the
    ## button that reads it whole, which Ctrl-R presses (DIALOG_KEYS), for as long as the dialog is open
    "setting-credential": {"title": "Setting", "feeds": "setting", "first": "words", "reads": ("full:{kind}",),
                           "controls": ({"name": "about", "kind": "text"},
                                        {"name": "words", "kind": "input", "label": "Its value"}),
                           "buttons": (("ok", "OK"), ("reveal", "Reveal"), ("cancel", "Cancel"))},
}

DIALOG_HANDLERS = {}
CREDENTIAL_DIALOG = "setting-credential"

## What fills a dialog from what was read, while it is open: fill(state, dialog), called at
## every turn of the screen. Set where each is defined.
DIALOG_FILLS = {}

## What an action does to the row it is for, by the action's name: handler(state, row), set where each is defined.
## None here: the task of that action has not built it.
ACTION_HANDLERS = {
    ## asks for the typed word, then kills the selected session or agent: askKill, set where it is defined
    "kill": None,
    ## starts the control thread of the selected session again, asking nothing first: askControl, set where it is defined
    "control": None,
    "pause": None,
    "resume": None,
    "stop": None,
    "restart": None,
    ## Enter on a routine of `Launchpad`, and on its free prompt: askLaunch and askPrompt, set where they are defined
    "launch": None,
    "prompt": None,
    ## Enter and Right on a routine of `Launchpad` that cannot be started: askUnstarted, set where it is defined
    "unstarted": None,
    ## starts the selected team member with a prompt: askStart, set where it is defined
    "start": None,
    ## shows the keys of the screen, from COMMANDS: askHelp, set where it is defined
    "help": None,
    ## a pending question: its answer, its reject, its dismissal, each asked in a dialog, and
    ## the link of its message in a box: askAnswer, askReject, askDismiss, askLink, set where they are defined
    "answer": None,
    "reject": None,
    "dismiss": None,
    "link": None,
    ## Enter on a setting, inside a subject: the dialog of its kind: askSetting, set where it is defined
    "setting": None,
    ## Enter on a row of `Consoles`: it is started with the whole terminal: askRun, set where it is defined
    "run": None,
    ## the whole public line of the selected key of the server, in a box: askKeyLine, set where it is defined
    "line": None,
    ## Enter on a cleanup of `Team Data`: asked first, then run in the big output dialog: askCleanup, set where it is defined
    "cleanup": None,
    ## Enter on a command of a workspace in `Locations (Places)`: asked first, then run in the big output dialog,
    ## or with the whole terminal where it runs so: askPlaceCommand, set where it is defined
    "placecommand": None,
}

## What an action answered, for the actions an app feature adds: answer(text, about, width) gives what the call was (for its failure's title), the lines of
## the left pane and the line of the status line. Set where each is defined.
ACTION_ANSWERS = {}


## The row a form registers: its parser, and whether its answer counts always or only while a reading
## dialog is open. A row that states no applies value is refused here, once, rather than defaulted.
def formRow(name, parser, applies):
    if applies not in ("always", "reading-dialog"):
        raise SystemExit("⛔ ERROR: LocalManagerScreen.Constants: the form %s states no applies value, so nothing was started" % name)
    return {"parse": parser, "applies": applies}
