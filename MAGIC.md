# MAGIC.md — myx.distro-.local

Team-owned notes for the magic-* team. This package installs the others, so what a workspace actually exposes is recorded here.

## Families are packages

- A family is a package. The families are source, deploy, remote, system, agents and `.local`. They are separate sets.
- Each installed `myx.distro-*` package contributes its own `sh-scripts/` directory to a console's `PATH`.
- A console's `PATH` is set explicitly by that console's own rc file. Each rc hardcodes its own list; nothing is discovered dynamically.

## Exposure is per console

- Local and Agents consoles expose every family.
- Source and Deploy consoles expose every family except remote.
- Remote console exposes every family except agents.
- Read `PATH` rather than assuming it. `command -v <Tool>.fn.sh` is the authority on whether a tool is reachable from where you stand.

## Two faults, one check

- A family's directory is on `PATH` and the command is missing: that package is not installed here.
- The family's directory is absent from `PATH`: this console does not expose that family.
- Tell the two apart before concluding a tool is broken or gone.

## Completion is an offer, not authority

- Consoles that register tab-completions register them for every family regardless of which ones their own `PATH` carries. A name that completes is not proof the command resolves.
