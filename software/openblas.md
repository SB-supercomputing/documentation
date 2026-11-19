# OpenBLAS

An open-source implementation of the BLAS library for linear algebra operations.

OpenBLAS is an optimized library for performing Basic Linear Algebra Subprograms (BLAS) and Linear Algebra operations. Multiple versions are provided on SeaWulf, enabling users to select based on performance requirements and cluster setup. OpenBLAS is highly optimized for parallel computations, so it is important to select the correct version that fits your application and environment to ensure the best performance.

**Module name** `openblas`

## Loading OpenBLAS

- module `openblas/0.3.21`
- module `openblas/dynamic/(default)`
- module `openblas/dynamic/0.2.18`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load an OpenBLAS module**

```
module load openblas/dynamic/(default)
```

**Compile a program against OpenBLAS**

```
gcc -o my_openblas_program my_openblas_program.c -lopenblas
```

## Availability

OpenBLAS is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/openblas> (maintained by Research Computing and Informatics).
{: .rci-credit }
