# Example jobs

## Overview

These examples show different job types on SeaWulf. Each explains the resource choices and when to use that configuration.

## 1 · Serial job (hello world)

```
#!/bin/bash
#SBATCH -p short-40core-shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 5G
#SBATCH -t 00:05:00
#SBATCH -o hello.out

echo "Hello from SeaWulf!"
```

One task on a shared partition with modest memory. Suits quick tests or small scripts: a serial program needs minimal resources.

## 2 · Python job

```
#!/bin/bash
#SBATCH -p short-40core
#SBATCH -N 1
#SBATCH -n 40
#SBATCH -t 00:10:00
#SBATCH -o python.out

module load anaconda
conda activate my-environment
python script.py
```

Python scripts are typically single-threaded unless using multi-threaded libraries (NumPy, PyTorch, Dask). If your script is single-threaded, run on one core in a shared partition instead. Requesting all 40 cores wastes resources.

## 3 · MPI job

```
#!/bin/bash
#SBATCH -p short-40core
#SBATCH -N 2
#SBATCH -n 80
#SBATCH -t 00:10:00
#SBATCH -o mpi.out

module load openmpi
mpirun ./my_mpi_program
```

Two nodes × 40 tasks fully utilize all cores across both nodes: each MPI rank handles part of the workload.

## 4 · OpenMP job

```
#!/bin/bash
#SBATCH -p short-40core
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 40
#SBATCH -t 00:10:00
#SBATCH -o openmp.out

export OMP_NUM_THREADS=40
./my_openmp_program
```

OpenMP uses threads, not separate processes: one task (`-n 1`) with 40 cores (`-c 40`), and `OMP_NUM_THREADS=40` so the program uses them all.

## 5 · GPU job

```
#!/bin/bash
#SBATCH -p a100
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 50G
#SBATCH --gres=gpu:1
#SBATCH -t 00:30:00
#SBATCH -o gpu.out

module load cuda120/toolkit/12.0
./my_gpu_program
```

Request a GPU with `--gres=gpu:1`. One CPU task suffices to launch, though you can request more threads if the program also uses CPU cores.

## 6 · Array job

```
#!/bin/bash
#SBATCH --job-name=parameter_sweep
#SBATCH --array=1-100
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --time=02:00:00
#SBATCH -p short-40core
#SBATCH -o array_%A_%a.out

module load python/3.9

python simulation.py --param-set $SLURM_ARRAY_TASK_ID
```

`--array=1-100` creates 100 jobs, each receiving a unique `$SLURM_ARRAY_TASK_ID`: ideal for parameter sweeps, Monte Carlo simulations, or processing many input files. `%A` is the array job ID, `%a` the task ID.

## Quick reference

| Job type | Use when | Key directives |
| --- | --- | --- |
| Serial | Single-threaded programs | `-n 1` on shared partition |
| Python | Python scripts | `-n 40` or `-n 1` depending on libraries |
| MPI | Distributed parallel programs across nodes | `-N 2 -n 80` |
| OpenMP | Shared-memory threading on single node | `-n 1 -c 40` |
| GPU | CUDA or GPU-accelerated applications | `--gres=gpu:1` |
| Array | Multiple similar runs | `--array=1-100` |

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/example-jobs> (maintained by Research Computing and Informatics).
