# AOCC

AMD's Optimizing C Compiler, designed for high performance on AMD architectures.

The AMD Optimizing C/C++ Compiler (AOCC) is a high-performance compiler suite designed specifically for AMD processors on the SeaWulf computing environments. AOCC provides advanced optimization techniques tailored for AMD EPYC processors, delivering enhanced performance for scientific and technical applications running on AMD hardware. This compiler suite is built on the LLVM/Clang infrastructure and incorporates AMD-specific optimizations that leverage the unique architecture of AMD CPUs.

**Module name** `aocc`

## Loading AOCC

- module `aocc/3.2.0`
- module `aocc/4.0.0`
- module `aocc/4.2.0`
- module `openmpi/aocc4.2/4.1.5`
- module `openmpi/aocc4.0/4.1.5`
- module `mvapich2/aocc4.2/2.3.7`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `clang` C Compiler
- `clang++` C++ Compiler
- `flang` Fortran Compiler
- `mpicc (OpenMPI)` AOCC C compiler wrapper
- `mpicxx (OpenMPI)` AOCC C++ compiler wrapper
- `mpifort (OpenMPI)` AOCC Fortran compiler wrapper
- `mpicc (MVAPICH2)` AOCC C compiler wrapper
- `mpicxx (MVAPICH2)` AOCC C++ compiler wrapper
- `mpif90 (MVAPICH2)` AOCC Fortran compiler wrapper

## Example usage

**Load AOCC**

```
module load aocc/4.2.0
```

**Load AOCC with OpenMPI**

```
module load aocc/4.2.0
module load openmpi/aocc4.2/4.1.5
```

**Load AOCC with MVAPICH2**

```
module load aocc/4.2.0
module load mvapich2/aocc4.2/2.3.7
```

**Verify compiler location**

```
which clang
```

**Compile with AOCC compilers**

```
clang myprogram.c -o myprogram
clang++ myprogram.cpp -o myprogram
flang myprogram.f90 -o myprogram
```

**Compile MPI programs with wrapper scripts**

```
mpicc mpi_program.c -o mpi_program
mpicxx mpi_program.cpp -o mpi_program
mpifort mpi_program.f90 -o mpi_program
mpif90 mpi_program.f90 -o mpi_program
```

**Optimization examples**

```
clang -O3 myprogram.c -o myprogram
clang -Ofast myprogram.c -o myprogram
clang -march=znver3 myprogram.c -o myprogram
clang -O3 -fvectorize -Rpass=loop-vectorize myprogram.c -o myprogram
```

**Profile-guided optimization**

```
clang -O3 -fprofile-instr-generate myprogram.c -o myprogram
./myprogram
llvm-profdata merge -output=myprogram.profdata default.profraw
clang -O3 -fprofile-instr-use=myprogram.profdata myprogram.c -o myprogram
```

**Link AMD math library**

```
clang -O3 -march=znver3 myprogram.c -o myprogram -lamdlibm
```

**Aggressive inlining**

```
clang -O3 -finline-functions -mllvm -inline-threshold=1000 myprogram.c -o myprogram
```

## Availability

AOCC is available on: SeaWulf.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/aocc> (maintained by Research Computing and Informatics).
{: .rci-credit }
