📘 syntax: DistroLocalTools.fn.sh --install-embedded-python [--uv-version <version>] [--from-folder <folder>]
📘 syntax: DistroLocalTools.fn.sh --install-embedded-python --help

##  Summary:

		Installs a pinned `uv` release and, with that uv, a standalone CPython build into the workspace's
		`.local/embedded-python/`, for the tools that need a Python of their own. It is an operation of its own: it does
		not combine with the `--install-distro-*` options, and it changes none of the toolsets they install.

		It works on macOS and Linux, on arm64 and x86_64 (glibc and musl). On FreeBSD, and on any other system that no
		standalone build covers, it says why, exits non-zero and writes nothing.

##  Arguments:

		None. This command is option-driven.

##  Options:

		--uv-version <version>
			Installs this uv release in place of the default one (the pinned release, set in the include
			`sh-lib/python/LocalTools.EmbeddedPython.include`). The version is three numbers with dots, as the release
			is named on https://github.com/astral-sh/uv/releases. Anything else is refused.

		--from-folder <folder>
			Installs from files downloaded once elsewhere, for a host with no internet: nothing is fetched, and the
			folder is only read. It is the `downloads` folder of an online run, copied: the uv archive
			`uv-<target>.tar.gz` with its `.sha256` beside it, and `python/` with uv's Python archive. The uv archive is
			checked against its `.sha256` before anything is written. A folder that lacks a file the install needs is
			refused, naming the file.

		--help
			Prints this manual.

##  Notes:

		The uv archive of the machine's target (`aarch64-apple-darwin`, `x86_64-apple-darwin`,
		`x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu` or the `-musl` ones) is fetched from the release page
		of the pinned version, together with the `.sha256` that uv publishes beside it, and is unpacked only when its
		sha256 is the one that file names. A checksum that does not match, is missing or is not a checksum refuses the
		install, and the archive that failed is not kept.

		The Python is a standalone CPython of the pinned minor (3.12), installed by that uv. Every folder uv uses is in
		`.local/embedded-python/`, and nothing is written in the home folder, in a shell startup file or in the system:

			uv/         the unpacked uv release
			python/     the Python builds uv installs
			bin/        the links uv makes to them
			cache/      uv's cache
			tools/      uv's tool folder
			tmp/        the temporary folder of uv's own process
			downloads/  what an online run fetched: the uv archive and its `.sha256`, and uv's Python archive in `python/`

		On standard output it prints the Python it made, one line, for a caller to use. Everything else is said on
		standard error: what it installed, and where each thing is.

		It is safe to run again: what stands at the wanted version is left as it is, nothing is fetched, and it prints the
		same Python. A host with no internet takes the `downloads` folder of a run made elsewhere with the same operating
		system and processor, copied, as `--from-folder`.

##  Examples:

		# Install the pinned uv and Python into this workspace's .local
		`DistroLocalTools.fn.sh --install-embedded-python`

		# Install another uv release
		`DistroLocalTools.fn.sh --install-embedded-python --uv-version 0.12.9`

		# Install on a host with no internet, from the downloads folder of a run made elsewhere, copied here
		`DistroLocalTools.fn.sh --install-embedded-python --from-folder /path/to/downloads`

		# Print this manual
		`DistroLocalTools.fn.sh --install-embedded-python --help`
