# GROMACS

A versatile, efficient package for performing molecular dynamics simulations.

GROMACS is a highly efficient molecular dynamics simulation software package used for simulating biomolecular systems such as proteins, lipids, and nucleic acids. It is optimized for high-performance simulations and is widely used in computational chemistry and biophysics.

**Module name:** `gromacs`

## Loading GROMACS

- module: `gromacs/5.1.1`
- module: `gromacs/gcc12/mvapich2/2022.2-skylake`
- module: `gromacs/aocc3.2/mvapich2/2022.2-epyc`
- module: `gromacs/gcc12/mvapich2/2023.2-a100`
- module: `gromacs/aocc3.2/openmpi/2022.2-epyc`
- module: `gromacs/intel2022.2/mpi/2022.2-epyc`
- module: `gromacs/gcc12/mvapich2/2022.2-epyc`
- module: `gromacs/intel2022.2/mpi/2022.2-skylake`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the GROMACS module**

```
module load gromacs/gcc12/mvapich2/2023.2-a100
```

## Availability

GROMACS is available on: SeaWulf, NVwulf.

**Category:** Molecular dynamics & chemistry

**Applies to:** SeaWulf, NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/gromacs> (maintained by Research Computing and Informatics).
