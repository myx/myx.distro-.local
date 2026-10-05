# Formats

[Back to the README](../README.md)

## project.inf

A project is any directory with a `project.inf` file at its root. The file names the project and lists what it requires, provides and declares. Source and deploy tools read it to find and manage the project.

Projects may sit at any depth under the source tree. They are never nested inside one another.

### Syntax

- Write `Key: value` or `Key = value`. Both are valid.
- Lines starting with `#` or `!` are comments. Blank lines are ignored.
- A backslash at the end of a line continues the value on the next line.
- The escapes are `\:`, `\=`, `\\`, `\t`, `\n`, `\r` and `\uXXXX`.
- Use ISO-8859-1 or UTF-8. Escape any other character with `\uXXXX`.

A multi-valued property looks like this:

	Property: \
		value1 \
		value2 \

### Properties

- `Name` — the project name. It matches the folder name and may include the path in the source tree.
- `Requires` — other projects, or their `Provides` values, that this project depends on.
- `Provides` — values that every project requiring this one inherits.
- `Declares` — values that apply to this project only. They are never inherited.
- `Keywords` — search terms for selecting the project in source and deploy operations.

[myx.distro-source](https://github.com/myx/myx.distro-source/blob/main/docs/formats.md) lists the remaining properties.

### Matching Requires to Provides

- A `Requires` token is matched against `Provides` tokens, never against `Name`.
- A project's own `Name` is always part of its own `Provides`, even when the line does not repeat it.
- A `Requires` token may end in a modifier, such as `accounts/user.alice:admins`. The tool tries an exact match first.
- When the exact match fails, it retries without the text after the last colon. Here that matches `accounts/user.alice`.
- The fallback applies to `Requires` only. A `Provides` token with several colons, such as `deploy-export:...`, is matched whole.

### Opting a project out of a stage

Source and deploy tools select a project when a `Provides`, `Declares` or `Keywords` token begins with the selector.

Put `--` before a token to opt the project out. No selector begins with `--`, so nothing selects it. The token stays indexed and readable.

Remove the `--` to restore the project to the stage. This works for every token a selector matches.

The full grammar is in the [project.inf manual](../sh-lib/help/Man.Project.Inf.file.help.md).

## Workspace config file

The workspace config file is a list of directives, one per line. [Configuration](configuration.md) describes it.
