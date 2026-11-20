# this FAQ section is currently under development

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

## Thread Binding

Ookami users may wish to exercise control over how threads for their jobs are bound. This article will discuss some OpenMP examples that offer various options for thread binding.

Two particular environment variables may be used to control thread affinity for OpenMP jobs:

[OMP_PROC_BIND](https://www.openmp.org/spec-html/5.0/openmpse52.html): controls whether and how threads are bound. Possible values include

| **Value** | **Behavior** |
| --- | --- |
| true | enable binding a thread (default) |
| false | disable thread binding |
| master | bind thread to same place as the parent thread |
| close | place threads as close as possible to the parent thread |
| spread | spread threads out as much as possible within the processor |

[OMP_PLACES](https://www.openmp.org/spec-html/5.0/openmpse53.html): describes the places where threads may be bound. Possible values include:

| **Value** | **Behavior** |
| --- | --- |
| threads | each place is a hardware thread |
| cores | each place is a single CPU |
| sockets | each place is a single socket (on Ookami this will be a NUMA node, not a socket) |
| &lt; custom > | Manually specified place intervals with the syntax: &lt;starting place location>:&lt;number of places>:&lt;size of stride> |

While testing thread-binding behavior, it may be useful to set one or more of the following environment variables:

```
 # turns on display of OMP's internal control variables
export OMP_DISPLAY_ENV=true

# display the affinity of each OMP thread
export OMP_DISPLAY_AFFINITY=true

# controls the format of the thread affinityexport
OMP_AFFINITY_FORMAT="Thread Affinity: %0.3L %.8n %.15{thread_affinity} %.12H"
```

The following "Hello World" examples will illustrate thread binding behavior under a few different scenarios.

First, let's try binding each thread to a core:

```
 #!/bin/sh

#SBATCH --partition=short
#SBATCH --job-name=omp_hello_cores
#SBATCH --output=omp_hello_cores.log
#SBATCH --nodes=1 
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=8 ### 48 threads (cores) per rank (node)
#SBATCH --time=1:00:00

#set up the environment--------------
module load slurm

# specify number of OMP threads
export OMP_NUM_THREADS=32

# enable thread binding and print out info on thread affinity
export OMP_DISPLAY_ENV=true
export OMP_DISPLAY_AFFINITY=true
export OMP_AFFINITY_FORMAT="Thread Affinity: %0.3L %.8n %.15{thread_affinity} %.12H"
export OMP_PROC_BIND=true

#Compiling OMP Hello World-----------
gcc -o hello-omp -fopenmp /lustre/projects/global/samples/HelloWorld/hello-omp.c

#Running------------------------------
#bind each thread to a core
export OMP_PLACES=cores

./hello-omp
```

In this case, we're running a single node job with 4 tasks, and 8 cores per task (32 threads total). The top of the log file shows information regarding our OMP settings:

```
   OPENMP DISPLAY ENVIRONMENT BEGIN
  _OPENMP = '201511'
  OMP_DYNAMIC = 'FALSE'
  OMP_NESTED = 'FALSE'
  OMP_NUM_THREADS = '32'
  OMP_SCHEDULE = 'DYNAMIC'
  OMP_PROC_BIND = 'TRUE'
  OMP_PLACES = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},
{16},{17},{18},{19},{20},{21},{22},{23},{24},{25},{26},{27},{28},{29},{30},{31},{32},
{33},{34},{35},{36},{37},{38},{39},{40},{41},{42},{43},{44},{45},{46},{47}'
  OMP_STACKSIZE = '0'
  OMP_WAIT_POLICY = 'PASSIVE'
  OMP_THREAD_LIMIT = '4294967295'
  OMP_MAX_ACTIVE_LEVELS = '2147483647'
  OMP_CANCELLATION = 'FALSE'
  OMP_DEFAULT_DEVICE = '0'
  OMP_MAX_TASK_PRIORITY = '0'
  OMP_DISPLAY_AFFINITY = 'TRUE'
  OMP_AFFINITY_FORMAT = 'Thread Affinity: %0.3L %.8n %.15{thread_affinity} %.12H'
OPENMP DISPLAY ENVIRONMENT END
```

Note that each OMP place has been bound to a single core. Next we get information about each threads affinity:

```
 Thread Affinity: 001        0               0        fj030
Thread Affinity: 001        1               1        fj030
Thread Affinity: 001        2               2        fj030
Thread Affinity: 001        3               3        fj030
Thread Affinity: 001        4               4        fj030
Thread Affinity: 001        5               5        fj030
...(truncated for legibility)...
```

In the first row, the '001' indicates the [nesting level](https://www.openmp.org/spec-html/5.0/openmpsu127.html) of the thread, the next column indicates the thread number (0-based index), the next column indicates the thread affinity (indicating in this case that thread 0 is bound to core 0), and the final column indicates the hostname of the compute node the thread was found on.

Finally, we have the "Hello World" statements:

```
 Hello world from thread 1 of 32 running on cpu  0 on fj030!
Hello world from thread 2 of 32 running on cpu  0 on fj030!
Hello world from thread 3 of 32 running on cpu  0 on fj030!
Hello world from thread 4 of 32 running on cpu  0 on fj030!
...(truncated for legibility)...
```

Since the code we ran indexes the threads starting at 1 and the CPUs starting at 0, we can see that setting OMP_PLACES=cores has bound the first thread, to the first CPU, the second thread to the second CPU...etc.

For some applications it may be beneficial to bind threads within individual [NUMA nodes](https://codenotary-compliance.medium.com/vmware-vsphere-why-checking-numa-configuration-is-so-important-9764c16a7e73) or [Core Memory Groups (CMGs)](https://www.fujitsu.com/global/about/resources/publications/technicalreview/2020-03/article03.html). To do this, we can change the value of OMP_PLACES to:

export OMP_PLACES=sockets

If we run the same script with this change, we see the following in the log:

```
OPENMP DISPLAY ENVIRONMENT BEGIN
  _OPENMP = '201511'
  OMP_DYNAMIC = 'FALSE'
  OMP_NESTED = 'FALSE'
  OMP_NUM_THREADS = '32'
  OMP_SCHEDULE = 'DYNAMIC'
  OMP_PROC_BIND = 'TRUE'
  OMP_PLACES = '{0:12},{12:12},{24:12},{36:12}'
  OMP_STACKSIZE = '0'
  OMP_WAIT_POLICY = 'PASSIVE'
  OMP_THREAD_LIMIT = '4294967295'
  OMP_MAX_ACTIVE_LEVELS = '2147483647'
  OMP_CANCELLATION = 'FALSE'
  OMP_DEFAULT_DEVICE = '0'
  OMP_MAX_TASK_PRIORITY = '0'
  OMP_DISPLAY_AFFINITY = 'TRUE'
  OMP_AFFINITY_FORMAT = 'Thread Affinity: %0.3L %.8n %.15{thread_affinity} %.12H'
OPENMP DISPLAY ENVIRONMENT END

Thread Affinity: 001        0            0-11        fj030
Thread Affinity: 001        1            0-11        fj030
Thread Affinity: 001        2            0-11        fj030
Thread Affinity: 001        3            0-11        fj030
Thread Affinity: 001        4            0-11        fj030
Thread Affinity: 001        5            0-11        fj030
Thread Affinity: 001        6            0-11        fj030
Thread Affinity: 001        7            0-11        fj030
Thread Affinity: 001        8           12-23        fj030
Thread Affinity: 001        9           12-23        fj030
Thread Affinity: 001       10           12-23        fj030
Thread Affinity: 001       11           12-23        fj030
Thread Affinity: 001       12           12-23        fj030
Thread Affinity: 001       13           12-23        fj030
Thread Affinity: 001       14           12-23        fj030
Thread Affinity: 001       15           12-23        fj030
Thread Affinity: 001       16           24-35        fj030
Thread Affinity: 001       17           24-35        fj030
Thread Affinity: 001       18           24-35        fj030
Thread Affinity: 001       19           24-35        fj030
Thread Affinity: 001       20           24-35        fj030
Thread Affinity: 001       21           24-35        fj030
Thread Affinity: 001       22           24-35        fj030
Thread Affinity: 001       23           24-35        fj030
Thread Affinity: 001       24           36-47        fj030
Thread Affinity: 001       25           36-47        fj030
Thread Affinity: 001       26           36-47        fj030
Thread Affinity: 001       27           36-47        fj030
Thread Affinity: 001       28           36-47        fj030
Thread Affinity: 001       29           36-47        fj030
Thread Affinity: 001       30           36-47        fj030
Thread Affinity: 001       31           36-47        fj030

Hello world from thread 1 of 32 running on cpu  0 on fj030!
Hello world from thread 2 of 32 running on cpu  3 on fj030!
Hello world from thread 3 of 32 running on cpu  4 on fj030!
Hello world from thread 4 of 32 running on cpu  5 on fj030!
Hello world from thread 5 of 32 running on cpu  6 on fj030!
Hello world from thread 6 of 32 running on cpu  7 on fj030!
Hello world from thread 7 of 32 running on cpu  8 on fj030!
Hello world from thread 8 of 32 running on cpu  9 on fj030!
Hello world from thread 9 of 32 running on cpu 12 on fj030!
Hello world from thread 10 of 32 running on cpu 13 on fj030!
Hello world from thread 11 of 32 running on cpu 14 on fj030!
Hello world from thread 12 of 32 running on cpu 12 on fj030!
Hello world from thread 13 of 32 running on cpu 15 on fj030!
Hello world from thread 14 of 32 running on cpu 14 on fj030!
Hello world from thread 15 of 32 running on cpu 16 on fj030!
Hello world from thread 16 of 32 running on cpu 17 on fj030!
Hello world from thread 17 of 32 running on cpu 24 on fj030!
Hello world from thread 18 of 32 running on cpu 25 on fj030!
Hello world from thread 19 of 32 running on cpu 24 on fj030!

...(truncated for legibility)...
```

Now we see that threads 0-7 are bound to CPUs in the first CMG (CPUs 0-11), threads 8-15 are bound to CPUs in the second CMG (CPUs 12-23), threads 16-23 are bound to CPUs in the third CMG (CPUs 24-35), and threads 24-31 are bound to CPUs in the fourth and final CMG (cores 34-47).

Note however within each CMG, the thread index does not necessarily match the CPU index (e.g., the 19th thread is bound to the 25th CPU).

If we wish to ensure that the order of threads matches the order of CPUs, we can explicitly define the binding assignments. The syntax for doing this is

```
location:number:stride
```

For example:

```
export OMP_PLACES="{0}:12,{12}:12,{24}:12,{36}:12"
```

The above syntax designates 4 different locations, each of which will receive 12 cores (we have omitted the stride). Within the first CMG, thread 0 will be bound to core 0, thread 1 to core 1, etc. The same logic is applied to the cores in the other CMGs as well, such that each thread index will match the core index.

Similarly,

```
export OMP_PLACES="{0:12},{12:12},{24:12},{36:12}"
```

will specify 4 locations that each receive 12 cores. However, in this case the thread index will not necessarily match the core index.

This type of explicit binding assignment grammar can be applied in a variety of different ways to accomodate a different scenarios. See here for several additional examples.

Uses may also wish to use OpenMP in conjuction with MPI. Some instructions and examples for thread binding under hybrid OMP-MPI scenarios can be found [here](core-thread-control-mpi-flags.md).

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/thread_binding.php`, retrieved November 5, 2026.
{: .archive-credit }
