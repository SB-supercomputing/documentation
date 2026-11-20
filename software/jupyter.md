# Jupyter

A web-based interactive computing environment supporting many languages, especially Python.

Jupyter is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations, and narrative text. It supports multiple programming languages, including Python, R, and Julia, making it a powerful tool for interactive computing and data analysis.

**Module name** `jupyter`

## Loading Jupyter

- module `r-jupyter/4.0.2`
- module `jupyter/7.4.4`
- module `jupyter/latest`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load a Jupyter module**

```
module load jupyter/7.4.4
```

## Availability

Jupyter is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/jupyter> (maintained by Research Computing and Informatics).
{: .rci-credit }
