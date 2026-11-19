# diffexp

A tool for differential expression analysis in bioinformatics datasets.

This environment contains a variety of tools for quantifying and comparing gene expression from RNA-Seq data. As you cannot have multiple conda environments active at once, do not load this environment in addition to another conda linked module or local environment.

**Module name:** `diffexp`

## Loading diffexp

- module: `diffexp/1.0 (default)`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load diffexp**

```
module load diffexp
```

**Load a specific version**

```
module load diffexp/<version>
```

## Availability

diffexp is available on: SeaWulf, ClinWulf.

**Category:** Bioinformatics

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/diffexp> (maintained by Research Computing and Informatics).
