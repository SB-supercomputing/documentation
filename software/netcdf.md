# NetCDF

Libraries and machine-independent formats for array-oriented scientific data.

NetCDF is a widely used format for array-oriented scientific data, especially for climate and weather simulations.

**Module name** `netcdf`

## Loading NetCDF

- module `netcdf/intel2022.2/4.9.0`
- module `netcdf/aocc4.0/openmpi4.1.5/4.9.0`
- module `netcdf/gcc12.1/openmpi4.1.4/4.9.0`
- module `netcdf/intel2023.1/4.9.0`
- module `netcdf-fortran/aocc/4.5.3`
- module `netcdf/gcc/4.7.3-parallel`
- module `netcdf-fortran/intel/4.5.3`
- module `netcdf/gcc/fortran/4.5.2-parallel`
- module `netcdf-operators/1.0`
- module `netcdf/aocc/4.9.2`
- module `netcdf/gcc/4.7.1`
- module `netcdf/gcc/4.7.1-gcc-4.8.5`
- module `netcdf/gcc/4.7.1-gcc-6.5.0`
- module `netcdf/gcc/4.7.1-gcc-7.1.0`
- module `netcdf/intel/64/4.1.1`
- module `netcdf/intel/64/4.7.4-parallel`
- module `netcdf/rpm/64/4.1.1-3`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the NetCDF module**

```
module load netcdf/intel2022.2/4.9.0
```

**Compile a program against NetCDF**

```
mpicc -o my_netcdf_program my_netcdf_program.c -lnetcdf
```

## Availability

NetCDF is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/netcdf> (maintained by Research Computing and Informatics).
{: .rci-credit }
