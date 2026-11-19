# Intel MPI

A high-performance, production-quality MPI implementation for Intel architectures.

Intel MPI (Message Passing Interface) is a high-performance, scalable parallel programming library used to develop parallel applications across distributed systems. On SeaWulf, it is accessible both as standalone modules and through Intel's oneAPI toolkit.

**Module name** `intel-mpi`

## Loading Intel MPI

- module `intel/mpi/32/2017/0.098`
- module `intel/mpi/64/2017/0.098`
- module `intel/mpi/64/2018/18.0.0`
- module `intel/mpi/64/2018/18.0.1`
- module `intel/mpi/64/2018/18.0.2`
- module `intel/mpi/64/2019/19.0.0`
- module `intel/mpi/64/2019/19.0.3`
- module `intel/mpi/64/2019/19.0.4`
- module `intel/mpi/64/2019/19.0.5`
- module `intel/mpi/64/2020/20.0.0`
- module `intel/mpi/64/2020/20.0.1`
- module `intel/mpi/64/2020/20.0.2`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load an Intel MPI module**

```
module load intel/mpi/64/2020/20.0.2
```

**Load Intel MPI via oneAPI**

```
module load intel/oneAPI/ mpi
```

**Compile an MPI program**

```
mpiicc -o my_mpi_program my_mpi_program.c
```

**Run an MPI job**

```
mpirun -np 4 ./my_mpi_program
```

## Availability

Intel MPI is available on: SeaWulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/intel-mpi> (maintained by Research Computing and Informatics).
{: .rci-credit }
