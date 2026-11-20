# FFTW3

A C library for computing discrete Fourier transforms in one or more dimensions.

FFTW (Fastest Fourier Transform in the West) is a highly optimized library for computing discrete Fourier transforms (DFTs). Multiple versions are available, optimized for various compilers and MPI configurations. Incompatible versions of FFTW, MPI, or compilers can lead to errors or degraded performance.

**Module name** `fftw3`

## Loading FFTW3

- module `fftw3/mvapich2/gcc12.1/3.3.10`
- module `fftw2/openmpi/gcc/64/double/2.1.5`
- module `fftw3/mvapich2/3.3.8-float`
- module `fftw2/openmpi/gcc/64/float/2.1.5`
- module `fftw3/openmpi/gcc/64/3.3.7`
- module `fftw3/mvapich2/3.3.8`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the FFTW3 module**

```
module load fftw3/mvapich2/gcc12.1/3.3.10
```

**Compile a program against FFTW3**

```
mpicc -o my_fftw_program my_fftw_program.c -lfftw3
```

## Availability

FFTW3 is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/fftw3> (maintained by Research Computing and Informatics).
{: .rci-credit }
