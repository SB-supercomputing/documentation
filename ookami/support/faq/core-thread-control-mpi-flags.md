# Using MPI options to manage resources on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

While [Slurm provides options for managing thread and CPU resources](core-thread-control-ookami.md), some Ookami users may wish to exert additional control over resources using MPI-specific flags. This article will discuss some useful options available for OpenMPI and MVAPICH.

### OpenMPI

OpenMPI provides several optional flags that are useful for flexibly assigning resources and determining how processes are mapped to CPUs. Of particular note, the "--map-by" option allows the user to map processes in a variety of diferrent ways.

Arguments supplied to the "--map-by" flag typically have the following syntax:

```
--map-by ppr:x:<object>:pe=n
```

Here, **ppr** stands for "processes per resource" and **x** indcates the number of processes to be assigned. The **object** is the resource that processes will be mapped to and can take many forms, including node, core, socket, numa, or hwthread. Additionally, **pe** is the "processing element" (e.g., OpenMP thread), and **n** indicates how many such elements will be generated per process.

Another option that is useful for investigating how job resources are bound is the "--report-bindings" flag that can be provided to "mpiexec". This flag will report how each MPI_COMM_WORLD (MCW) rank is assigned to the specified resources.

A few "Hello World" examples will illustrate how these options can be set to manage resources. Source code for "Hello World" examples can be found at:

```
/lustre/projects/global/samples/HelloWorld
```

The first example will use 1 Node, 1 process, and 48 threads:

```
#!/usr/bin/env bash

#SBATCH --job-name=test_openmpi
#SBATCH --output=test_openmpi.log
#SBATCH -N 1
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=48
#SBATCH -p short

# specify message size threshold for using the UCX Rendevous Protocol
export UCX_RNDV_THRESH=65536

# use high-performance rc and xpmem transports where possible
export UCX_TLS=rc,xpmem

# control how much information about the transports is printed to log
export UCX_LOG_LEVEL=info

module load slurm
module load openmpi/gcc8/4.1.2

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

mpiexec --map-by ppr:1:node:pe=48 --report-bindings ./hybrid_hello
```

In the above, we have compiled a "Hello World" code with **mpicc**, and then executed it with **mpiexec**. The UCX environment variables that are set will control which transports are used and how much information about the transports is printed. Please see [here](https://ucx-py.readthedocs.io/en/latest/configuration.html) for more information about the UCX variables.

Importantly, the **--map-by** statement binds 1 process to a single node, with 48 thread per process.

The **--report-bindings** flag produces output to show what node, core, and thread each MCW was mapped to:

```
[fj131:21758] MCW rank 0 is not bound (or bound to all available processors)
```

In the output we see that there are 48 total "Hello World" statements printed, all from different threads of the same process:

```
Hello from thread 43 out of 48 from process 0 out of 1 on fj131
Hello from thread 5 out of 48 from process 0 out of 1 on fj131
Hello from thread 12 out of 48 from process 0 out of 1 on fj131
Hello from thread 17 out of 48 from process 0 out of 1 on fj131
Hello from thread 25 out of 48 from process 0 out of 1 on fj131
...
(output truncated)
```

Now, let's modify this example to use 2 nodes, 4 processes per node, and 2 OpenMP threads per process:

```
#!/usr/bin/env bash

#SBATCH --job-name=test_openmpi
#SBATCH --output=test_openmpi.log
#SBATCH -N 2
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=2
#SBATCH -p short

# specify message size threshold for using the UCX Rendevous Protocol
export UCX_RNDV_THRESH=65536

# use high-performance rc and xpmem transports where possible
export UCX_TLS=rc,xpmem

# control how much information about the transports is printed to log
export UCX_LOG_LEVEL=info

module load slurm
module load openmpi/gcc8/4.1.2

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

mpiexec --map-by ppr:4:node:pe=2 --report-bindings ./hybrid_hello
```

In this case, we have used an Sbatch flag to set 2 CPUs per task, changed the value of **ppr** to 4 and changed the **pe** value to 2 in the **--map-by** flag. The output shows expected 8 total ranks/processes spread across two nodes, with two threads per rank:

```
[fj126:27130] MCW rank 3 bound to socket 0[core 6[hwt 0]], socket 0[core 7[hwt 0]]:
[././././././B/B/./././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj126:27130] MCW rank 0 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]]:
[B/B/./././././././././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj126:27130] MCW rank 1 bound to socket 0[core 2[hwt 0]], socket 0[core 3[hwt 0]]:
[././B/B/./././././././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj126:27130] MCW rank 2 bound to socket 0[core 4[hwt 0]], socket 0[core 5[hwt 0]]:
[././././B/B/./././././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj127:20627] MCW rank 6 bound to socket 0[core 4[hwt 0]], socket 0[core 5[hwt 0]]:
[././././B/B/./././././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj127:20627] MCW rank 7 bound to socket 0[core 6[hwt 0]], socket 0[core 7[hwt 0]]:
[././././././B/B/./././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj127:20627] MCW rank 4 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]]:
[B/B/./././././././././.][./././././././././././.][./././././././././././.][./././././././././././.]
[fj127:20627] MCW rank 5 bound to socket 0[core 2[hwt 0]], socket 0[core 3[hwt 0]]:
[././B/B/./././././././.][./././././././././././.][./././././././././././.][./././././././././././.]
Hello from thread 0 out of 2 from process 0 out of 8 on fj126
Hello from thread 1 out of 2 from process 0 out of 8 on fj126
Hello from thread 0 out of 2 from process 1 out of 8 on fj126
Hello from thread 1 out of 2 from process 1 out of 8 on fj126
Hello from thread 1 out of 2 from process 2 out of 8 on fj126
Hello from thread 0 out of 2 from process 2 out of 8 on fj126
Hello from thread 0 out of 2 from process 5 out of 8 on fj127
Hello from thread 1 out of 2 from process 5 out of 8 on fj127
Hello from thread 0 out of 2 from process 6 out of 8 on fj127
Hello from thread 1 out of 2 from process 6 out of 8 on fj127
Hello from thread 0 out of 2 from process 3 out of 8 on fj126
Hello from thread 1 out of 2 from process 3 out of 8 on fj126
Hello from thread 0 out of 2 from process 7 out of 8 on fj127
Hello from thread 1 out of 2 from process 7 out of 8 on fj127
Hello from thread 0 out of 2 from process 4 out of 8 on fj127
Hello from thread 1 out of 2 from process 4 out of 8 on fj127
```

In some cases, it may be useful to allocate processes based on [numa or core memory groups (CMG)](https://en.wikipedia.org/wiki/Non-uniform_memory_access) to improve efficiency:

```
#!/usr/bin/env bash

#SBATCH --job-name=test_openmpi
#SBATCH --output=test_openmpi.log
#SBATCH -N 2
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=4
#SBATCH -p short

# specify message size threshold for using the UCX Rendevous Protocol
export UCX_RNDV_THRESH=65536

# use high-performance rc and xpmem transports where possible
export UCX_TLS=rc,xpmem

# control how much information about the transports is printed to log
export UCX_LOG_LEVEL=info

module load slurm
module load openmpi/gcc8/4.1.2

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

mpiexec --map-by ppr:1:numa:pe=4 --report-bindings ./hybrid_hello
```

In the above example, we have changed the mapping object from **node** to **numa**, and we are launching 1 process per numa, each with four threads.

The result, once again, is 8 total processes spread across the two nodes:

```
...
Hello from thread 3 out of 4 from process 0 out of 8 on fj127
Hello from thread 2 out of 4 from process 0 out of 8 on fj127
Hello from thread 0 out of 4 from process 1 out of 8 on fj127
Hello from thread 2 out of 4 from process 7 out of 8 on fj128
Hello from thread 0 out of 4 from process 7 out of 8 on fj128
Hello from thread 2 out of 4 from process 6 out of 8 on fj128
...
```

But the way that the MCW ranks have been allocated is now quite different:

```
[fj127:25164] MCW rank 1 bound to socket 1[core 12[hwt 0]], socket 1[core 13[hwt 0]], socket 1[core 14[hwt 0]], socket 1[core 15[hwt 0]]: 
[./././././././././././.][B/B/B/B/./././././././.][./././././././././././.][./././././././././././.]
[fj127:25164] MCW rank 2 bound to socket 2[core 24[hwt 0]], socket 2[core 25[hwt 0]], socket 2[core 26[hwt 0]], socket 2[core 27[hwt 0]]:
[./././././././././././.][./././././././././././.][B/B/B/B/./././././././.][./././././././././././.]
[fj128:25248] MCW rank 6 bound to socket 2[core 24[hwt 0]], socket 2[core 25[hwt 0]], socket 2[core 26[hwt 0]], socket 2[core 27[hwt 0]]:
[./././././././././././.][./././././././././././.][B/B/B/B/./././././././.][./././././././././././.]
[fj128:25248] MCW rank 5 bound to socket 1[core 12[hwt 0]], socket 1[core 13[hwt 0]], socket 1[core 14[hwt 0]], socket 1[core 15[hwt 0]]:
[./././././././././././.][B/B/B/B/./././././././.][./././././././././././.][./././././././././././.]

...

(truncated for clarity)
```

Unlike our previous examples, each MCW rank is now bound to a separate numa/CMG (referred to as sockets), and there are 4 threads spread across each numa/CMG.

Finally, let's run an example involving several nodes, with 1 process per numa/CMG of the node and each process using all 12 cores available to that socket:

```
#!/usr/bin/env bash

#SBATCH --job-name=test_openmpi
#SBATCH --output=test_openmpi.log
#SBATCH -N 8
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=12
#SBATCH -p short

# specify message size threshold for using the UCX Rendevous Protocol
export UCX_RNDV_THRESH=65536

# use high-performance rc  and xpmem transports where possible
export UCX_TLS=rc,xpmem

# control how much information about the transports is printed to log
export UCX_LOG_LEVEL=info

module load slurm
module load openmpi/gcc8/4.1.2

mpicc -fopenmp /lustre/projects/global/samples/HelloWorld/hybrid_hello.c -o hybrid_hello

mpiexec --map-by ppr:1:numa:pe=12 --report-bindings ./hybrid_hello
```

In this case, 32 processes--each with 12 threads--have been generated across 8 nodes:

```
...
Hello from thread 11 out of 12 from process 4 out of 32 on fj128
Hello from thread 6 out of 12 from process 16 out of 32 on fj131
...
```

Each MCW rank has used all the CPUs within a given numa/CMG. For example, here are the reported bindings for one MCW rank:

```
[fj127:28077] MCW rank 0 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]], socket 0[core 2[hwt 0]], socket 0[core 3[hwt 0]],
socket 0[core 4[hwt 0]], socket 0[core 5[hwt 0]], socket 0[core 6[hwt 0]], socket 0[core 7[hwt 0]],
socket 0[core 8[hwt 0]], socket 0[core 9[hwt 0]], socket 0[core 10[hwt 0]], socket 0[core 11[hwt 0]]:
[B/B/B/B/B/B/B/B/B/B/B/B][./././././././././././.][./././././././././././.][./././././././././././.]
```

In this case, we can see that the 12 threads for MCW rank 0 are all found within a single numa/CMG. Each process was confined to a single numa/CMG, which may help increase the efficiency of the work.

Many other CPU-mapping configurations are possible. Please see the [OpenMPI documentation](https://www.open-mpi.org/doc/v4.0/man1/mpiexec.1.php) for additional details.

### MVAPICH2

The following example demonstrates how to run a simple MPI job using the Mvapich2 implementation of MPI.

Note that on Ookami, Mvapich2 has been compiled with explicit Slurm support. This means that MPI jobs should be launched using the "srun" command instead of the more typical "mpirun" or "mpiexec" commands:

```
#!/usr/bin/env bash

#SBATCH --job-name=gccmpitest
#SBATCH --output=gcc_mpi_hello.log
#SBATCH --ntasks-per-node=48
#SBATCH -N 4
#SBATCH --time=00:05:00
#SBATCH -p short

# load slurm and mvapich2 compiled with gcc 8
module load slurm
module load  mvapich2/gcc8/2.3.5

# compile the hello world code with the MPI compiler
mpicc /lustre/projects/global/samples/HelloWorld/mpi_hello.c -o mpi_hello

# launch the MPI job with srun instead of mpirun or mpiexec
srun ./mpi_hello
```

In this case, we are creating a total of 192 "hello world" processes spread across 4 nodes. The output will look similar to the following:

```
Hello world from processor fj005, rank 145 out of 192 processors
Hello world from processor fj003, rank 82 out of 192 processors
Hello world from processor fj003, rank 83 out of 192 processors
Hello world from processor fj002, rank 1 out of 192 processors
Hello world from processor fj003, rank 49 out of 192 processors
Hello world from processor fj002, rank 34 out of 192 processors
Hello world from processor fj002, rank 2 out of 192 processors
...
```

*More examples coming soon...*

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/core-thread-control-mpi-flags.php`, retrieved November 5, 2026.
{: .archive-credit }
