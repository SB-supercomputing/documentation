# MPFR

A C library for multiple-precision floating-point computation with correct rounding.

MPFR is a library for performing high-precision floating-point arithmetic with correct rounding. It is designed for applications that require reliable numerical computation with arbitrary precision.

**Module name** `mpfr`

## Loading MPFR

- module `mpfr/3.1.5`
- module `mpfr/4.0.0`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the mpfr module**

```
module load mpfr/4.0.0
```

## Availability

MPFR is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/mpfr> (maintained by Research Computing and Informatics).
{: .rci-credit }
