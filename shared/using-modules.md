# Using modules

Software on the clusters is organized into *modules*. Loading a module sets up everything a program needs, and unloading it takes it away again, so you can switch between packages and versions without clashes.

**On this page:** [The basics](#basics) · [Find software](#find) · [Modules in job scripts](#jobs) · [Node types](#arch) · [Troubleshooting](#trouble)

## The basics {#basics}

```
module avail                   # everything you can load
module load python/3.11.2      # load a package (a specific version)
module list                    # what's loaded right now
module unload python/3.11.2    # remove one
module purge                   # remove everything and start clean
```

Tip: always name the version (`python/3.11.2`, not just `python`) so your results don't change when a newer default arrives.

## Find software {#find}

```
module avail python            # search by name
module show python/3.11.2      # what a module sets up, and where it lives
```

You can also browse the [software catalog](../software/README.md), which has load instructions for each package. Can't find what you need? You can [install it yourself](managing-custom-software.md) or ask RCI to add it.

## Modules in job scripts {#jobs}

Jobs don't inherit what you loaded at the prompt reliably, so load modules inside every job script:

```
#!/bin/bash
#SBATCH -p short-40core
#SBATCH --time=01:00:00

module purge                   # start clean
module load gcc/12.3.0
module load python/3.11.2

python my_script.py
```

If you compiled a program, load the same modules at run time that you used to build it.

## Node types matter {#arch}

SeaWulf has several kinds of compute nodes, and some software versions only exist for some of them:

- 40-core Intel Skylake
- 96-core AMD EPYC Milan
- 96-core Intel Sapphire Rapids (HBM)

If a module won't load or a program crashes, check that you're on the right login node for your target queue (see [Which SeaWulf login node?](connecting-cluster.md#login-nodes)) and that the version was built for that node type.

## Troubleshooting {#trouble}

<details markdown="1">
<summary>"Unable to locate a modulefile"</summary>

Check the exact name and version with `module avail <name>`. Some modules only appear on certain login nodes.

</details>

<details markdown="1">
<summary>Two modules conflict</summary>

Run `module purge` and load only what you need, compilers first, then libraries, then applications.

</details>

!!! note ""
    **Need new software or a different version?** Submit a request at [iacs.supportsystem.com](https://iacs.supportsystem.com/).

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/using-modules> (maintained by Research Computing and Informatics).
{: .rci-credit }
