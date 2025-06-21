#!/usr/bin/env sh
set -euo pipefail

###############################################################################
#
# This is 'boot' standaline installer script, that allows to bootstrap and install
# any myx.distro workspace project and setup the base system and utilities.
#
# Supported flags:
#   --web-fetch           Download GitHub ZIP & unpack (default)
#   --git-clone           Clone via git
#   --force               Always re-bootstrap even if already present
#   --config-stdin        Read workspace config from stdin
#   --config-file <file>  Use workspace config file specified
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
BOOT_METHOD=web-fetch
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
		: "${2:?⛔ ERROR: $1 argument requires file-path argument to follow!}"
		BOOT_CONFIG=$2 ; shift ; shift ;;
    *)
		echo "⛔ ERROR: workspace-install: invalid option: $1" >&2
		set +e ; return 1
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

  git-clone)
    if ! command -v git >/dev/null 2>&1; then
      echo "ERROR: git is required for --git-clone" >&2
      exit 1
    fi
    ;;

  web-fetch)
    # downloader
    if   command -v curl >/dev/null 2>&1; then
      DLOAD_CMD() { curl -fsSL "$1"; }
    elif command -v wget >/dev/null 2>&1; then
      DLOAD_CMD() { wget -q -O - "$1"; }
    elif command -v fetch >/dev/null 2>&1; then
      DLOAD_CMD() { fetch -q -o - "$1"; }
    else
      echo "ERROR: need curl, wget or fetch for --web-fetch" >&2
      exit 1
    fi

    # unzipper
    if   command -v unzip  >/dev/null 2>&1; then
      UNZIP_CMD() { unzip -q "$1" -d "$2"; }
    elif command -v bsdtar >/dev/null 2>&1; then
      UNZIP_CMD() { bsdtar -C "$2" -x -f "$1"; }
    else
      echo "ERROR: need unzip or bsdtar for --web-fetch" >&2
      exit 1
    fi

    # rsync (we'll use it to sync the fetched archive)
    if ! command -v rsync >/dev/null 2>&1; then
      echo "ERROR: rsync is required for --web-fetch" >&2
      exit 1
    fi
    ;;

  *)
    echo "ERROR: unsupported boot mode: $BOOT_METHOD" >&2
    exit 1
    ;;
esac

# ─── 4) CONDITIONAL BOOTSTRAP ────────────────────────────────────────────────
LOCAL_BASE="$MMDAPP/.local/myx"
DISTRO_DIR="$LOCAL_BASE/myx.distro-system"

if [ "$BOOT_UPDATE" -eq 1 ] || [ ! -d "$LOCAL_BASE" ]; then
  echo "→ Bootstrapping distro-system via $BOOT_METHOD…" >&2
  mkdir -p "$LOCAL_BASE"

  case "$BOOT_METHOD" in

    git-clone)
		if [ -d "$DISTRO_DIR" ]; then
			echo "  • updating existing clone…" >&2
			git -C "$DISTRO_DIR" fetch --depth=1 origin main \
				&& git -C "$DISTRO_DIR" reset --hard FETCH_HEAD
		else
			echo "  • git clone…" >&2
			git clone --depth=1 \
				https://github.com/myx/myx.distro-system.git \
				"$DISTRO_DIR" >&2
		fi
      ;;

    web-fetch)
      echo "  • setting up temporary directory" >&2
      TMPBASE="${TMPDIR:-$MMDAPP/.local/tmp}/boot-web-fetch.XXXXXXXXXX"
      WORKTMP=$(mktemp -d "$TMPBASE")
      trap 'rm -rf "$WORKTMP"' EXIT INT TERM

      echo "  • downloading & unpacking ZIP…" >&2
      DLOAD_CMD https://github.com/myx/myx.distro-system/archive/refs/heads/main.zip \
	  | UNZIP_CMD "$WORKTMP"

      # find the extracted folder (GitHub names it myx.distro-system-main)
      SRC_DIR=$(find "$WORKTMP" -maxdepth 1 -type d -name 'myx.distro-system-*' | head -1)

      echo "  • syncing files to $DISTRO_DIR…" >&2
      rsync -a --delete "$SRC_DIR"/ "$DISTRO_DIR"/
      ;;

  esac
fi

# ─── 5) NEXT STEPS: parse workspace config file and feed the script via ./DistroLocalConsole.sh ───────
