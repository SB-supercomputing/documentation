# FSL

A comprehensive library of analysis tools for FMRI, MRI, and DTI data.

The FSL module provides a comprehensive library of analysis tools for processing functional, structural, and diffusion MRI brain imaging data. FSL includes a range of tools for image analysis, such as preprocessing, statistical analysis, and visualization.

**Module name** `fsl`

## Loading FSL

- module `fsl/5.0.6`
- module `fsl/5.0.10`
- module `fsl/6.0.0`
- module `fsl/6.0.4`
- module `fsl/6.0.6.5`
- module `fsl/6.0.7.10`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the FSL module**

```
module load fsl/6.0.7.10
```

## Availability

FSL is available on: SeaWulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/fsl> (maintained by Research Computing and Informatics).
{: .rci-credit }
