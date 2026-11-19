# Using the NVIDIA HPC SDK compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

**Note: currently Ookami doe not offer GPUs**

Ookami users can take advantage of the [NVIDIA HPC Software Development Kit (SDK)](https://developer.nvidia.com/hpc-sdk), which includes a set of compilers, performance tools, and math and communications libraries for developing GPU-accelerated applications.

Currently, Ookami users should run their GPU-related tasks on the fj-epyc node, which contains two Tesla V100 GPUs.

Therefore, to make use of NVIDIA HPC SDK users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md) and request the milan-64core partition

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on the appropriate node, there are several different sets of modules that can be chosen, depending on the version of CUDA desired. For CUDA 11.0, load one of the following

```
# Full set of Nvidia compilers, libraries, CUDA 11.0, and MPI
nvidia/cuda11.0/nvhpc/21.5

# Nvidia libraries, CUDA, and MPI but without the complete compiler suite (BYO compilers)
nvidia/cuda11.0/nvhpc-byo-compiler/21.5

# Nvidia compilers, libraries abd CUDA but without MPI
nvidia/cuda11.0/nvhpc-nompi/21.5
```

A similar set of modules can also be chosen for CUDA 10.2 and 11.3 by replacing "11.0" in the module name with the appropriate version number.

Let's load the standard module for CUDA 11.0:

```
module load nvidia/cuda11.0/nvhpc/21.5
```

This will add several compilers, including nvc, nvcc, nvfortran, and nvc++, along with compatible MPI compilers and runtime executables to the PATH.

Next, we will use a [hydrodynamics mini-app that solves compressible Euler equations in 2D](https://github.com/UK-MAC/CloverLeaf_OpenACC) to demonstrate the use of the GPU-accelerated nvfortran compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=nvhpc_example
#SBATCH --output=nvhpc_example.log
#SBATCH --ntasks-per-node=64
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p milan-64core

# unload any modules currently loaded
module purge

# load the nvhpc module
module load nvidia/cuda11.0/nvhpc/21.5

# copy the sample directory with the CloverLeaf mini-app code to the working directory
cp -r /lustre/projects/global/samples/CloverLeaf_OpenACC $SLURM_SUBMIT_DIR

# change to the newly copied directory
cd CloverLeaf_OpenACC

# compile the code
make COMPILER=PGI MPI_COMPILER=mpif90

# set environment variable to get information about the GPU usage printed to the log
NV_ACC_NOTIFY=1

# run the code on a single GPU with one thread
OMP_NUM_THREADS=1 mpirun -np 1 ./clover_leaf
```

Let's call this script "nvhpc-example.slurm" and submit it with sbatch:

```
sbatch nvhpc-example.slurm
```

Once the job has run, you should see voluminous compilation and runtime information in the job's log file ("nvhpc_example.log"). The end of the log file should contain something similar to the following, indicating that the test was successful:

```
Test problem   2 is within   0.1170175E-10% of the expected solution
 This test is considered PASSED
 Wall clock    0.3163411617279053
 First step overhead   1.9407272338867188E-004
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-nvidia-compilers.php`, retrieved November 5, 2026.
{: .archive-credit }
