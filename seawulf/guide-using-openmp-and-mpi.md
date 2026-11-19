# Guide to using OpenMP and MPI

When tasks need to coordinate, unlike [embarrassingly parallel workflows](guide-embarrassingly-parallel-workflows.md), you parallelize with threads and message passing. Three approaches on SeaWulf: **OpenMP** (multi-threading on a single node’s shared memory), **MPI** (message passing across nodes), and **hybrid** (MPI between nodes + OpenMP within them). All examples below live in `/gpfs/projects/samples/pi` on SeaWulf.

## The serial baseline

A pi-by-series calculation in C (~4.2 s serial):

```
#include <stdio.h>
#include <time.h>

#define NPTS 1000000000

void main() {
   int i;
   double a,b,c,pi,dt,mflops;
   struct timespec tstart,tend;
   clock_gettime(CLOCK_REALTIME,&tstart);
   a = 0.5;  b = 0.75;  c = 0.25;  pi = 0;
   for (i = 1; i <= NPTS; ++i)
      pi += a/((i-b)*(i-c));
   clock_gettime(CLOCK_REALTIME,&tend);
   dt = (tend.tv_sec+tend.tv_nsec/1e9)-(tstart.tv_sec+tstart.tv_nsec/1e9);
   mflops = NPTS*5.0/(dt*1e6);
   printf("NPTS = %d, pi = %f\n",NPTS,pi);
   printf("time = %f, estimated MFlops = %f\n",dt,mflops);
}
```

```
#!/usr/bin/env bash
#SBATCH --job-name=serial_pi
#SBATCH --output=serial_pi.log
#SBATCH --nodes=1
#SBATCH --time=05:00
#SBATCH -p short-28core

module load gcc/12.1.0
gcc /gpfs/projects/samples/pi/pi.c -o pi -lm
./pi
```

## OpenMP: parallelize one node

One pragma parallelizes the loop across threads; `OMP_NUM_THREADS` sets the thread count and `-fopenmp` enables it at compile time:

```
#pragma omp parallel for reduction(+:pi)
for (i = 1; i <= NPTS; ++i)
   pi += a/((i-b)*(i-c));
```

```
#!/usr/bin/env bash
#SBATCH --job-name=openmp_pi
#SBATCH --output=openmp_pi.log
#SBATCH --time=05:00
#SBATCH -p short-28core

module load gcc/12.1.0
export OMP_NUM_THREADS=28
gcc /gpfs/projects/samples/pi/openmp_pi.c -o openmp_pi -fopenmp
./openmp_pi
```

Runtime drops to ~0.38 s with 28 threads: an order of magnitude. Match threads to the node’s core count as a starting point, but benchmark: most codes do not scale well to ever more threads.

## MPI: parallelize across nodes

MPI splits the work across ranks (processes) that pass messages. The core pattern: each rank computes a slice, then a reduce collects the answer:

```
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &nproc);

/* each rank sums its own slice of the series... */
istart = 1 + NPTS*((rank+0.0)/nproc);
iend = NPTS*((rank+1.0)/nproc);
sum = 0.0;
for (i = istart; i <= iend; ++i)
   sum += 0.5/((i-0.75)*(i-0.25));

/* ...and rank 0 collects the total */
MPI_Reduce(&sum,&pi,1,MPI_DOUBLE,MPI_SUM,0,MPI_COMM_WORLD);
MPI_Finalize();
```

```
#!/usr/bin/env bash
#SBATCH --job-name=mpi_pi
#SBATCH --output=mpi_pi.log
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=28
#SBATCH --time=05:00
#SBATCH -p short-28core

module load mvapich2/gcc12.1/2.3.7
export MV2_HOMOGENEOUS_CLUSTER=1
export MV2_ENABLE_AFFINITY=0
mpicc /gpfs/projects/samples/pi/mpi_pi.c -o mpi_pi
mpirun ./mpi_pi
```

- SeaWulf offers several MPI stacks: Mvapich, Intel MPI, and OpenMPI, in multiple compiler flavors. None loads by default: `module load mvapich2/gcc12.1/2.3.7` (or equivalent) first.
- Compiler wrappers: `mpicc` (C), `mpicxx` (C++), `mpif90` (Fortran). Python (mpi4py) and R (Rmpi) work too.
- `--ntasks-per-node=28` gives one rank per core. Only request multiple nodes when you are actually using MPI.
- 2 nodes / 56 ranks ≈ 0.156 s; 4 nodes ≈ 0.092 s: sublinear, because inter-node communication costs grow with scale.

## Hybrid OpenMP + MPI

One MPI rank per node, with OpenMP threads using all its cores: often the most memory-efficient shape for large applications:

```
#!/usr/bin/env bash
#SBATCH --job-name=hybrid_pi
#SBATCH --output=hybrid_pi.log
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH --time=05:00
#SBATCH -p short-28core

module load mvapich2/gcc12.1/2.3.7
export MV2_HOMOGENEOUS_CLUSTER=1
export MV2_ENABLE_AFFINITY=0
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
mpicc /gpfs/projects/samples/pi/hybrid_pi.c -o hybrid_pi -fopenmp
mpirun ./hybrid_pi
```

Compile with the MPI wrapper *and* `-fopenmp`. Reducing MPI ranks in favor of threads uses shared memory more efficiently, though for this simple pi benchmark, pure MPI actually wins (~2.08 s hybrid). The moral: **benchmark your own application**; the right shape is workload-specific.

> [!NOTE]
> **Need help choosing?** The Computational Science team can help you profile and pick a parallelization strategy: [open a ticket](https://rci.stonybrook.edu/hpc/support).

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/guide-using-openmp-and-mpi> (maintained by Research Computing and Informatics).
