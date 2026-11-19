# Git

A free tool that tracks changes to your code.

Git is a widely used version control system that allows users to track changes in source code and collaborate on projects. The Git module is only intended for use on the Haswell nodes, which do not natively have access to Git.

**Module name:** `git`

## Loading Git

- module: `git/2.12.2`
- module: `git/2.36.2`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the Git module**

```
module load git/2.12.2
```

## Availability

Git is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Development

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/git> (maintained by Research Computing and Informatics).
