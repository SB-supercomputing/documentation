# CMake

A free tool that sets up how software projects are built.

CMake is a powerful cross-platform build system generator. It helps developers automate the process of building, testing, and packaging software. CMake is widely used in C++ and other programming environments for managing build processes.

**Module name** `cmake`

## Loading CMake

- module `cmake/3.5.1`
- module `cmake/3.8.0`
- module `cmake/3.13.2`
- module `cmake/3.16.2`
- module `cmake/3.17.3`
- module `cmake/3.19.5`
- module `cmake/3.24.2`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the CMake module**

```
module load cmake/3.24.2
```

## Availability

CMake is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/cmake> (maintained by Research Computing and Informatics).
{: .rci-credit }
