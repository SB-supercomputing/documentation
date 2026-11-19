# Intel MKL

A set of highly optimized routines for scientific, engineering, and financial applications.

The Intel Math Kernel Library (MKL) is a highly optimized library for performing mathematical operations such as matrix multiplication, Fast Fourier Transforms (FFT), and vector operations. On SeaWulf, multiple versions are provided to accommodate different application needs. The library supports multi-threading, which can improve performance on parallel systems.

**Module name:** `intel-mkl`

## Loading Intel MKL

- module: `intel/mkl/64/2017/0.098`
- module: `intel/mkl/64/2018/18.0.0`
- module: `intel/mkl/64/2018/18.0.1`
- module: `intel/mkl/64/2018/18.0.2`
- module: `intel/mkl/64/2018/18.0.3`
- module: `intel/mkl/64/2019/19.0.0`
- module: `intel/mkl/64/2019/19.0.3`
- module: `intel/mkl/64/2019/19.0.4`
- module: `intel/mkl/64/2020/20.0.0`
- module: `intel/mkl/64/2020/20.0.1`
- module: `intel/mkl/64/2020/20.0.2`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load an Intel MKL module**

```
module load intel/mkl/64/2020/20.0.2
```

**Compile a program against MKL**

```
icc -o my_program my_program.c -lmkl
```

## Availability

Intel MKL is available on: SeaWulf, ClinWulf.

**Category:** Mathematics & statistics

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/intel-mkl> (maintained by Research Computing and Informatics).
