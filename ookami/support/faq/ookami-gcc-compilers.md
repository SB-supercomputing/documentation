# Using the GCC compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Ookami users can take advantage of multiple versions of the GNU Compiler Collection (GCC) on Ookami.

To use the gcc compilers, you must first be on a node with aarch64 CPU architecture. Therefore, users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md)

or

B) ssh to one of the [accessible aarch64 nodes](understanding_login_nodes.md)

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on an appropriate node, multiple gcc versions are available.

gcc version 8.3.1 is the system default version of gcc and is available without loading any modules. If desired, a newer version may be accessed via a module:

```
module load gcc/11.2.0
```

This will add the gcc, g++, and gfortran compiler executables to your PATH.

Here, we will use an [example matrix multiplication code](https://gitlab.com/arm-hpc/training/arm-sve-tools/-/blob/master/01_Compiler/01_Naive/mm.cpp) to demonstrate the use of the g++ compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=gcc_example
#SBATCH --output=gcc_example.log
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short

# unload any modules currently loaded
module purge

# load the gcc 11 module
module load gcc/11.2.0

# copy the sample C++ code to the working directory
cp /lustre/projects/global/samples/ARM-sample/mm.cpp $SLURM_SUBMIT_DIR

# compile the code using the g++ compiler
g++ mm.cpp -o mm

# run the code on an 1000 x 1000 x 1000 matrix
./mm 1000 1000 1000
```

Let's call this script "gcc-example.slurm" and submit it with sbatch:

```
sbatch gcc-example.slurm
```

Once the job has run, you should see something similar to the following in the job's log file ("gcc_example.log"), indicating that the matrix multiplication code has compiled and run sucessfully:

```
Set up of matrices took: 0.173 seconds
Performing multiply
Naive multiply took: 28.013 seconds
```

Example code for testing the GCC compilers can be found copied from:

```
/lustre/projects/global/samples/gcc-sample
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-gcc-compilers.php`, retrieved November 5, 2026.
{: .archive-credit }
