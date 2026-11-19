# MATLAB

A high-performance language for technical computing, data analysis, and algorithm development.

MATLAB is a high-performance programming language and environment used for numerical computing, algorithm development, data analysis, and visualization. It is widely used in engineering, scientific research, and academic settings to analyze large datasets, develop models, and perform simulations.

**Module name** `matlab`

## Loading MATLAB

- module `matlab/2016`
- module `matlab/2017a`
- module `matlab/2017b`
- module `matlab/2018a`
- module `matlab/2019a`
- module `matlab/2021a`
- module `matlab/2021b`
- module `matlab/2022a`
- module `matlab/2023a`
- module `matlab/2024a`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the MATLAB module**

```
module load matlab/2024a
```

## Availability

MATLAB is available on: SeaWulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/matlab> (maintained by Research Computing and Informatics).
{: .rci-credit }
