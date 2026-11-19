# bioconvert

A tool for converting bioinformatics data between various formats.

Bioconvert is a collaborative project to facilitate the interconversion of life science data from one format to another. Users cannot simultaneously activate multiple conda environments, so this module should not be loaded alongside other conda-linked or custom environments.

**Module name:** `bioconvert`

## Loading bioconvert

- module: `bioconvert/1.0.0 (default)`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load bioconvert**

```
module load bioconvert
```

**Load a specific version**

```
module load bioconvert/<version>
```

## Availability

bioconvert is available on: SeaWulf, ClinWulf.

**Category:** Bioinformatics

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/bioconvert> (maintained by Research Computing and Informatics).
