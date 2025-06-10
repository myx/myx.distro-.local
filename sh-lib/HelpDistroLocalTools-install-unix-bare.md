# myx.distro-.local, Workspace Utility

This utility facilitates **myx.distro** workspace (directory) creation and allows installation of  
`myx.distro-remote`, `myx.distro-deploy` or `myx.distro-source` applications in any **myx.distro** workspace.

---

## Installation (Variant: Unix, Bare)

Following steps should be performed in the shell:

1. **Open your shell terminal**, and:  
   1. Ensure you are using **bash** by running:  
   		bash -c 'echo Hello!'
	 you should get:
		`Hello!`

   2. Verify that **git** is installed and working:  
   		git --version
	 you should get something like:
		`git version 2.39.5 (Apple Git-154)`

   2. Verify that **git** is configured to work with **gihhub.com**:  
   		ssh -T git@github.com
	 you should get something like:
		`Hi XXX! You've successfully authenticated, but GitHub does not provide shell access.`

2. **Create an empty workspace folder** and **change your current working directoy** into it:  
   1. Create a root directory for your workspace (e.g., `/Volumes/disk2/hobby-set`):  
      mkdir -p /Volumes/disk2/hobby-set  
   2. Change into that directory:  
      cd /Volumes/disk2/hobby-set

3. While in workspace root directory, **Clone the Git repository** for 
   `git@github.com:myx/myx.distro-.local.git` into  
   `.local/myx/myx.distro-.local`:  

	mkdir -p .local/myx/  

	( cd .local/myx && git clone git@github.com:myx/myx.distro-.local.git )

4. **Run the installer script** using one of the following commands, depending on your desired setup:

   - **Empty workspace** (to be configured later):  

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --init-distro-workspace

   - **Remote workspace tools** (connect to source and deploy machines on remote hosts or local VMs):  

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --install-distro-remote

   - **Deploy workspace tools** (deployment runners or admin terminal servers):  

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --install-distro-deploy

   - **Source workspace tools** (build system runners or local source for developers):  

	bash .local/myx/myx.distro-.local/sh-scripts/DistroLocalTools.fn.sh --install-distro-source

5. Then you can **Enter Local Console** any time by running `DistroLocalConsole.sh` from
   your workspace directory. 
