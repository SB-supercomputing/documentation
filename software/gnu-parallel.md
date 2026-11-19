# GNU Parallel

A shell tool for executing jobs in parallel using one or more computers.

GNU Parallel is a shell tool for executing jobs in parallel using one or more computers. It is commonly used for distributing tasks across multiple CPU cores or nodes, improving efficiency in high-performance computing environments.

**Module name** `parallel`

## Loading GNU Parallel

- module `gnu-parallel/6.0`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the GNU Parallel module**

```
module load gnu-parallel/6.0
```

## Availability

GNU Parallel is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/gnu-parallel> (maintained by Research Computing and Informatics).
{: .rci-credit }
