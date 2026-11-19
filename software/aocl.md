# AOCL

AMD's collection of optimized math libraries for scientific workloads on AMD CPUs.

AMD Optimizing CPU Libraries (AOCL) is a set of performance-optimized math libraries tailored for scientific and engineering applications on AMD CPUs. The suite includes routines for linear algebra, FFTs, random number generation, and more, and is optimized for AMD EPYC processors to deliver high performance on supported hardware.

**Module name** `aocl`

## Loading AOCL

- module `aocl/4.2.0`
- module `aocl/4.0.0`
- module `aocl/3.1.0`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load an AOCL module**

```
module load aocl/4.2.0
```

**Link a program with AOCL using GCC**

```
gcc -o my_program my_program.c -laocl
```

## Availability

AOCL is available on: SeaWulf.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/aocl> (maintained by Research Computing and Informatics).
{: .rci-credit }
