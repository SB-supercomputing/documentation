# Example Slurm Job Script

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

This is an example slurm job script for the Ookami short queue:

```
#!/usr/bin/env bash

#SBATCH --job-name=examplejob
#SBATCH --output=examplejob.log
#SBATCH --ntasks-per-node=48
#SBATCH -N 2
#SBATCH --time=00:05:00
#SBATCH -p short

module load slurm
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6

mpicc /lustre/projects/global/samples/HelloWorld/mpi_hello.c -o mpi_hello

srun ./mpi_hello
```

This job will utilize 2 nodes, with 48 CPUs per node for 5 minutes in the short partition to compile and run an mpi_hello script.

If we named this script "test.slurm", we could submit the job using the following command:

```
sbatch test.slurm
```

**Breakdown:**

The directive

```
#SBATCH -p short
```

indicates to the batch scheduler that you want to use the short queue.

The directives

```
#SBATCH --ntasks-per-node=48
#SBATCH --nodes=2
#SBATCH --time=05:00
```

indicate that we are requesting 2 nodes, and we will run 48 tasks per node for 5 minutes.

All of these directives are passed straight to the sbatch command, so for a full list of options just take a look at the sbatch manual page by issuing the command:

```
man sbatch
```

For more information on SLURM, please also see [the official documentation](https://slurm.schedmd.com/documentation.html).

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/example-slurm-script.php`, retrieved November 5, 2026.
{: .archive-credit }
