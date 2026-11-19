# OpenMPI

An open-source MPI implementation that supports a wide range of protocols.

OpenMPI is a widely-used implementation of the Message Passing Interface (MPI) that allows for parallel processing across distributed systems. It is available on SeaWulf for Skylake, Milan, and Haswell nodes with varying versions and compiler support.

**Module name:** `openmpi`

## Loading OpenMPI

- module: `openmpi/gcc12.1/4.1.4`
- module: `openmpi/aocc4.0/4.1.5`
- module: `openmpi/gcc13.2/4.1.6`
- module: `openmpi/gcc13.2/5.0.2`
- module: `openmpi/1.10.1`
- module: `openmpi/3.1.5`
- module: `openmpi/aocc3.2/4.1.1`
- module: `openmpi/openmpi-opal`
- module: `openmpi/1.10.1-test`
- module: `openmpi/4.0.1`
- module: `openmpi/gcc11.2/4.1.1`
- module: `openmpi/3.0.0`
- module: `openmpi/4.0.5`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load OpenMPI**

```
module load openmpi/gcc13.2/5.0.2
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

OpenMPI is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** MPI implementations

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/openmpi> (maintained by Research Computing and Informatics).
