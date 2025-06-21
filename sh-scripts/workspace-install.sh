#!/usr/bin/env sh
set -euo pipefail

###############################################################################
#
# This is 'boot' standalone installer script, that allows to bootstrap and install
# any myx.distro workspace project and setup the base system and utilities.
#
# Supported flags:
#   --web-fetch				Download GitHub ZIP & unpack (default)
#   --git-clone				Clone via git
#   --force					Always re-bootstrap even if already present
#   --config-stdin			Read workspace config from stdin
#   --config-file <file>	Use workspace config file specified
#
# Usage:
#   TGT_APP_PATH=…/workspace ./workspace-install.sh [--git-clone|--web-fetch] [--force]
#
# You need to provide workspace config to stdin or as a file path on local filesystem.
# workspace-config is a text file with columns, containing directives for installer.
# First column is i{source|remote|deploy|system|.local} and identifies the system and 
# other columns are system-specific directives that installer translates to set of commands,
# installs systems mentioned and then feeds these commands to each respective system's console.
#
# Example of workspace config:
#
#	# Workspace config for: myx/util.workspace-myx.devops
#
#	# Repository roots for source projects:
#	source root lib
#	source root myx
#
#	# Initial list of source projects to pull
#	source pull myx/util.workspace-myx.devops:main:git@github.com:myx/util.workspace-myx.devops.git
#
#	# Executable commands to setup source sub-system
#	source exec Source DistroSourceTools --system-config-option --upsert-if MDLT_CONSOLE_ORIGIN source ""
#	source exec Source DistroImageSync --all-tasks --execute-source-prepare-pull
#
###############################################################################

: "${TGT_APP_PATH:?⛔ ERROR: TGT_APP_PATH env must be set}"

# ─── 1) PARSE FLAGS ──────────────────────────────────────────────────────────
BOOT_METHOD=--web-fetch
BOOT_UPDATE=0
BOOT_CONFIG=
while [ $# -gt 0 ]; do
  case "$1" in
	--web-fetch|--git-clone)
		BOOT_METHOD=$1; shift ;;
	--force)
		BOOT_UPDATE=1; shift ;;
	--config-stdin)
		BOOT_CONFIG= ; shift ;;
	--config-file)
		[ $# -lt 2 ] && { echo "⛔ ERROR: workspace-install: $1 needs argument" >&2; exit 1; }
		BOOT_CONFIG=$2 ; shift ; shift ;;
	*)
		echo "⛔ ERROR: workspace-install: invalid option: $1" >&2
		exit 1
  esac
done

# ─── 2) NORMALIZE WORKSPACE ROOT ─────────────────────────────────────────────
MMDAPP="$TGT_APP_PATH"

# expand ‘~’
case "$MMDAPP" in
  "~"*) MMDAPP="$HOME${MMDAPP#\~}" ;;
esac

# make absolute
case "$MMDAPP" in
  /*) ;; 
  *)  MMDAPP="$PWD/$MMDAPP" ;;
esac

export MMDAPP
mkdir -p "$MMDAPP"
cd "$MMDAPP"
echo "$0: Workspace root: $PWD" >&2

# ─── 3) VALIDATE TOOLS FOR CHOSEN BOOT_METHOD ────────────────────────────────
case "$BOOT_METHOD" in

  --git-clone)
	if ! command -v git >/dev/null 2>&1; then
	  echo "⛔ ERROR: workspace-install: git is required for --git-clone" >&2
	  exit 1
	fi
	;;

  --web-fetch)
	# downloader
	if   command -v curl >/dev/null 2>&1; then
		DLOAD_CMD() { curl -fsSL -o "$1" "$2"; }
	elif command -v wget >/dev/null 2>&1; then
		DLOAD_CMD() { wget -q -O "$1" "$2"; }
	elif command -v fetch >/dev/null 2>&1; then
		DLOAD_CMD() { fetch -q -o "$1" "$2"; }
	else
		echo "⛔ ERROR: workspace-install: need curl, wget or fetch" >&2; 
		exit 1
	fi

	# unzipper
	if   command -v unzip  >/dev/null 2>&1; then
	  UNZIP_CMD() { unzip -q "$1" -d "$2"; }
	elif command -v bsdtar >/dev/null 2>&1; then
	  UNZIP_CMD() { bsdtar -C "$2" -x -f "$1"; }
	else
	  echo "⛔ ERROR: workspace-install: need unzip or bsdtar for --web-fetch" >&2
	  exit 1
	fi

	# rsync (we'll use it to sync the fetched archive)
	if ! command -v rsync >/dev/null 2>&1; then
	  echo "⛔ ERROR: workspace-install: rsync is required for --web-fetch" >&2
	  exit 1
	fi
	;;

  *)
	echo "⛔ ERROR: workspace-install: unsupported boot mode: $BOOT_METHOD" >&2
	exit 1
	;;
esac

# ─── 4) CONDITIONAL BOOTSTRAP ────────────────────────────────────────────────
LOCAL_BASE="$MMDAPP/.local/myx"
DISTRO_DIR="$LOCAL_BASE/myx.distro-.local"

if [ "$BOOT_UPDATE" -eq 1 ] || [ ! -d "$LOCAL_BASE" ] || [ ! -f "$DISTRO_DIR/sh-scripts/workspace-install.sh" ] ; then
  echo "📜 workspace-install: → Bootstrapping distro-.local via $BOOT_METHOD" >&2
  mkdir -p "$LOCAL_BASE"

  case "$BOOT_METHOD" in

	--git-clone)
		# mkdir -p ".local/myx" ; ( cd ".local/myx" ; rm -rf "myx.distro-.local" ; git clone git@github.com:myx/myx.distro-.local.git )

		if [ -d "$DISTRO_DIR" ]; then
			echo "🌏 workspace-install: • updating existing clone…" >&2
			git -C "$DISTRO_DIR" fetch --depth=1 origin main \
				&& git -C "$DISTRO_DIR" reset --hard FETCH_HEAD
		else
			echo "🌏 workspace-install: • git clone…" >&2
			git clone --depth=1 \
				https://github.com/myx/myx.distro-.local.git \
				"$DISTRO_DIR" >&2
		fi
	  ;;

	--web-fetch)
		# running in subshell to cleanup it's temp upon arm exit
		(
			TMPBASE="${TMPDIR:-$MMDAPP/.local/tmp}/boot-web-fetch.XXXXXXXXXX"

			# created, used and deleted within this arm only
			WORKTMP=$(mktemp -d "$TMPBASE")
			trap 'rm -rf "$WORKTMP"' EXIT INT TERM

			echo "🌏 workspace-install: • downloading ZIP…" >&2
			DLOAD_CMD "$WORKTMP/boot.zip" "https://github.com/myx/myx.distro-.local/archive/refs/heads/main.zip"

			echo "🗂️ workspace-install: • unpacking ZIP…" >&2
			UNZIP_CMD "$WORKTMP/boot.zip" "$WORKTMP"

			# find the extracted folder (GitHub names it myx.distro-.local-main)
			SRC_DIR=$(find "$WORKTMP" -maxdepth 1 -type d -name 'myx.distro-.local-*' | head -1)

			echo "🔂 workspace-install: • syncing files to $DISTRO_DIR" >&2
			rsync -a --delete "$SRC_DIR"/ "$DISTRO_DIR"/
		)
	  ;;

  esac
fi


# ─── LOAD WORKSPACE CONFIG ────────────────────────────────────────────────────

# supports both: stdin and file specification
CONFIG_CONTENT=$(
  # 1) drop blank lines & comments  
  grep -E -v '^[[:space:]]*($|#)' "$BOOT_CONFIG" |
  # 2) trim leading/trailing space, squeeze inner spaces to one  
  sed \
    -e 's/^[[:space:]]*//' \
    -e 's/[[:space:]]*$//' \
    -e 's/[[:space:]]\{1,\}/ /g' |
  # 3) only keep lines with ≥3 fields (i.e. two spaces)  
  grep -E '^([^[:space:]]+ +){2}.*'
)

# ─── DETECT & INSTALL NEEDED SYSTEMS ─────────────────────────────────────────
INSTALL_SYSTEMS=
for sys in $(printf '%s\n' "$CONFIG_CONTENT" \
             | awk '$1!~/^#/ && NF {print $1}' \
             | sort -u); do
  # if --force OR the target sub‐directory doesn’t exist
  if [ "$BOOT_UPDATE" -eq 1 ] || [ ! -d "$sys" ]; then
    INSTALL_SYSTEMS="$INSTALL_SYSTEMS --install-distro-$sys"
  fi
done

if [ -n "$INSTALL_SYSTEMS" ]; then
  echo "🛠️ workspace-install: DistroLocalTools.fn.sh $INSTALL_SYSTEMS" >&2
  bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh $INSTALL_SYSTEMS
fi

## 6 - do 'source' commands
{
	ROOT_LIST=$( echo $(
		printf '%s\n' "$CONFIG_CONTENT" \
		| awk '/^source[[:space:]]+root[[:space:]]/ { print $3 }' \
		| tr '\n' ' '
	) )

	# split third field on first two “:”, keeping “url” intact
	REPO_LIST=$(
		printf '%s\n' "$CONFIG_CONTENT" \
		| awk '/^source[[:space:]]+pull[[:space:]]/ { print $3 }' \
		| sed -E 's#([^:]+):([^:]+):(.*)#\1\t\3\t\2#' \
		| awk '!x[$0]++'
	) 

	EXEC_CMDS=$(
		printf '%s\n' "$CONFIG_CONTENT" \
		| sed -n -E 's/^source[[:space:]]+exec[[:space:]]+(.+)/\1/p'
	#	| sed -n -E 's/^source[[:space:]]+exec[[:space:]]+(.+)/Source \1/p'
	)

	# printf "%s\n\n%s\n\n%s\n\n" "$ROOT_LIST" "$REPO_LIST" "$EXEC_CMDS"

	if [ -n "$ROOT_LIST$REPO_LIST$EXEC_CMDS" ]; then
		sed -e 's/^[[:space:]]*//' -e '/^#/d' -e '/^$/d' \
			| ./DistroSourceConsole.sh --non-interactive --verbose <<EOF

		set -e

		if [ -n "$ROOT_LIST" ] ; then
			echo "📝 workspace-install: Register repository roots ($ROOT_LIST)..."
			Source DistroSourceTools --register-repository-roots $ROOT_LIST
		fi

		if [ -n "$REPO_LIST" ] ; then
			echo "⬇️ workspace-install: Pull workspace-initial git repositories..." >&2
			printf "%s\n" "$REPO_LIST" | Source DistroImageSync --execute-from-stdin-repo-list
		fi

		if [ -n "$EXEC_CMDS" ] ; then
			echo "🖥️ workspace-install: Running extra commands..." >&2
			$EXEC_CMDS
		fi

		echo "SourceInstall: All Source Console tasks done." >&2

EOF
	fi
}
