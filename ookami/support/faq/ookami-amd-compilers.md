# Using the AMD compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Ookami users can take advantage of the [AMD Optimizing C/C++ Compiler (AOCC)](https://developer.amd.com/amd-aocc/#download) software suite that includes a set of compilers and debuggers tuned and optimzed for the AMD EPYC architecture.

While the AMD compilers should work on any Ookami x86_64 node, we recommend specifically using it on the fj-epyc node, as it contains the architecture for which AOCC is optimized. Therefore, users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md) and request the milan-64core partition

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on an appropriate node, load the following module:

```
module load aocc/3.0.0
```

This will add the clang, clang++, and flang executables (among others) to your $PATH.

Here, we will use an [example matrix multiplication code](https://gitlab.com/arm-hpc/training/arm-sve-tools/-/blob/master/01_Compiler/01_Naive/mm.cpp) to demonstrate the use of the clang++ compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=amd_example
#SBATCH --output=amd_example.log
#SBATCH --ntasks-per-node=64
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p milan-64core

# unload any modules currently loaded
module purge

# load the AOCC module
module load aocc/3.0.0

# copy the sample C++ code to the working directory
cp /lustre/projects/global/samples/ARM-sample/mm.cpp $SLURM_SUBMIT_DIR

# compile the code using the AMD clang++ compiler
clang++ mm.cpp -o mm

# run the code on an 1000 x 1000 x 1000 matrix
./mm 1000 1000 1000
```

Let's call this script "amd-example.slurm" and submit it with sbatch:

```
sbatch amd-example.slurm
```

Once the job has run, you should see something similar to the following in the job's log file ("amd_example.log"), indicating that the matrix multiplication code has compiled and run sucessfully:

```
Set up of matrices took: 0.020 seconds
Performing multiply
Naive multiply took: 3.312 seconds
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-amd-compilers.php`, retrieved November 5, 2026.
{: .archive-credit }
