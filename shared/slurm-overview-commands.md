# SLURM overview & commands

## What is SLURM?

SLURM (Simple Linux Utility for Resource Management) is the open-source workload manager and job scheduler used on the RCI clusters to manage compute resources and run jobs efficiently.

Before using SLURM commands, load the module:

```
module load slurm
```

## Essential commands

| Function | Command | Description |
| --- | --- | --- |
| Submit batch job | `sbatch [script]` | Submit a job script to the queue (see [Writing job scripts](writing-job-scripts.md)) |
| Interactive job | `srun --pty bash` | Start an interactive session on a compute node (see [Interactive jobs](interactive-jobs.md)) |
| Check job status | `squeue` | View the current job queue and status |
| Check your jobs | `squeue --user=$USER` | View only your jobs |
| Cancel job | `scancel [job_id]` | Cancel a running or queued job |
| Job details | `scontrol show job [job_id]` | Show detailed job configuration and runtime info |
| Job history | `sacct` | View completed job information |
| Node information | `sinfo` | Display node and partition information |

!!! tip ""
    **Tip:** Use `sbatch` for batch jobs (non-interactive, queued execution) and `srun` for interactive sessions (real-time access to compute nodes).

## Essential SLURM directives

| Resource | Directive | Example |
| --- | --- | --- |
| Job name | `#SBATCH --job-name=` | `--job-name=my_job` |
| Number of nodes | `#SBATCH --nodes=` | `--nodes=2` |
| Tasks per node | `#SBATCH --ntasks-per-node=` | `--ntasks-per-node=40` |
| CPUs per task | `#SBATCH --cpus-per-task=` | `--cpus-per-task=2` |
| Memory per node | `#SBATCH --mem=` | `--mem=64GB` |
| Wall time | `#SBATCH --time=` | `--time=02:30:00` |
| Partition/queue | `#SBATCH -p` | `-p short-40core` |
| Output file | `#SBATCH --output=` | `--output=job_%j.out` |
| Error file | `#SBATCH --error=` | `--error=job_%j.err` |

The `%j` placeholder in filenames is automatically replaced with the job ID. Note that `-n` specifies the number of tasks (e.g. MPI processes) while `-c` specifies CPU cores per task (e.g. OpenMP threads).

## Useful environment variables

| Variable | Description |
| --- | --- |
| `$SLURM_JOBID` | Unique job identifier |
| `$SLURM_SUBMIT_DIR` | Directory the job was submitted from |
| `$SLURM_JOB_NODELIST` | List of nodes allocated to the job |
| `$SLURM_NTASKS` | Total number of tasks for the job |
| `$SLURM_CPUS_PER_TASK` | CPUs allocated per task |
| `$SLURM_JOB_NAME` | Name of the job |

```
echo "Job ID: $SLURM_JOBID"
echo "Running on nodes: $SLURM_JOB_NODELIST"
cd $SLURM_SUBMIT_DIR
```

## Best practices

- **Estimate resources honestly.** Over-requesting leads to longer queue times and reduced system efficiency.
- **Always capture output.** Use `%j` in output/error filenames to track jobs.
- **Load modules in the script.** Start with `module purge` to avoid conflicts.
- **Test small first.** Debug in interactive sessions before submitting large batch jobs.

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/slurm-overview-commands> (maintained by Research Computing and Informatics).
{: .rci-credit }
