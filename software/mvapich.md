# MVAPICH

A high-performance MPI implementation for modern interconnects.

MVAPICH is a high-performance MPI implementation designed for both Infiniband and Ethernet networks, suitable for distributed parallel applications. On SeaWulf, it supports Skylake, Milan, and Haswell architectures with varying compiler and version configurations.

**Module name:** `mvapich2`

## Loading MVAPICH

- module: `mvapich/gcc13.2/3.0`
- module: `mvapich2/gcc13.2/2.3.7`
- module: `mvapich2/gcc7.1/64/2.2rc1`
- module: `mvapich2/gcc12.1/cuda12/2.3.7`
- module: `mvapich2/aocc3.2/2.3.7`
- module: `mvapich2/gcc10.2/2.3.7`
- module: `mvapich2/gcc/64/2.2rc1`
- module: `mvapich2/gcc12.1/2.3.7`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load MVAPICH**

```
module load mvapich/gcc13.2/3.0
```

**Compile an MPI program**

```
mpicc -o my_mpi_program my_mpi_program.c
```

**Run an MPI job**

```
mpirun -np 4 ./my_mpi_program
```

## Availability

MVAPICH is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** MPI implementations

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/mvapich> (maintained by Research Computing and Informatics).
