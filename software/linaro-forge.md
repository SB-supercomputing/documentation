# Linaro Forge

A platform providing tools for optimizing and debugging HPC and ARM-based systems.

Linaro Forge is a suite of tools designed to help users efficiently build and optimize software for ARM-based systems. It provides a comprehensive set of tools for developers to enhance performance and debugging during the development lifecycle.

**Module name** `linaro-forge`

## Loading Linaro Forge

- module `linaro-forge/23.0.4`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the Linaro Forge module**

```
module load linaro-forge/23.0.4
```

## Availability

Linaro Forge is available on: SeaWulf, NVwulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/linaro-forge> (maintained by Research Computing and Informatics).
{: .rci-credit }
