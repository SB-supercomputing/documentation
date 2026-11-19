# Math libraries on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

There are multiple math libraries available on Ookami, listed below.

[LAPACK: Linear algebra package](https://netlib.org/lapack/)

[BLAS: Basic linear algebra subprograms](https://www.netlib.org/blas/)

[ScaLAPACK: Scalable linear algebra package](https://netlib.org/scalapack/)

## [FFTW: Fastest Fourier Transform in the West](https://www.fftw.org/)

---

The specific implementation of these libraries on Ookami will depend on which compiler you are using.

## Cray LibSci

Cray users can take advantage of the [LibSci library](https://support.hpe.com/hpesc/public/docDisplay?docId=a00115110en_us&docLocale=en_US&page=Cray_Scientific_and_Math_Libraries_CSML_.html) to access versions of BLAS, LAPACK, and SCALAPACK that have been optimized for Cray systems.

To access these libraries on Ookami, please load the following module:

```
module load CPE
```

This will load several Cray modules, including the cray-libsci/20.10.1.2 module.

To additionally make a Cray version of FFTW available, please load the following module (after loading CPE):

```
module load cray-fftw/3.3.8.8
```

## Arm Performance Libraries

The [Arm Performance Libraries](https://developer.arm.com/Tools%20and%20Software/Arm%20Performance%20Libraries) provide optimized versions of BLAS, LAPACK and FFTW. To access these libraries, please do the following:

```
module load arm-modules/22.1
module load armpl/22.1.0
```

Because Arm does not provide an MPI implementation, we have built our own version of SCALAPACK using the Arm compilers and performance libraries along with OpenMPI. To access it, please load the following module:

```
module load scalapack/arm22/2.2.0
```

## OpenBLAS

[OpenBLAS](https://www.openblas.net/) is an optimized and SVE-enabled version of the BLAS library available on Ookami. To access a recent version of OpenBLAS compiled with the latest GCC, please do:

```
module load openblas/gcc13/0.3.21
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/available_math_libraries.php`, retrieved November 5, 2026.
{: .archive-credit }
