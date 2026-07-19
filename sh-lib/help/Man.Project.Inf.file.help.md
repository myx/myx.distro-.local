# Source File Format: project.inf

A project is any directory that contains a project.inf file at its root. This manifest file 
defines the project’s identity and metadata—what it requires, what it provides, how it 
should be built, and where deployment tools must connect—so that source and deployment 
systems can discover and manage it automatically.

Projects may live at any depth under your source tree but must never be nested inside one 
another: each project.inf marks the top of a standalone project - standalone directory 
hierarchy. The file itself follows a Java-properties–style syntax, including backslashes at
line ends to continue long or multi-valued properties across several indented lines. It 
supports standard escapes (\t, \n, \:, \=, \\) and Unicode (\uXXXX), giving you a flexible 
yet predictable format for all your project metadata.

Variety of notations supported, like the form ```Property: value[ value2 ...]\n``` or 
slightly different ```Property = value[ value2 ...]\n```, as well, as:

```
	Property: \
		value1 \
		value2 \
	
	...
```

In project's project.inf file we focus on following properties:

	- 'Name' - the name of the project, It should match the folder name and may include the
		full project ID (the path in the source tree).

	- 'Requires' - list of other projects or their 'Provides' items that this project depends 
		on.

	- 'Declares' - project properties that given project declares and that are applied to
		given project only.

	- 'Provides' - project properties that all other projects requiring given project will 
		inherit.

	- 'Keywords' - the search kewords for given project to be found and selected on source
		and deploy operations.


Declares are metadata entries that apply only to the project in which they’re defined—they 
describe or configure that project alone and are never passed on to dependents. Provides 
metadata entries, by contrast, are properties exported to every project that lists this one 
in its Requires. For example, an abstract-db-node module might declare (Declares) its own 
Git repository URL or internal package name (information only it needs), while providing 
(in Provides) shared initialization parameters, like: connection strings, default schemas, 
feature flags—that all requiring projects automatically inherit.


# More details on project.inf format:

##   📜 Java .properties Format Essentials

	Input format is java properties file format, that is flexible and user-friendly. So we 
	describe the basic details here.

###    ✅ Key-Value Syntax

	- key=value and key:value are both valid.

	- Whitespace around the separator (= or :) is ignored.

	- Leading whitespace before the key is ignored.

	- Trailing whitespace after the value is preserved.

###    💬 Comments

	- Lines starting with # or ! are treated as comments and ignored.

	- Blank lines are ignored.

###    🔄 Line Continuation

	- A backslash (\) at the end of a line continues the value onto the next line.

	- Leading whitespace on continued lines is ignored.

###    🔠 Escaping Special Characters

	- \: → literal colon

	- \= → literal equals

	- \\ → literal backslash

	- \t, \n, \r → tab, newline, carriage return

	- \uXXXX → Unicode character (e.g. \u002c for comma)

###    🔁 Duplicate Keys

	- If a key appears multiple times, the last occurrence wins.

###    🌍 Encoding

	- Files are expected to be in ISO-8859-1 (Latin-1) or UTF-8.
	- Non-Latin (Latin-1) or Non-Printable (Unicode) characters must be escaped using \uXXXX.

##  📜 Internal project.inf format

	In order for source tools to work efficiently with project meta-data, source system creates
	the index and internal copies of project.inf files in a stripped simplified format by 
	building local cache hierarchy. The converter utility runs on bash 3.2 or emulated sh of 
	MacOSX, FreeBSD or Linux.

###    Source project.inf parser/stripper/reformatter steps

	- Assume file is in UTF-8 encoding or all non-latin values are properly escaped;

	- Strip comments and ignore blank lines;

	- Collapse line continuations into a single logical value, collapse whitespace around continuation (if any) into single space;

	- Skip properties other than: `Name`, `Requires`, `Keywords`, `Declares`, `Provides`;

	- Normalize the first occurrence of either `:` or `=` as the key-value separator, keeping any additional separators in the value;

	- Duplicate keys produce stderr warning and concatenated with single space between existing and new value;

	- Unescape all supported sequences: `\\`, `\=`, `\:`, `\n`, `\r`, `\t`, and Unicode escapes like `\uXXXX`;

	- Output lines in strict <property>=<value> format, with values unquoted and unescaped.

###    parser/stripper/reformatter, input example

	So, an input file like: 

  ```properties
	# This is a sample project configuration
	Name: test-project

	Description: My First Test Project
	
	Requires: \
		base-system \
		core-logging \
		common-ui \

	Keywords: \
		test1 \
		test1 \

	Declares: \
		build-source-tools:actions \
		user-ext-myx:admin \

  ```

###    parser/stripper/reformatter, output example

	The stripped version, generated will look like:

	```Name=test-project```
	```Requires=base-system core-logging common-ui```
	```Keywords=test1 test1```
	```Declares=build-source-tools:actions user-ext-myx:admin```

##  🔗 Requires ↔ Provides Dependency Matching

	The dependency graph between projects is resolved by matching `Requires` tokens against
	`Provides` tokens — **not** by matching against `Name`. Project A depends on project B if
	any one of A's `Requires` tokens exactly equals any one of B's `Provides` tokens (subject to
	the colon-modifier fallback below).

	A project's own `Name` value is always an implicit member of its own `Provides` set, even
	if that value isn't separately repeated inside the project's `Provides:` line.

###    Example (real, from myx.common/os-myx.common-macosx and myx.common/os-myx.common)

	`os-myx.common-macosx/project.inf`:

	```
	Name: os-myx.common-macosx
	Requires: os-myx.common
	Provides: \
		os.any os.macosx os-myx.common-macosx myx/os-myx.common-macosx myx.common/os-myx.common-macosx \
		deploy-export:sh-scripts/install-myx.common-macosx.sh:raw.githubusercontent.com/myx/os-myx.common-macosx/master/sh-scripts/install-myx.common-macosx.sh \
	```

	`os-myx.common/project.inf`:

	```
	Name: os-myx.common
	Requires: 
	Provides: \
		os-myx.common myx.common/os-myx.common myx/myx.common/os-myx.common \
		...
	```

	`os-myx.common-macosx`'s `Requires: os-myx.common` resolves against `os-myx.common`'s
	`Provides` list, where `os-myx.common` appears explicitly (it would still resolve even if it
	didn't, via the implicit-Name rule above).

###    Colon-modifier suffix on Requires tokens

	Some `Requires` tokens carry a trailing `:modifier` that is **not** part of the identity
	being matched — a role/group-membership qualifier layered on top of the base requirement.

	Match rule: try an exact token match first; if that fails, and the token has a trailing
	`:something` with no further `/` in that segment, retry the match against the substring
	before the last colon.

	Real example (`ndm/infra/accounts-ndm/group.ndm-admins/project.inf`):

	```
	Name: group.ndm-admins
	Requires: \
		accounts/user.ndm-eliseev:admins \
		accounts/user.ndm-zerobug \
		...
	```

	`accounts/user.ndm-eliseev:admins` matches `user.ndm-eliseev/project.inf`'s
	`Provides: accounts/user.ndm-eliseev ...` — the `:admins` suffix is dropped for matching
	purposes, it is not part of the identity. (`accounts/user.ndm-zerobug`, with no colon,
	matches directly with no fallback needed.)

	This is distinct from *structured* Provides-only tokens that legitimately contain multiple
	colons as part of one literal token, e.g.
	`deploy-export:sh-scripts/install-x.sh:raw.githubusercontent.com/...` — those are Provides-side
	build/deploy-export markers matched as one whole token, and are not typically referenced back
	via Requires. So the colon-stripping fallback applies **only** on the Requires side, and only
	after an exact match attempt has already failed.

