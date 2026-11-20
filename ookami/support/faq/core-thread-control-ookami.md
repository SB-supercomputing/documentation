# Using Slurm to manage resources on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

The [Slurm Workload Manager](https://slurm.schedmd.com/documentation.html) provides a variety of ways for users to control how computational resources are managed when running a job on Ookami. This article will discuss Slurm options that can be specified to control resource usage, particularly with MPI and OpenMP.

Several useful flags can be supplied to sbatch/srun/salloc to control job resource usage. These include:

|  |  |
| --- | --- |
| Optional Flag | Behavior |
| --nodes | No. of nodes to use for the job |
| --ntasks | No. of tasks (e.g., commands to run in parallel) to be run |
| --ntasks-per-node | No. of tasks to use per node. Often, this will be the number of  cores available on the compute node. |
| --ntasks-per-core | No. of tasks to use per core |
| --ntasks-per-socket | No. of tasks to run per CPU socket |
| --sockets-per-node | No. of sockets to use (up to 4) per node |
| --threads-per-core | No. of threads to use (e.g., with OpenMP) per core. Using more than  one thread per core may degrade performance and is generally not  recommended. |
| --cpu-bind | Use of this flag allows detailed control of binding tasks  to CPUs. |

These options can be used in combination to control how the workload is spread across separate nodes, and across cores and threads within a single node. This will be illustrated using several "Hello World" examples (please read the Getting Started Guide first). Source code for these examples can be found at:

/lustre/projects/global/samples/HelloWorld

The first example will utilize two compute nodes and execute 1 MPI task per core:

```
#!/usr/bin/env bash

#SBATCH --job-name=onetaskpercore
#SBATCH --output=onetaskpercore.log
#SBATCH --ntasks-per-node=48
#SBATCH -N 2
#SBATCH --time=00:05:00
#SBATCH -p short

module load slurm
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6

# this example will use 1 MPI task per CPU

mpicc /lustre/projects/global/samples/HelloWorld/mpi_hello.c -o mpi_hello

srun ./mpi_hello
```

The above script launches 48 MPI tasks per node and 2 nodes total. The outcome is a Hello World statement from each core across two nodes:

```
Hello world from processor fj003, rank 49 out of 96 processors
Hello world from processor fj002, rank 34 out of 96 processors
Hello world from processor fj003, rank 50 out of 96 processors
...
```

Parallelization can also be accomplished using OpenMP threads on a single node:

```
#!/usr/bin/env bash

#SBATCH --job-name=48openmpthreads
#SBATCH --output=48openmpthreads.log
#SBATCH --ntasks=1
#SBATCH -N 1
#SBATCH --cpus-per-task=48
#SBATCH --time=00:05:00
#SBATCH -p short

module load slurm

# this example will use 1 task and 48 OpenMP threads
omp_threads=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=$omp_threads

gcc -fopenmp /lustre/projects/global/samples/HelloWorld/openMP_hello.c -o openMP_hello

./openMP_hello
```

In the above example, a single node is requested to run 1 task split across 48 cores. The $SLURM_CPUS_PER_TASK environment variable corresponds to the 48 cores per task that we requested and is used to set the OpenMP environment variable that determines how many threads are used. After compiling and running the script, the outcome is a "Hello World" statement from each of the 48 threads run on the node:

```
Hello World... from thread = 0
Hello World... from thread = 41
Hello World... from thread = 42
...
```

Another option is to combine parallelization with MPI and OpenMP across and within nodes:

```
#!/usr/bin/env bash

#SBATCH --job-name=twompiproc
#SBATCH --output=twompiproc.log
#SBATCH --ntasks=2
#SBATCH -N 2
#SBATCH --cpus-per-task=48
#SBATCH --time=00:05:00
#SBATCH -p short

module load slurm
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6

# this example will use 2 MPI tasks spread across two nodes with 48 OpenMP threads per task

# Disable CPU affinity which may degrade performance
export MV2_ENABLE_AFFINITY=0

omp_threads=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=$omp_threads

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

srun ./hybrid_hello
```

This script will launch two MPI tasks--one per node--and then launch 48 OpenMP threads per task. As before, we use the Slurm environment variable $SLURM_CPUS_PER_TASK to control the number of OpenMP threads. In addition, we have set the value of a new environment variable, $MV2_ENABLE_AFFINITY, to zero, which disables CPU affinity and may prevent performance degradation for more complicated tasks.

The result is 96 total "Hellos" from each thread that are spread across 2 processes and two nodes. Each process is contained to a single node:

```
Hello from thread 0 out of 48 from process 0 out of 2 on fj003
Hello from thread 7 out of 48 from process 0 out of 2 on fj003
Hello from thread 8 out of 48 from process 0 out of 2 on fj003
...
Hello from thread 3 out of 48 from process 1 out of 2 on fj004
Hello from thread 2 out of 48 from process 1 out of 2 on fj004
Hello from thread 1 out of 48 from process 1 out of 2 on fj004
```

Advanced users may sometimes want combine MPI and OpenMP but limit processes to stay within each of the 4 physical CPU sockets on each node. One final example illustrates how to do this:

```
#!/usr/bin/env bash

#SBATCH --job-name=onempipersocket
#SBATCH --output=onempipersocketc.log
#SBATCH --sockets-per-node=4
#SBATCH -N 2
#SBATCH --ntasks-per-socket=1
#SBATCH --time=00:05:00
#SBATCH -p short

module load slurm
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6

# this example will use 2 nodes with 1 MPI task per socket and 12 openmp threads per MPI task

# Disable CPU affinity which may degrade performance
export MV2_ENABLE_AFFINITY=0

export OMP_NUM_THREADS=12

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

srun ./hybrid_hello
```

Here, we have requested 2 nodes, with 1 task per socket. We have also requested all 4 sockets per node. This time we set $OMP_NUM_THREADS manually to 12 in order to split core usage evenly across the 4 sockets.

The outcome is once again 96 "Hellos", but this time they are spread across 4 processes per node, with 12 threads per process:

```
Hello from thread 3 out of 12 from process 0 out of 8 on fj002
...
Hello from thread 0 out of 12 from process 1 out of 8 on fj002
...
Hello from thread 1 out of 12 from process 2 out of 8 on fj002
...
Hello from thread 1 out of 12 from process 3 out of 8 on fj002
...
Hello from thread 7 out of 12 from process 4 out of 8 on fj003
...
Hello from thread 6 out of 12 from process 5 out of 8 on fj003
...
Hello from thread 9 out of 12 from process 6 out of 8 on fj003
...
Hello from thread 0 out of 12 from process 7 out of 8 on fj003
...
```

Hopefully it is clear from these examples that users can exert relatively fine-grained control over nodes, CPUs and threads on Ookami using Slurm. Please note that there are multiple ways to accomplish the same task, and the examples above just illustrate one particular route.

While these examples show how to control behavior on a per-job basis, users may also pass most of the same flags to "srun" within the script in order to exert additional control on a per-task basis. The srun flag "--cpu-binding" can also allows fine-grained control of CPUs used in the tasks called by srun. Please see this [detailed discussion](https://slurm.schedmd.com/mc_support.html) for more information and additional options.

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/core-thread-control-ookami.php`, retrieved November 5, 2026.
{: .archive-credit }
