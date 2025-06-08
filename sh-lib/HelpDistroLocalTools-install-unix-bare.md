# Myx.distro Workspace Utility

This utility facilitates **myx.distro** workspace (directory) creation and allows installation of  
`myx.distro-remote`, `myx.distro-deploy` or `myx.distro-source` applications in any **myx.distro** workspace.

---

## Installation (Variant: Unix, Bare)

Following steps should be performed in the shell:

1. **Open your shell terminal**, and:  
   1. Ensure you are using **bash** by running:  
      bash  
   2. Verify that `git` is installed and working:  
      git --version

2. **Create an empty workspace folder and change into it**:  
   1. Create a root directory for your workspace (e.g., `/Volumes/disk2/hobby-set`):  
      mkdir -p /Volumes/disk2/hobby-set  
   2. Change into that directory:  
      cd /Volumes/disk2/hobby-set

3. **Clone the Git repository** for `git@github.com:myx/myx.distro-.local.git` into  
   `.local/myx/myx.distro-.local`:  
   mkdir -p .local/myx/  
   ( cd .local/myx && git clone git@github.com:myx/myx.distro-.local.git )

4. **Run the installer script** using one of the following commands, depending on your desired setup:

   - **Empty workspace** (to be configured later):  
     bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.sh --init-distro-workspace

   - **Remote workspace tools** (connect to source and deploy machines on remote hosts or local VMs):  
     bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.sh --install-distro-remote

   - **Deploy workspace tools** (deployment runners or admin terminal servers):  
     bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.sh --install-distro-deploy

   - **Source workspace tools** (build system runners or local source for developers):  
     bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.sh --install-distro-source






# Myx.distro Workspace Utility

This utility facilitates **myx.distro** workspace (directory) creation and allows installation of  
`myx.distro-remote`, `myx.distro-deploy` or `myx.distro-source` applications in any **myx.distro** workspace.

