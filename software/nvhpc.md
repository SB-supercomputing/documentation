# NVHPC

NVIDIA's HPC compiler suite optimized for performance on NVIDIA GPUs.

The NVIDIA HPC SDK (NVHPC) is a comprehensive suite of compilers, libraries, and tools designed specifically for high-performance computing on NVIDIA GPU-accelerated systems. It provides optimized solutions for developing applications that can effectively leverage the computational power of NVIDIA GPUs in the SeaWulf computing environment, supporting C, C++, and Fortran programming languages.

**Module name:** `nvhpc`

## Loading NVHPC

- module: `nvidia/nvhpc/21.5`
- module: `nvidia/nvhpc/21.7`
- module: `nvidia/nvhpc/23.7`
- module: `nvidia/nvhpc/23.11`
- module: `nvidia/nvhpc/24.11`
- module: `nvidia/nvhpc-nompi`
- module: `nvidia/nvhpc-hpcx`
- module: `nvidia/nvhpc-openmpi3`
- module: `nvidia/nvhpc-byo-compiler`
- module: `nvidia/nvhpc-hpcx-cuda11`
- module: `nvidia/nvhpc-hpcx-cuda12`
- module: `nvtop/3.0.1`
- module: `nvtop/3.1.0`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `NVIDIA Nsight Systems`: System-wide performance analysis tool
- `NVIDIA Nsight Compute`: Interactive kernel profiler
- `NVIDIA Debugger (cuda-gdb)`: For debugging GPU applications
- `NVTOP`: Interactive GPU process monitor

## Example usage

**Load NVHPC**

```
module load nvidia/nvhpc/24.11
```

**Compile with NVHPC compilers**

```
nvc myprogram.c -o myprogram
nvc++ myprogram.cpp -o myprogram
nvfortran myprogram.f90 -o myprogram
```

**GPU acceleration with OpenACC and CUDA**

```
nvc -acc -Minfo=accel myprogram.c -o myprogram
nvc -cuda -Minfo=accel mycudaprogram.cu -o mycudaprogram
```

**Optimization and GPU options**

```
nvc -O3 myprogram.c -o myprogram
nvc -acc=gpu -gpu=cc80 myprogram.c -o myprogram
nvc -acc=gpu -gpu=managed myprogram.c -o myprogram
nvc -acc=gpu -gpu=lineinfo myprogram.c -o myprogram
nvc -acc=gpu myprogram.c -o myprogram -lcublas -lcufft
nsys profile ./myprogram
```

**SLURM script example (GPU MPI job)**

```
#!/bin/bash
#SBATCH --job-name=nvhpc_test
#SBATCH --output=nvhpc_test.out
#SBATCH -p a100
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --gres=gpu:2
#SBATCH --time=01:00:00

module load nvidia/nvhpc-hpcx-cuda12/23.11

mpicc -acc=gpu -Minfo=accel mpi_gpu_example.c -o mpi_gpu_example
mpirun -np $SLURM_NTASKS ./mpi_gpu_example
```

## Availability

NVHPC is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Compilers

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/nvhpc> (maintained by Research Computing and Informatics).
