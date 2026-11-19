# AmberMD

A suite of biomolecular simulation programs focusing on molecular dynamics and free energy.

AMBER is a suite of biomolecular simulation programs that provides tools for molecular dynamics, quantum mechanics, and molecular mechanics simulations. The software serves chemistry, biophysics, and structural biology research for studying proteins, nucleic acids, and molecular systems.

**Module name** `amber`

## Loading AmberMD

- module `amber/16`
- module `amber/22`
- module `amber/24`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the AMBER module**

```
module load amber/24
```

## Availability

AmberMD is available on: SeaWulf, NVwulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/ambermd> (maintained by Research Computing and Informatics).
{: .rci-credit }
