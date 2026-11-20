# GCC

A popular open-source compiler for C, C++, and other languages.

The GNU Compiler Collection (GCC) is a cornerstone of high-performance computing on SeaWulf, offering a comprehensive set of compilers and development tools for scientific and technical applications. This open-source toolchain supports multiple programming languages and integrates with MPI implementations for parallel computing on SeaWulf's supercomputing environment.

**Module name** `gcc-stack`

## Loading GCC

- module `gcc-stack: GCC 13.2 + MVAPICH 2.3.7 (recommended)`
- module `gcc/13.2.0 · mvapich2/gcc13.2/2.3.7`
- module `gcc/12.1.0 · mvapich2/gcc12.1/2.3.7 (alternative)`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `gcc` C compiler
- `g++` C++ compiler
- `gfortran` Fortran compiler
- `mpicc / mpicxx / mpif90` MVAPICH MPI wrappers

## Example usage

**Load the recommended GCC stack**

```
module load gcc-stack
```

**Compile with GCC compilers**

```
gcc myprogram.c -o myprogram
g++ myprogram.cpp -o myprogram
gfortran myprogram.f90 -o myprogram
```

**Compile MPI programs with wrapper scripts**

```
mpicc mpi_program.c -o mpi_program
mpicxx mpi_program.cpp -o mpi_program
mpif90 mpi_program.f90 -o mpi_program
```

**Optimization examples**

```
gcc -O3 myprogram.c -o myprogram
gcc -Ofast myprogram.c -o myprogram
gcc -march=native myprogram.c -o myprogram
gcc -O3 -ftree-vectorize -fopt-info-vec myprogram.c -o myprogram
gcc -O3 -fprofile-generate myprogram.c -o myprogram
./myprogram
gcc -O3 -fprofile-use myprogram.c -o myprogram
```

**SLURM script example (GCC + MVAPICH)**

```
#!/bin/bash
#SBATCH --job-name=gcc_test
#SBATCH --output=gcc_test.out
#SBATCH -p short-40core
#SBATCH --ntasks=40
#SBATCH --time=01:00:00 # Load necessary modules module load gcc-stack # Compile and run your code mpicc -O3 mpi_example.c -o mpi_example
mpirun -np $SLURM_NTASKS ./mpi_example
```

## Availability

GCC is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/gcc> (maintained by Research Computing and Informatics).
{: .rci-credit }
