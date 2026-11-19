# Vectorization Flags

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

To enable vectorization it is important to set specific flags for the compiler. There are also flags for causing the compiler to generate messages on what it did vectorize. Here the most important flags are given.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | **Cray** | | **Arm** | **GNU** | **Nvidia** |
|  | **Flags** | | | | |
|  | Pre-23 CPE<br> | CPE 23 and later: <br>(not applicable for Fortran)<br> | all versions<br> | >= gcc 11 | all versions<br> |
| **Optimization** | -O3 | -O3<br> | -O3 or -Ofast | -O3 or -Ofast | -fast (check documentation) |
| **Vectorization** | -h vector3 | Automatic (if -O3 or -O2 flag is set) | -mcpu=a64fx -armpl | -mcpu=a64fx | -tp=native (on a64fx node) |
| **Vectorization report** | -h msgs | -Rpass=loop-vectorize | -Rpass=loop-vectorize | -fopt-info-vec | -Minfo=vect |
| **Report on missed optimization** | -h negmsgs | -Rpass-analysis=loop-vectorize | -Rpass-analysis=loop-vectorize | -fopt-info-vec-missed | -Mneginfo |
| **OpenMP** | -h omp | -fopenmp | -fopenmp | -fopenmp | -mp  -acc for OpenACC |
| **Debugging** | -G 2 | -ggdb<br> | -ggdb | -ggdb | -g or -gopt (see documentation) |
| **Large memory** | -h pic | -mcmodel=large | -mcmodel=large | -mcmodel=large | -mcmodel=large |
| **Module** | CPE/*version* | CPE/23.02(or newer)<br> | arm-modules/*version* | gcc/*version* | nvidia/nvhpc-nompi/version |
|  | **Compiler names** | | | | |
| **C** | cc<br> | | armclang | gcc | nvc |
| **C++** | CC<br> | | armclang++ | g++ | nvc++ |
| **Fortran** | ftn<br> | | armflang | gfortran | nvfortran |

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/Vectorization_Flags.php`, retrieved November 5, 2026.
{: .archive-credit }
