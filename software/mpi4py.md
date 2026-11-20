# mpi4py

A Python interface for MPI-based parallel computing.

mpi4py provides Python bindings for the Message Passing Interface (MPI) standard, allowing Python programs to exploit multiple processors on multiple compute nodes. Do not load other MPI modules alongside it, as this may cause version conflicts and job failures; install mpi4py via conda rather than pip.

**Module name** `mpi4py`

## Loading mpi4py

- module `mpi4py/latest`
- module `anaconda/3`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the system mpi4py module**

```
module load mpi4py/latest
```

**Create a conda environment with mpi4py**

```
module load anaconda/3
conda create --name my_parallel_env mpi4py numpy pandas
source activate my_parallel_env
```

**Run an mpi4py script**

```
mpirun -n $SLURM_NTASKS python my_script.py
```

**Example Python script**

```
from mpi4py import MPI comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() print(f"Hello from process {rank} out of {size}!")
```

## Availability

mpi4py is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/mpi4py> (maintained by Research Computing and Informatics).
{: .rci-credit }
