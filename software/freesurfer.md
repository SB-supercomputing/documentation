# Freesurfer

A suite for the analysis and visualization of structural and functional neuroimaging data.

The FreeSurfer module provides software for the analysis and visualization of neuroimaging data, including tools for processing MRI data and performing various analyses on brain structures.

**Module name:** `freesurfer`

## Loading Freesurfer

- module: `freesurfer/5.3.0-HCP`
- module: `freesurfer/6.0.0`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the FreeSurfer module**

```
module load freesurfer/6.0.0
```

## Availability

Freesurfer is available on: SeaWulf, ClinWulf.

**Category:** Neuroimaging

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/freesurfer> (maintained by Research Computing and Informatics).
