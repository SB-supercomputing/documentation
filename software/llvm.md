# LLVM

A collection of modular and reusable compiler and toolchain technologies.

The LLVM Project is a collection of modular and reusable compiler and toolchain technologies.

**Module name** `llvm`

## Loading LLVM

- module `llvm/3.9.1`
- module `llvm/7.1.0`
- module `llvm/10.0.1`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load LLVM**

```
module load llvm/10.0.1
```

## Availability

LLVM is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/llvm> (maintained by Research Computing and Informatics).
{: .rci-credit }
