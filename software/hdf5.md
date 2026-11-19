# HDF5

A file format and tools for large, complex data.

HDF5 is a versatile data model and file format widely used for storing large, complex data in scientific and engineering fields.

**Module name** `hdf5`

## Loading HDF5

- module `hdf5-parallel/gcc12.1/openmpi/1.12.2`
- module `hdf5-parallel/intel2023.1/1.12.2`
- module `hdf5-parallel/intel2022.2/1.12.2`
- module `hdf5-parallel/intel2024.0/1.14.3`
- module `hdf5-parallel/aocc4.0/openmpi/1.12.2`
- module `hdf5-parallel/gcc12.1/mvapich2/1.12.2`
- module `hdf5/1.6.10`
- module `hdf5/intel/1.6.10-parallel`
- module `hdf5/1.6.10-parallel`
- module `hdf5/intel/1.8.20-parallel`
- module `hdf5/1.8.4`
- module `hdf5/intel/1.10.5-parallel`
- module `hdf5/1.8.17`
- module `hdf5/parallel/intel2022.2/1.12.2`
- module `hdf5/1.8.19`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the HDF5 parallel module**

```
module load hdf5-parallel/gcc12.1/openmpi/1.12.2
```

**Compile a program against HDF5**

```
mpicc -o my_hdf5_program my_hdf5_program.c -lhdf5
```

## Availability

HDF5 is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/hdf5> (maintained by Research Computing and Informatics).
{: .rci-credit }
