# HPC cheat sheet

The commands you'll type most on SeaWulf, on one page. Everything here runs on a login node after you [connect](connecting-cluster.md). Replace anything in `<angle brackets>` with your own values.

**Jump to:** [Top 10](#top10) · [Run work](#run) · [Job script](#script) · [Queues](#queues) · [Manage jobs](#manage) · [Files & transfer](#files) · [Modules](#modules) · [Storage](#storage) · [Efficiency](#perf) · [Troubleshooting](#trouble)

!!! note ""
    **First, load Slurm.** The job commands below need the Slurm module. Run this once each time you log in, or add it to your `~/.bashrc`:

    ```
    module load slurm
    ```

## Top 10 {#top10}

| Command | What it does |
| --- | --- |
| `sbatch job.sh` | Submit a job script |
| `squeue -u $USER` | List your jobs and their state |
| `scancel <jobid>` | Cancel a job |
| `srun -p short-40core --pty bash` | Open an interactive shell on a compute node |
| `sinfo -p short-40core` | See how busy a queue is |
| `scontrol show job <jobid>` | Full details of one job, including why it's waiting |
| `sacct -j <jobid>` | Look up a finished job |
| `seff <jobid>` | How much CPU and memory a finished job really used |
| `module avail` / `module load <name>` | Find and load software |
| `myquota` | Check your storage and file-count limits |

## Three ways to run work {#run}

```
# Batch: queue a script to run on its own (best for real work)
sbatch job.sh

# Interactive: get a shell on a compute node, then work as usual
srun -p short-40core --time=01:00:00 --pty bash

# Allocate first, then run steps inside the allocation with srun
salloc -p short-40core --time=02:00:00 --ntasks=4
```

Type `exit` when you're done with an interactive session so the node is freed. More in [Interactive jobs](interactive-jobs.md).

## Job script template {#script}

```
#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --output=results_%j.txt      # %j becomes the job ID
#SBATCH --error=errors_%j.txt
#SBATCH --partition=short-40core
#SBATCH --time=02:00:00              # hh:mm:ss, keep it realistic
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=<you>@stonybrook.edu

module load intel-stack
mpirun ./my_program               # MPI example; for a serial program, just run it
```

Prefer not to write it by hand? The [job script builder](https://rci.stonybrook.edu/hpc/script-builder) makes one for you. Details in [Writing job scripts](writing-job-scripts.md).

## Common queues {#queues}

| Queue | Time limit | Good for |
| --- | --- | --- |
| `debug-40core` | 1 hour | Quick tests before a big run |
| `short-40core` | 4 hours | Standard jobs using whole nodes |
| `short-40core-shared` | 4 hours | Smaller jobs that don't need a whole node |
| `medium-40core` | 12 hours | Longer runs |
| `short-96core` | 4 hours | Larger parallel jobs on AMD Milan nodes |

These run from `milan.seawulf.stonybrook.edu`. The [queue selection guide](../seawulf/queue-selection-guide.md) lists every queue, including GPU, high-memory, and long queues.

## Watch and manage jobs {#manage}

```
# Your jobs, with state and the reason a job is waiting
squeue -u $USER --format="%.10i %.20j %.8T %.10M %.6D %R"

# Cancel one job, or all of your pending jobs
scancel <jobid>
scancel -u $USER --state=pending

# Hold a pending job, then let it run again
scontrol hold <jobid>
scontrol release <jobid>

# Your job history since a date
sacct --starttime=<YYYY-MM-DD> --format=JobID,JobName,State,Elapsed,ExitCode
```

More in [Managing jobs](managing-jobs.md).

## Files and transfer {#files}

Run these on **your own computer**, not on the cluster.

```
# Upload a file or a folder to your home directory
scp results.csv <netid>@milan.seawulf.stonybrook.edu:~/
scp -r my_folder/ <netid>@milan.seawulf.stonybrook.edu:~/

# Download a file
scp <netid>@milan.seawulf.stonybrook.edu:~/output.txt ./

# Sync a folder (only copies what changed); try --dry-run first
rsync -avz --progress my_folder/ <netid>@milan.seawulf.stonybrook.edu:~/my_folder/
```

`rsync` flags: `-a` keeps permissions and times, `-v` lists files, `-z` compresses, `--dry-run` shows what would happen without copying. For large data, use [Globus](../seawulf/globus-file-transfer.md). To avoid a Duo prompt for every copy, see [fewer Duo prompts](duo-authentication.md#fewer).

## Software modules {#modules}

```
module avail                 # everything available
module avail python          # search by name
module load gcc/12.3.0       # load a specific version
module list                  # what's loaded now
module show <name>           # what a module sets up
module purge                 # unload everything and start clean
```

Browse what's installed in the [software catalog](../software/README.md). More in [Using modules](using-modules.md).

## Storage {#storage}

```
myquota                               # space and file counts for home and scratch
cd /gpfs/scratch/$USER                # your scratch space (files older than 45 days are deleted)
du -sh * | sort -h                    # what's using the space in this folder
tar -czf archive.tar.gz my_folder/    # bundle a folder into one file
tar -xzf archive.tar.gz               # unpack it
```

Home is 20 GB and backed up; scratch is 20 TB, not backed up, and purged after 45 days. See [Storage layout & policies](../seawulf/storage-layout-policies.md) and [Checking storage quotas](../seawulf/checking-storage-quotas.md).

## Check efficiency {#perf}

```
# While a job runs
sstat -j <jobid> --format=JobID,AveCPU,AveRSS,MaxRSS

# After it finishes
seff <jobid>
sacct -j <jobid> --format=JobID,Elapsed,MaxRSS,AveCPU,State
```

If `seff` shows you used far less memory or CPU than you asked for, request less next time. Your jobs will start sooner and [fair share](fairshare-job-priority.md) works in your favor.

## Quick troubleshooting {#trouble}

| Problem | Try |
| --- | --- |
| "command not found" for `sbatch` or `squeue` | `module load slurm` |
| Job stuck in PD (pending) | Check the reason with `squeue -u $USER` (last column) or `scontrol show job <jobid>`, and how busy the queue is with `sinfo -p <queue>` |
| Job failed | `tail -20 results_<jobid>.txt` and `grep -i error errors_<jobid>.txt` |
| Queue name not recognized | You may be on the wrong login node. See [which login node](connecting-cluster.md#login-nodes). |
| "Disk quota exceeded" | `myquota`, then clean up or move files to scratch |
| Can't connect | `ssh -v <netid>@milan.seawulf.stonybrook.edu` for details, and see [login troubleshooting](connecting-cluster.md#trouble) |

Still stuck? See [When to ask for help](when-ask-help.md) or [open a ticket](https://iacs.supportsystem.com). New to all this? Start with the [Quick Start Guide](../seawulf/quick-start-guide.md) and the [glossary of HPC terms](https://rci.stonybrook.edu/docs/glossary-hpc-terms).

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/hpc-cheat-sheet> (maintained by Research Computing and Informatics).
{: .rci-credit }
