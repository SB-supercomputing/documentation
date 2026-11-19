# Using the Fujitsu compilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Ookami users can take advantage of the Fujitsu compiler software package.

To use the Fujitsu compilers, you must first be on a node with aarch64 CPU architecture. Therefore, users should first either:

A) start an [interactive Slurm job](interactive_slurm_session.md)

or

B) ssh to one of the [accessible aarch64 nodes](understanding_login_nodes.md)

or

C) Alternatively, if no interactive session is desired, users may simply write and submit a [Slurm job submission script](example-slurm-script.md) to compile the code.

Once on an appropriate node, load the following module:

```
module load fujitsu/compiler/1.0.20
```

This will add the fcc (C), FCC (C++), and frt (Fortran) compiler executables to your PATH.

Here, we will use an [example matrix multiplication code](https://gitlab.com/arm-hpc/training/arm-sve-tools/-/blob/master/01_Compiler/01_Naive/mm.cpp) to demonstrate the use of the FCC compiler. Because this code compiles without issue and does not require any interactive troubleshooting, we can write a Slurm script to compile and run the code:

```
#!/usr/bin/env bash

#SBATCH --job-name=FCC_example
#SBATCH --output=FCC_example.log
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short

# unload any modules currently loaded
module purge

# load the Fujitsu module
module load fujitsu/compiler/1.0.20

# copy the sample C++ code to the working directory
cp /lustre/projects/global/samples/ARM-sample/mm.cpp $SLURM_SUBMIT_DIR

# compile the code using the g++ compiler
FCC mm.cpp -o mm

# run the code on an 1000 x 1000 x 1000 matrix
./mm 1000 1000 1000
```

Let's call this script "fujitsu-example.slurm" and submit it with sbatch (make sure that the slurm module is loaded first):

```
sbatch fujitsu-example.slurm
```

Once the job has run, you should see something similar to the following in the job's log file ("FCC_example.log"), indicating that the matrix multiplication code has compiled and run sucessfully:

```
Set up of matrices took: 0.199 seconds
Performing multiply
Naive multiply took: 36.997 seconds
```

The Fujitsu compiler software package also includes its own version of OpenMPI. Loading the fujitsu/compiler/1.0.20 module to access the mpifcc (C), mpiFCC (C++), and mpifrt (Fortran) MPI compiler executables.

In the following example, will we use the Fujitsu implementation of MPI to compile and run a simple MPI "hello world" code:

```
#!/usr/bin/env bash

#SBATCH --job-name=fuj_mpi_hello
#SBATCH --output=fuj_mpi_hello.log
#SBATCH --ntasks-per-node=48
#SBATCH -N 4
#SBATCH --time=00:05:00
#SBATCH -p short

# unload any modules currently loaded
module purge

# load the Fujitsu module
module load fujitsu/compiler/1.0.20

# copy the sample C code to the working directory
cp /lustre/projects/global/samples/HelloWorld/mpi_hello.c $SLURM_SUBMIT_DIR

# compile the code using the mpifcc compiler
mpifcc mpi_hello.c -o mpi_hello

# run the code with mpiexec
mpiexec ./mpi_hello
```

Let's call this Slurm script "fuj_mpi_hello.slurm" and run it with the following command:

```
sbatch fuj_mpi_hello.slurm
```

In this case, we ran 48 "hello world" tasks from each of 4 nodes, so the output will look something like the following:

```
Hello world from processor fj171, rank 191 out of 192 processors
Hello world from processor fj169, rank 63 out of 192 processors
Hello world from processor fj170, rank 127 out of 192 processors
Hello world from processor fj168, rank 31 out of 192 processors
Hello world from processor fj168, rank 15 out of 192 processors
Hello world from processor fj169, rank 95 out of 192 processors
Hello world from processor fj171, rank 159 out of 192 processors
Hello world from processor fj168, rank 47 out of 192 processors
Hello world from processor fj168, rank 42 out of 192 processors
Hello world from processor fj171, rank 175 out of 192 processors
Hello world from processor fj171, rank 170 out of 192 processors
...
```

Example code for testing the Fujitsu compilers can be found copied from:

```
/lustre/projects/global/samples/Fujitsu
```

---

**NOTE:**

The environment variable  **XOS_MMM_L_PAGING_POLICY**  can have huge impact on your code's performance. You can read more about it in the documentation, which can be found in

```
/opt/FJSVstclanga/cp-1.0.20.06/manual/english/
```

Note that there is a seperate documentation document for each language.

As a general advise:
 If your code is sequential, just run it.
If your code is threaded, set the variable to demand:demand:demand.

Archived from the Internet Archive's copy of `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami-fujitsu-compilers.php`, saved September 28, 2021.
{: .archive-credit }
