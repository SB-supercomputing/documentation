# Using the ARM compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Ookami users can take advantage of the [ARM Allinea Studio software suite](https://www.arm.com/products/development-tools/server-and-hpc/allinea-studio) that includes a set of compilers, high performance math libraries, and performance profiling tools.

To use the ARM compilers, you must first be on a node with aarch64 CPU architecture. Therefore, users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md)

or

B) ssh to one of the [accessible aarch64 nodes](understanding_login_nodes.md)

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on an appropriate node, load the following module to access the latest Arm compilers:

```
module load arm-modules/version
```

This will add the armclang, armclang++, and armflang executables as well as the arm performance libraries to your $PATH.

Here, we will use an [example matrix multiplication code](https://gitlab.com/arm-hpc/training/arm-sve-tools/-/blob/master/01_Compiler/01_Naive/mm.cpp) to demonstrate the use of the armclang++ compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=arm_example
#SBATCH --output=arm_example.log
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short

# unload any modules currently loaded
module purge

# make the ARM modules available
module load arm-modules/version

# copy the sample C++ code to the working directory
cp /lustre/projects/global/samples/ARM-sample/mm.cpp $SLURM_SUBMIT_DIR

# compile the code using the ARM C++ compiler
armclang++ mm.cpp -o mm

# run the code on an 1000 x 1000 x 1000 matrix
./mm 1000 1000 1000
```

Let's call this script "arm-example.slurm" and submit it with sbatch:

```
sbatch arm-example.slurm
```

Once the job has run, you should see something similar to the following in the job's log file ("arm_example.log"), indicating that the matrix multiplication code has compiled and run sucessfully:

```
Set up of matrices took: 0.182 seconds
Performing multiply
Naive multiply took: 20.884 seconds
```

Example code for testing the ARM compilers can be copied from the following directory:

```
/lustre/projects/global/samples/ARM-sample
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-arm-compilers.php`, retrieved November 5, 2026.
{: .archive-credit }
