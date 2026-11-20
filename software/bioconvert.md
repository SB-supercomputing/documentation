# bioconvert

A tool for converting bioinformatics data between various formats.

Bioconvert is a collaborative project to facilitate the interconversion of life science data from one format to another. Users cannot simultaneously activate multiple conda environments, so this module should not be loaded alongside other conda-linked or custom environments.

**Module name** `bioconvert`

## Loading bioconvert

- module `bioconvert/1.0.0 (default)`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

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

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/bioconvert> (maintained by Research Computing and Informatics).
{: .rci-credit }
