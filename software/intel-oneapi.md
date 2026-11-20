# Intel oneAPI

A unified programming model with support for Intel CPUs, GPUs, and FPGAs.

Intel oneAPI is seamlessly integrated into SeaWulf as a module, making it easily accessible to users who require its powerful toolkit. With oneAPI, you can develop across diverse computing architectures, simplifying complex tasks and enhancing the versatility and performance of SeaWulf's supercomputing capabilities. This unified programming model streamlines development, allowing researchers, staff, and students to optimize their workflows across multiple platforms and environments with efficiency.

**Module name** `intel-oneapi`

## Loading Intel oneAPI

- module `intel/oneAPI/2024.2`
- module `tbb/latest`
- module `compiler-rt/latest`
- module `compiler/latest`
- module `mkl/latest`
- module `mpi/latest`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `icx` New LLVM-based Intel C compiler
- `icpx` New LLVM-based Intel C++ compiler
- `ifx` New LLVM-based Intel Fortran compiler
- `icc` Classic Intel C compiler
- `icpc` Classic Intel C++ compiler
- `ifort` Classic Intel Fortran compiler
- `mpiicx / mpiicpx / mpiifx` MPI wrappers for the new Intel compilers
- `mpiicc / mpiicpc / mpiifort / mpicc / mpicxx / mpifort` MPI wrappers for classic Intel and GCC compilers

## Example usage

**Load the Intel oneAPI stack**

```
module load intel-stack
```

**Compile with the new LLVM-based compilers**

```
icx myprogram.c -o myprogram
icpx myprogram.cpp -o myprogram
ifx myprogram.f90 -o myprogram
```

**Compile with the classic Intel compilers**

```
icc myprogram.c -o myprogram
icpc myprogram.cpp -o myprogram
ifort myprogram.f90 -o myprogram
```

## Availability

Intel oneAPI is available on: SeaWulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/intel-oneapi> (maintained by Research Computing and Informatics).
{: .rci-credit }
