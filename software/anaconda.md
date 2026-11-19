# Anaconda

A free, open-source distribution of Python and R for scientific computing.

Anaconda is a popular open-source distribution of Python and R for scientific computing, data analysis, and machine learning. It simplifies package management and deployment and includes a wide range of pre-installed libraries and tools, such as NumPy, pandas, and scikit-learn, for efficient data science workflows.

**Module name:** `anaconda`

## Loading Anaconda

- module: `anaconda/`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the Anaconda module**

```
module load anaconda/
```

## Availability

Anaconda is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Development

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/anaconda> (maintained by Research Computing and Informatics).
