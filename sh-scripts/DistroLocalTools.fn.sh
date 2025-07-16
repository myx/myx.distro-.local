#!/usr/bin/env bash

##
## NOTE:
## Designed to be able to run without distro context. Used to install required parts.
##


if [ -z "$MMDAPP" ] ; then
	set -e
	export MMDAPP="$( cd $(dirname "$0")/../../../.. ; pwd )"
	echo "$0: Working in: $MMDAPP" >&2
	[ -d "$MMDAPP/.local" ] || ( echo "⛔ ERROR: expecting '.local' directory." >&2 && exit 1 )
fi

: "${MDLT_ORIGIN:=$MMDAPP/.local}"
export MDLT_ORIGIN

if   [ -d "$MYXROOT" ] && [ -f "$MYXROOT/share/myx.common/bin/lib/catMarkdown.Common" ]; then
	export MYXROOT
elif   [ -f "$MDLT_ORIGIN/myx/myx.common/os-myx.common/host/tarball/share/myx.common/bin/lib/catMarkdown.Common" ]; then
	export MYXROOT="$MDLT_ORIGIN/myx/myx.common/os-myx.common/host/tarball/share/myx.common"
elif [ -f "/usr/local/share/myx.common/bin/lib/catMarkdown.Common" ]; then
	export MYXROOT="/usr/local/share/myx.common"
elif command -v myx.common 2>/dev/null && myx.common which lib/catMarkdown 2>/dev/null ; then
	export MYXROOT="$( myx.common which lib/catMarkdown | sed -e 's|/bin/lib/catMarkdown.*$||' )"
else
	export MYXROOT=''
fi

[ -n "${MYXUNIX-}" ] || export MYXUNIX="$(uname -s)"

##
## To make this script self-sufficient, this copied from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/git/clonePull.Common`
##
[ -f "$MYXROOT/bin/git/clonePull.Common" ] && . "$MYXROOT/bin/git/clonePull.Common" || GitClonePull(){
	set -e

	if [ -x "$MYXROOT/bin/git/clonePull.Common" ] ; then 
		echo "😻 GitClonePull: executable found!" >&2
		"$MYXROOT/bin/git/clonePull.Common" "$@"
		return 0
	fi

	echo "-- using embedded function"

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


##
## To make this script self-sufficient, this copied IN SIMPLIFIED FORM from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/lib/prefix.Common`
##
[ -f "$MYXROOT/bin/lib/prefix.Common" ] && . "$MYXROOT/bin/lib/prefix.Common" || Prefix(){
	set -e

	if [ -x "$MYXROOT/bin/lib/prefix.Common" ] ; then 
		echo "😻 Prefix: executable found!" >&2
		"$MYXROOT/bin/lib/prefix.Common" "$@"
		return 0
	fi

	echo "-- using embedded function"

	local PREFTEXT="$1"
	shift

	PREFTEXT="$( printf %s "$PREFTEXT" | tr '^' '-' | tr -d '\n' )"

    ( "$@" 2>&1 \
    		|| ( EXITCODE=$? ; set +x ; echo "⛔ ERROR: exited with error status ($EXITCODE)" ; exit $EXITCODE ) \
   	) | sed -l -e "s^\^^$PREFTEXT: ^" 1>&2
   	
}

##
## To make this script self-sufficient, this copied from:
## `myx/myx.common/os-myx.common/host/share/myx.common/bin/lib/catMarkdown.Common`
##
[ -f "$MYXROOT/bin/lib/catMarkdown.Common" ] && . "$MYXROOT/bin/lib/catMarkdown.Common" || CatMarkdown() {
	set -e

	if [ -x "$MYXROOT/bin/lib/catMarkdown.Common" ] ; then 
		echo "😻 CatMarkdown: executable found!" >&2
		"$MYXROOT/bin/lib/catMarkdown.Common" "$@"
		return 0
	fi

	echo "-- using embedded function"

	local fromFile="$1"
	if [ -n "$fromFile" ] ; then
		if [ ! -f "$fromFile" ] ; then
			echo "⛔ ERROR: CatMarkdown: file not found: $fromFile" >&2
			set +e ; return 1
		fi
		shift
		cat "$fromFile" | CatMarkdown
		return 0
	fi

	# detect “real” TTY
	if     [ -t 1 ] \
		&& [ -z "${NO_COLOR-}" ] \
		&& [ -n "${TERM-}" ] && [ "$TERM" != dumb ] \
		&& tput colors >/dev/null 2>&1 \
		&& [ "$(tput colors)" -ge 8 ] \
	; then
		USE_COLOR=1
	fi

	if [ "${USE_COLOR-}" ]; then
		# ANSI codes
		esc=$(printf '\033')
		reset="${esc}[0m"
		bold_on="${esc}[1m"   bold_off="${esc}[22m"
		ital_on="${esc}[3m"   ital_off="${esc}[23m"
		code_on="${esc}[96m"  code_off="${reset}"
		quote_on="${esc}[90m" quote_off="${reset}"
		bullet_on="${esc}[32m" bullet_off="${reset}"
		hdr1_on="${esc}[95m"  hdr2_on="${esc}[94m"  hdr3_on="${esc}[92m"
		hdr_off="${reset}"

		sed -E \
		-e "s/^###### (.*)/${hdr1_on}\1${hdr_off}/" \
		-e "s/^##### (.*)/${hdr1_on}\1${hdr_off}/" \
		-e "s/^#### (.*)/${hdr2_on}\1${hdr_off}/" \
		-e "s/^### (.*)/${hdr2_on}\1${hdr_off}/" \
		-e "s/^## (.*)/${hdr3_on}\1${hdr_off}/" \
		-e "s/^# (.*)/${hdr3_on}\1${hdr_off}/" \
		-e "s/^([[:space:]]*)> +(.*)/\1${quote_on}> ${quote_off}\2/" \
		-e "s/^([[:space:]]*)([0-9]+)\. +(.*)/\1${bullet_on}○ ${bullet_off}\3/" \
		-e "s/^([[:space:]]*)[-*] +(.*)/\1${bullet_on}• ${bullet_off}\2/" \
		-e "s/\*\*([^*]+)\*\*/${bold_on}\1${bold_off}/g" \
		-e "s/_([^_]+)_/${ital_on}\1${ital_off}/g" \
		-e "s/\`([^\`]+)\`/${code_on}\1${code_off}/g" \
		-e '/^[[:space:]]*\|?[-:]+(\|[-:]+)+\|?[[:space:]]*$/d'
	else
		sed -E \
		-e 's/^#{1,6} //g' \
		-e 's/^([[:space:]]*)> +(.*)/\1\2/' \
		-e 's/^([[:space:]]*)([0-9]+)\. +(.*)/\1- \3/' \
		-e 's/^([[:space:]]*)[-*] +(.*)/\1- \2/' \
		-e 's/\*\*([^*]+)\*\*/\1/g' \
		-e 's/_([^_]+)_/\1/g' \
		-e 's/\`([^`]+)\`/\1/g' \
		-e '/^[[:space:]]*\|?[-:]+(\|[-:]+)+\|?[[:space:]]*$/d'
	fi | column -s '|' -t
}


##
##
##		DistroLocalTools
##
##
DistroLocalTools(){
	local MDSC_CMD='DistroLocalTools'
	[ -z "$MDSC_DETAIL" ] || echo "> $MDSC_CMD" $MDSC_NO_CACHE $MDSC_NO_INDEX "$@" >&2

	set -e

	while true ; do
		case "$1" in
			--make-*)
				. "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/LocalTools.Make.include"
				return 0
			;;
			--*-config-option|--*-config-option)
				. "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/LocalTools.Config.include"
				return 0
			;;
			--init-distro-workspace)
				shift

				return 0
			;;
			--install-distro-*)
				# update '.local' when running scripts from locally editable 'source'
				[ "$MDLC_INMODE" != "source" ] || local MDLT_ORIGIN="$MMDAPP/.local"
				local cmds
				cmds+="$(
					# echo '. "$( myx.common which lib/prefix )"'' ## included statically above
					# echo '. "$( myx.common which git/clonePull )"'' ## included statically above
					echo
					echo 'set -e'
					echo "export MMDAPP='$MMDAPP'"
					echo "export MDLT_ORIGIN='${MDLT_ORIGIN:-$MMDAPP/.local}'"
					echo
					echo 'set +e # for pulls (when no changes)'
					echo 'Prefix "os-myx.common" GitClonePull "$MDLT_ORIGIN/myx/myx.common/os-myx.common" "git@github.com:myx/os-myx.common.git" &'
					echo 'Prefix "distro-.local" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-.local/" "git@github.com:myx/myx.distro-.local.git" &'
					echo 'set -e'
					echo
					echo 'touch "$MMDAPP/.local/MDLT.settings.env" # make sure workspace env file exists'
					echo 'export MYXROOT="$MDLT_ORIGIN/myx/myx.common/os-myx.common/host/tarball/share/myx.common"'
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
								echo 'touch "$MMDAPP/.local/MDSC.deploy.settings.env" # make sure workspace deploy env file exists'
							)"
						;;
						--install-distro-source)
							shift
							cmds+="$(
								echo
								echo 'Prefix "distro-system" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-system/" "git@github.com:myx/myx.distro-system.git" &'
								echo 'Prefix "distro-source" GitClonePull "$MDLT_ORIGIN/myx/myx.distro-source/" "git@github.com:myx/myx.distro-source.git" &'
								echo 'mkdir -p "$MMDAPP/source" # make sure `source` directory exists'
								echo 'touch "$MMDAPP/.local/MDSC.source.settings.env" # make sure workspace deploy env file exists'
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
			--upgrade-installed-tools)
				shift
				DistroLocalTools $(
					for ITEM in "deploy" "source" "remote" ; do
						[ -d "$MDLT_ORIGIN/myx/myx.distro-$ITEM/sh-scripts" ] || continue
						echo --install-distro-$ITEM
					done
				)
				DistroLocalTools --make-workspace-integration-files
				return 0
			;;
			--help-install-unix-bare)
				(
					# . "$( myx.common which lib/catMarkdown )" ## included statically above
					CatMarkdown "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/help/Help.DistroLocalTools-install-unix-bare.md" >&2
				)
				return 0
			;;
			--help|--help-syntax)
				echo "📘 syntax: DistroLocalTools.fn.sh --upgrade-local-tools" >&2
				echo "📘 syntax: DistroLocalTools.fn.sh <option>" >&2
				echo "📘 syntax: DistroLocalTools.fn.sh [--help]" >&2
				if [ "$1" = "--help" ] ; then
					cat "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/help/Help.DistroLocalTools.text" >&2
				fi
				return 0
			;;
			--verbose)
				shift
				export MDSC_DETAIL="true"
				continue
			;;
			*)
				echo "⛔ ERROR: $MDSC_CMD: invalid option: $1" >&2
				set +e ; return 1
			;;
		esac
	done
}

case "$0" in
	*/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh)

		if [ -z "$1" ] || [ "$1" = "--help" ] ; then
			if [ -z "$1" ] || [ ! -f "$MDLT_ORIGIN/myx/myx.distro-.local/sh-lib/help/Help.DistroLocalTools.text" ] ; then
				echo "📘 syntax: DistroLocalTools.fn.sh --install-distro-source" >&2
				echo "📘 syntax: DistroLocalTools.fn.sh --install-distro-deploy" >&2
				echo "📘 syntax: DistroLocalTools.fn.sh --install-distro-remote" >&2
			else
				DistroLocalTools "${1:-"--help-syntax"}"
			fi
			exit 1
		fi

		set -e
		DistroLocalTools "$@"
	;;
esac
