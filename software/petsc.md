# PETSc

A suite of data structures and routines for scalable solution of PDE-modeled problems.

PETSc is a suite of data structures and routines for the scalable solution of scientific computations, particularly for problems involving partial differential equations. It provides a high-performance environment for solving large, sparse linear and nonlinear systems of equations, and is widely used in scientific and engineering applications that require parallel computing.

**Module name:** `petsc`

## Loading PETSc

- module: `petsc/intel2024.2/3.4.5`
- module: `petsc/intel2024.2/3.21.5`
- module: `petsc/3.1`
- module: `petsc/3.4.5`
- module: `petsc/3.15.0`
- module: `petsc/3.1-p8`
- module: `petsc/3.7.5`
- module: `petsc/intel2017/3.4.5`
- module: `petsc/3.2-p7`
- module: `petsc/3.14.6`
- module: `petsc/intel2022.2/3.4.5`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the petsc module**

```
module load petsc/3.4.5
```

## Availability

PETSc is available on: SeaWulf, NVwulf.

**Category:** Mathematics & statistics

**Applies to:** SeaWulf, NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/petsc> (maintained by Research Computing and Informatics).
