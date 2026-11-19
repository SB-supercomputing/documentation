# Python

A high-level programming language widely used for general-purpose and AI applications.

Python is a versatile, high-level programming language used in a wide range of applications including data analysis, machine learning, web development, and scientific computing. Python's rich ecosystem of libraries and frameworks makes it a popular choice for both beginners and experienced developers. SeaWulf provides multiple Python versions accessible via the module command.

**Module name:** `python`

## Loading Python

- module: `python/3.11.2`
- module: `python/3.12.0`
- module: `python/3.9.7`
- module: `py/2.7.15`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the Python module**

```
module load python/3.12.0
```

## Availability

Python is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Programming languages

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/python> (maintained by Research Computing and Informatics).
