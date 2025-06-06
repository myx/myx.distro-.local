#!/usr/bin/env bash

##
## NOTE:
## Designed to be able to run without distro context. Used to install required parts.
##

if [ -z "$MMDAPP" ] ; then
	set -e
	export MMDAPP="$( cd $(dirname "$0")/../../../.. ; pwd )"
	echo "$0: Working in: $MMDAPP"  >&2
	[ -d "$MMDAPP/.local" ] || ( echo "ERROR: expecting '.local' directory." >&2 && exit 1 )
fi

##
## To make this script self-sufficient, this copied from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/git/clonePull`
##
GitClonePull(){
	set -e

	local tgtPath="$1"
	[ -z "$tgtPath" ] && echo "ERROR: GitClonePull: tgtPath is required!" >&2 && return 1

	local repoUrl="$2"
	[ -z "$repoUrl" ] && echo "ERROR: GitClonePull: repoUrl is required!" >&2 && return 1

	local specificBranch="$3"
	
	local currentPath="`pwd`"
	
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
			git pull
			cd "$currentPath"
		fi
	fi
	if [ ! -d "$tgtPath" ] || [ ! -d "$tgtPath/.git" ] ; then
		echo "ERROR: GitClonePull: error checking out!" >&2 && return 1
	fi

	echo "GitClonePull: $tgtPath: finished." >&2
}


DistroLocalTools(){
	local MDSC_CMD='DistroLocalTools'
	[ -z "$MDSC_DETAIL" ] || echo "> $MDSC_CMD $@" >&2

	set -e

	case "$1" in
		--init-distro-workspace)
			shift

			return 0
		;;
		--install-distro-remote)
			shift

			GitClonePull "$MMDAPP/.local/source/myx/myx.common/" "git@github.com:myx/os-myx.common.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-remote/" "git@github.com:myx/myx.distro-remote.git" &

			wait

			return 0
		;;
		--install-distro-deploy)
			shift

			GitClonePull "$MMDAPP/.local/source/myx/myx.common/" "git@github.com:myx/os-myx.common.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-system/" "git@github.com:myx/myx.distro-system.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-deploy/" "git@github.com:myx/myx.distro-deploy.git" &

			wait

			return 0
		;;
		--install-distro-source)
			shift

			GitClonePull "$MMDAPP/.local/source/myx/myx.common/" "git@github.com:myx/os-myx.common.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-system/" "git@github.com:myx/myx.distro-system.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-source/" "git@github.com:myx/myx.distro-source.git" &

			wait

			return 0
		;;
		--install-distro-.local)
			shift

			GitClonePull "$MMDAPP/.local/source/myx/myx.common/" "git@github.com:myx/os-myx.common.git" &
			GitClonePull "$MMDAPP/.local/source/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &

			wait

			return 0
		;;
		--system-config-option|--custom-config-option)
		;;
		--help-install-unix-bare)
			cat "$MMDAPP/source/myx/myx.distro-.local/sh-lib/HelpDistroLocalTools-unix-bare.text" >&2
			exit 1;
		;;
		*)
			echo "ERROR: $MDSC_CMD: invalid option: $1" >&2
			set +e ; return 1
		;;
	esac
}


case "$0" in
	*/myx/myx.distro-.local/sh-scripts/DistroLocalTools.sh)

		if [ -z "$1" ] || [ "$1" = "--help" ] ; then
			echo "syntax: DistroLocalTools.sh --install-distro-source" >&2
			echo "syntax: DistroLocalTools.sh --install-distro-deploy" >&2
			echo "syntax: DistroLocalTools.sh [--help]" >&2
			if [ "$1" = "--help" ] ; then
				cat "$MMDAPP/source/myx/myx.distro-.local/sh-lib/HelpDistroLocalTools.text" >&2
			fi
			exit 1
		fi
		
		DistroLocalTools "$@"
	;;
esac
