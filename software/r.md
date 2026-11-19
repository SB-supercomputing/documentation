# R

A programming language and environment for statistical computing and graphics.

R is a programming language and free software environment for statistical computing and graphics. It is used for data analysis, statistical modeling, and the creation of data visualizations, with a rich ecosystem of libraries and packages for various applications such as machine learning, data mining, and bioinformatics.

**Module name:** `r`

## Loading R

- module: `R/gcc13.2/mkl/4.4.1`
- module: `R/gcc13.2/mkl/a100/4.4.1`
- module: `R/4.4.1`
- module: `R/3.3.2`
- module: `R/3.4.2`
- module: `R/3.4.3`
- module: `R/3.4.4`
- module: `R/3.5.2`
- module: `R/3.6.0`
- module: `R/3.6.2`
- module: `R/4.0.2`
- module: `R/4.1.1`
- module: `R/4.2.1`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the R module**

```
module load R/4.4.1
```

## Availability

R is available on: SeaWulf, ClinWulf.

**Category:** Programming languages

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/r> (maintained by Research Computing and Informatics).
