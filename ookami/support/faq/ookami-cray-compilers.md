# Using the Cray compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Ookami users can take advantage of the [Cray Programming Environment](https://pubs.cray.com/bundle/HPE_Cray_Programming_Environment_User_Guide_For_Apollo_80_ARM_2009_S8011_Apollo80/page/About_Cray_Programming_Environment_User_Guide.html) that includes a set of compilers, high performance math libraries, and performance profiling tools.

To use the Cray compilers, you must first be on a node with aarch64 CPU architecture. Therefore, users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md)

or

B) ssh to one of the [accessible aarch64 nodes](understanding_login_nodes.md)

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on an appropriate node, load the following module to access the Cray compilers:

```
module load CPE
```

This is a meta-module that loads several different modules needed for accessing the Cray Programming Environment. Loading it will add the c ("cc"), c++ ("CC"), and fortran ("ftn") compiler executables to your PATH.

Here, we will use an [example matrix multiplication code](https://gitlab.com/arm-hpc/training/arm-sve-tools/-/blob/master/01_Compiler/01_Naive/mm.cpp) to demonstrate the use of the Cray c++ compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=cray_example
#SBATCH --output=cray_example.log
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short

# unload any modules currently loaded
module purge

# load the CPE module to setup the cray programming environment
module load CPE

# copy the sample C++ code to the working directory
cp /lustre/projects/global/samples/Cray-sample/mm.cpp $SLURM_SUBMIT_DIR

# compile the code using the Cray C++ compiler
CC mm.cpp -o mm

# run the code on a 1000 x 1000 x 1000 matrix
./mm 1000 1000 1000
```

Let's call this script "cray-example.slurm" and submit it with sbatch:

```
sbatch cray-example.slurm
```

Once the job has run, you should see something similar to the following in the job's log file ("cray_example.log"), indicating that the matrix multiplication code has compiled and run sucessfully:

```
Set up of matrices took: 0.151 seconds
Performing multiply
Naive multiply took: 5.939 seconds
```

Example code for testing the Cray compilers can be copied from the following directory:

```
/lustre/projects/global/samples/Cray-sample
```

---

In case you want to use Cray and the mvapich module, load them in seperate commands and in the right order

```
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6
```

The mvapich module picks up environment variables set by CPE, so if you run everthing in one module load command, this doesn't work.

If you prefer to use a version of mvapich without SVE support, you should load the following modules instead:

```
module load CPE-nosve
module load cray-mvapich2_nogpu/2.3.6
```

To see the Cray manpages use

```
man crayftn
man craycc
man crayCC
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-cray-compilers.php`, retrieved November 5, 2026.
{: .archive-credit }
