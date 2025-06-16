#!/usr/bin/env bash

##
## NOTE:
## Designed to be able to run without distro context. Used to install required parts.
##



##
## To make this script self-sufficient, this copied from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/git/clonePull`
##
GitClonePull(){
	set -e

	if [ -x "$MDLT_ORIGIN/myx/myx.common/os-myx.common/host/share/myx.common/bin/git/clonePull" ] ; then 
		echo "😻 GitClonePull: executable found!" >&2
		"$MDLT_ORIGIN/myx/myx.common/os-myx.common/host/share/myx.common/bin/git/clonePull" "$@"
		return 0
	fi

	: "${1:?⛔ ERROR: GitClonePull: tgtPath is required!}"
	: "${2:?⛔ ERROR: GitClonePull: repoUrl is required!}"
	local tgtPath="$1" repoUrl="$2"

	local specificBranch="$3"
	
	local currentPath="$PWD"
	
	if [ -d "$tgtPath" ] && [ -d "$tgtPath/.git" ] ; then
		cd "$tgtPath"
		if git rev-parse --abbrev-ref HEAD > /dev/null ; then
			local clonedBranch="`git rev-parse --abbrev-ref HEAD`"
			if [ "$clonedBranch" != "${specificBranch:-master}" ] && [ "$clonedBranch" != "${specificBranch:-main}" ] ; then
				echo "GitClonePull: Switch branches: $clonedBranch -> ${specificBranch:-master}..." >&2
				cd "$tgtPath/.."
				rm -rf "$tgtPath"
			fi
		fi
		cd "$currentPath"
	fi
	if [ ! -d "$tgtPath" ] || [ ! -d "$tgtPath/.git" ] ; then
	    echo "GitClonePull: $tgtPath: creating..." >&2
	    mkdir -p "$tgtPath"
		local GIT_BRANCH_OPT=""
		if [ -n "$specificBranch" ] ; then
			local GIT_BRANCH_OPT="--single-branch --branch $specificBranch"
		fi
		if ! git clone $GIT_BRANCH_OPT "$repoUrl" "$tgtPath" ; then
		    rm -rf "$tgtPath"
		    return 1
		fi
		cd "$currentPath"
	else
		if [ -d "$tgtPath" ] ; then
			cd "$tgtPath"
			echo "GitClonePull: $tgtPath: updating..." >&2
			git remote set-url origin "$repoUrl"
			if [ -n "$specificBranch" ] ; then
				git checkout $specificBranch
			fi
			git pull --ff-only
			cd "$currentPath"
		fi
	fi
	if [ ! -d "$tgtPath" ] || [ ! -d "$tgtPath/.git" ] ; then
		echo "⛔ ERROR: GitClonePull: error checking out!" >&2 && return 1
	fi

	echo "GitClonePull: $tgtPath: finished." >&2
}


# this part supposed to install, import or update the workspace on possible non-prepared machine
case "$1" in
	--install-workspace-from-stdin-config)
		: "${TGT_APP_PATH:?⛔ ERROR: TGT_APP_PATH env must be set}"
		MMDAPP=$TGT_APP_PATH
		case $MMDAPP in
			"~"*) MMDAPP=$HOME${MMDAPP#\~} ;;
		esac
		case $MMDAPP in
			/*) ;;
			*)  MMDAPP=$PWD/$MMDAPP ;;
		esac
			
		export MMDAPP ; mkdir -p "$MMDAPP" ; cd "$MMDAPP"
		echo "$0: Workspace root: $PWD" >&2
		
		if [ ! -d ".local/myx" ] ; then
			echo "Install: .local system, pulling system packages..." >&2
			mkdir -p ".local/myx" ; ( cd ".local/myx" ; rm -rf "myx.distro-.local" ; git clone git@github.com:myx/myx.distro-.local.git )
		fi

		echo "Install: DistroLocalTools.fn.sh --stdin-workspace-config-parse..." >&2
		cat | bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --stdin-workspace-config-parse

		echo "Install: DistroLocalTools.fn.sh done" >&2
		exit 0
	;;
esac

if [ -z "$MMDAPP" ] ; then
	set -e
	export MMDAPP="$( cd $(dirname "$0")/../../../.. ; pwd )"
	echo "$0: Working in: $MMDAPP"  >&2
	[ -d "$MMDAPP/.local" ] || ( echo "⛔ ERROR: expecting '.local' directory." >&2 && exit 1 )
fi

: "${MDLT_ORIGIN:=$MMDAPP/.local}"
export MDLT_ORIGIN


##
## To make this script self-sufficient, this copied IN SIMPLIFIED FORM from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/lib/prefix`
##
Prefix(){
	local PREFTEXT="$1"
	shift

	PREFTEXT="$( printf %s "$PREFTEXT" | tr '^' '-' | tr -d '\n' )"
	
	set -e

    ( "$@" 2>&1 \
    		|| ( EXITCODE=$? ; set +x ; echo "⛔ ERROR: exited with error status ($EXITCODE)" ; exit $EXITCODE ) \
   	) | sed -l -e "s^\^^$PREFTEXT: ^" 1>&2
   	
}
DistroLocalTools(){
	local MDSC_CMD='DistroLocalTools'
	[ -z "$MDSC_DETAIL" ] || echo "> $MDSC_CMD $@" >&2

	set -e

	case "$1" in
		--make-*)
			. "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/LocalTools.Make.include"
			return 0
		;;
		--*-config-option|--*-config-option)
			. "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/LocalTools.Config.include"
			return 0
		;;
		--help-install-unix-bare)
			. "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/LocalTools.CatMarkdown.include"
			DistroLocalCatMarkdown "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/Help.DistroLocalTools-install-unix-bare.md" >&2
			exit 1;
		;;
		''|--help)
			echo "syntax: DistroLocalTools.fn.sh <option>" >&2
			echo "syntax: DistroLocalTools.fn.sh [--help]" >&2
			if [ "$1" = "--help" ] ; then
				cat "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/Help.DistroLocalTools.text" >&2
			fi
			set +e ; return 1
		;;
		--init-distro-workspace)
			shift

			return 0
		;;
		--stdin-workspace-config-parse)
			shift
			cat
			return 0
			local cmds
			cmds+="$(
				echo ': "${TGT_APP_PATH:?⛔ ERROR: TGT_APP_PATH env must be set}"'
				echo 'MMDAPP=$TGT_APP_PATH'
				echo 'case $MMDAPP in'
  				echo '"~"*) MMDAPP=$HOME${MMDAPP#\~} ;;'
				echo 'esac'
				echo 'case $MMDAPP in'
				echo '  /*) ;;'
				echo '  *)  MMDAPP=$PWD/$MMDAPP ;;'
				echo 'esac'
				echo 
				echo 'export MMDAPP ; mkdir -p "$MMDAPP" ; cd "$MMDAPP"'
				echo 'echo "$0: Workspace root: $PWD" >&2'
				echo 
				echo 'if [ ! -d ".local/myx" ] ; then'
				echo '	echo "Install: .local system, pulling system packages..." >&2'
				echo '	mkdir -p ".local/myx" ; ( cd ".local/myx" ; rm -rf "myx.distro-.local" ; git clone git@github.com:myx/myx.distro-.local.git )'
				echo 'fi'
				echo 'cat | '
			)"

		;;
		--install-distro-*)
			# update '.local' when running scripts from locally editable 'source'
			[ "$MDLC_INMODE" != "source" ] || local MDLT_ORIGIN="$MMDAPP/.local"
			local cmds
			cmds+="$(
				echo
				echo 'set -e'
				echo "export MMDAPP='$MMDAPP'"
				echo "export MDLT_ORIGIN='${MDLT_ORIGIN:-$MMDAPP/.local}'"
				echo
				echo 'set +e # for pulls (when no changes)'
				echo 'Prefix "os-myx.common" GitClonePull "$MDLT_ORIGIN/myx/myx.common/os-myx.common" "git@github.com:myx/os-myx.common.git" &'
				echo 'Prefix "distro-.local" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &'
				echo 'touch "$MMDAPP/.local/MDLT.settings.env" # make sure workspace env file exists'
			)"

			while true ; do
				case "$1" in
					--install-distro-remote)
						shift
						cmds+="$(
							echo
							echo 'Prefix "distro-remote" GitClonePull "$MMDAPP/.local/myx/myx.distro-remote/" "git@github.com:myx/myx.distro-remote.git" &'
							echo 'mkdir -p "$MMDAPP/remote" # make sure `remote` directory exists'
						)"
					;;
					--install-distro-deploy)
						shift
						cmds+="$(
							echo
							echo 'Prefix "distro-system" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-system/" "git@github.com:myx/myx.distro-system.git" &'
							echo 'Prefix "distro-deploy" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-deploy/" "git@github.com:myx/myx.distro-deploy.git" &'
							echo 'mkdir -p "$MMDAPP/distro" # make sure `distro` directory exists'
						)"
					;;
					--install-distro-source)
						shift
						cmds+="$(
							echo
							echo 'Prefix "distro-system" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-system/" "git@github.com:myx/myx.distro-system.git" &'
							echo 'Prefix "distro-source" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-source/" "git@github.com:myx/myx.distro-source.git" &'
							echo 'mkdir -p "$MMDAPP/source" # make sure `source` directory exists'
						)"
					;;
					--install-distro-.local)
						shift
						cmds+="$(
							echo
							echo 'mkdir -p "$MMDAPP/.local" # make sure .local directory exists'
						)"
					;;
					'')
						if [ -z "$cmds" ] ; then
							echo "⛔ ERROR: $MDSC_CMD: nothing to install, check arguments" >&2
							set +e ; return 1
						fi
						cmds+="$(
							echo
							echo 'set -e # after pulls'
							echo
							echo 'wait # wait for all the subprocesses to finish'
							echo
							echo 'DistroLocalTools --make-workspace-integration-files'
						)"
						break
					;;
					*)
						echo "⛔ ERROR: $MDSC_CMD: invalid option: $1" >&2
						set +e ; return 1
					;;
				esac
			done

			cmds="$( echo "$cmds" | awk '!$0 || !seen[$0]++' )"

			printf "\n$MDSC_CMD: Will execute: \n%s\n\n" "$( echo "$cmds" | sed 's|^|    |' )" >&2

			( eval "$cmds" )

			return 0
		;;
		*)
			echo "⛔ ERROR: $MDSC_CMD: invalid option: $1" >&2
			set +e ; return 1
		;;
	esac
}

case "$0" in
	*/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh)

		if [ -z "$1" ] || [ "$1" = "--help" ] ; then
			if [ -z "$1" ] || [ ! -f "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/Help.DistroLocalTools.text" ] ; then
				echo "syntax: DistroLocalTools.fn.sh --install-distro-source" >&2
				echo "syntax: DistroLocalTools.fn.sh --install-distro-deploy" >&2
				echo "syntax: DistroLocalTools.fn.sh --install-distro-remote" >&2
			else
				cat "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/Help.DistroLocalTools.text" >&2
				set +e ; return 1
			fi
		fi

		set -e
		DistroLocalTools "$@"
	;;
esac
