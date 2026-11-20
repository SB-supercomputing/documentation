# NAMD

A parallel molecular dynamics code for high-performance simulation of large biomolecular systems.

NAMD is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems. It is widely used in computational biology and biophysics to model the behavior of proteins, nucleic acids, and other molecules.

**Module name** `namd`

## Loading NAMD

- module `namd/2.9`
- module `namd/2.13`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the NAMD module**

```
module load namd/2.13
```

## Availability

NAMD is available on: SeaWulf, NVwulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/namd> (maintained by Research Computing and Informatics).
{: .rci-credit }
