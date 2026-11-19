# Writing job scripts

A job script tells Slurm what your job needs (cores, memory, time, queue) and what to run. Write it once, submit it with `sbatch`, and Slurm runs it on a compute node when resources are free. This page gives you a template to copy, explains each part, and lists the options you'll use most.

**On this page:** [The four parts](#parts) · [Template](#template) · [Asking for resources](#resources) · [Directive reference](#directives) · [Useful variables](#variables) · [Dependencies](#depend) · [Make scripts safer](#safe) · [Troubleshooting](#trouble)

!!! note ""
    **Shortcut:** the [job script builder](https://rci.stonybrook.edu/hpc/script-builder) asks a few questions and writes the script for you. Remember to run `module load slurm` before using `sbatch`.

## The four parts of a job script {#parts}

1. **Shebang line**: `#!/bin/bash`, so the script runs in bash.
2. **#SBATCH lines**: what the job needs. Slurm reads these; bash treats them as comments.
3. **Environment setup**: load modules and set variables.
4. **The work**: the commands that actually run.

## Template {#template}

```
#!/bin/bash

# --- Job identification ---
#SBATCH --job-name=my_job
#SBATCH --output=%x_%j.out            # %x = job name, %j = job ID
#SBATCH --error=%x_%j.err

# --- Resources ---
#SBATCH --partition=short-40core
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --time=02:00:00               # hh:mm:ss

# --- Optional: email when it ends or fails ---
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=<you>@stonybrook.edu

# --- Environment setup ---
module purge
module load intel/oneAPI/2022.2
module load compiler/latest
module load mpi/latest
export OMP_NUM_THREADS=1

echo "Job $SLURM_JOB_ID on $SLURM_JOB_NODELIST, $SLURM_NTASKS tasks, started $(date)"

# --- The work ---
cd $SLURM_SUBMIT_DIR
mpirun ./my_app input.dat > computation.log

echo "Finished $(date)"
```

Submit it and check on it:

```
sbatch my_job.slurm
squeue -u $USER
```

Ready-made scripts for serial, multi-threaded, MPI, GPU, and array jobs are in [Example jobs](../seawulf/example-jobs.md).

## Asking for the right resources {#resources}

- **Pick the queue first.** The queue decides the node type and the maximum run time. See the [queue selection guide](../seawulf/queue-selection-guide.md).
- **Whole node or part of one?** Queues without `-shared` give you whole nodes, with all their memory. For small jobs, use a [shared queue](../seawulf/shared-nodes.md) and set `--mem`.
- **Tasks vs. CPUs per task.** Use `--ntasks` for MPI processes and `--cpus-per-task` for threads (OpenMP, Python multiprocessing). Match `OMP_NUM_THREADS` to `$SLURM_CPUS_PER_TASK`.
- **Time.** Ask for a realistic limit with some margin. Shorter requests often start sooner; if the job runs past its limit, Slurm stops it.
- **Check afterward.** `seff <jobid>` shows how much CPU and memory you really used, so you can ask for less next time.

## Directive reference {#directives}

| Directive | What it sets | Example |
| --- | --- | --- |
| `-p, --partition` | Queue | `#SBATCH -p short-40core` |
| `-N, --nodes` | Number of nodes | `#SBATCH -N 2` |
| `-n, --ntasks` | Total tasks (e.g. MPI ranks) | `#SBATCH -n 80` |
| `--ntasks-per-node` | Tasks on each node | `#SBATCH --ntasks-per-node=40` |
| `-c, --cpus-per-task` | CPUs for each task (threads) | `#SBATCH -c 8` |
| `--mem` | Memory per node | `#SBATCH --mem=64GB` |
| `--mem-per-cpu` | Memory per CPU | `#SBATCH --mem-per-cpu=2GB` |
| `-t, --time` | Time limit | `#SBATCH -t 02:30:00` |
| `-J, --job-name` | Job name | `#SBATCH -J my_job` |
| `-o, --output` | File for normal output | `#SBATCH -o job_%j.out` |
| `-e, --error` | File for error output | `#SBATCH -e job_%j.err` |
| `--gres` | GPUs and other resources | `#SBATCH --gres=gpu:2` |
| `--array` | Job array indices | `#SBATCH --array=1-100` |
| `--mail-type`, `--mail-user` | Email notices | `#SBATCH --mail-type=END,FAIL` |

## Useful variables inside a job {#variables}

| Variable | Holds |
| --- | --- |
| `$SLURM_JOB_ID` | The job ID |
| `$SLURM_SUBMIT_DIR` | The folder you ran `sbatch` from |
| `$SLURM_JOB_NODELIST` | The nodes the job is running on |
| `$SLURM_NTASKS` | Total number of tasks |
| `$SLURM_CPUS_PER_TASK` | CPUs given to each task |
| `$SLURM_ARRAY_TASK_ID` | This task's index in a job array |

## Run jobs in order (dependencies) {#depend}

For work in steps, such as preprocessing, then analysis, then plotting, you can submit every step at once and have each one wait for the one before it. Slurm holds the later jobs until their condition is met.

```
# Submit the first step and keep its job ID
jid=$(sbatch --parsable step1.slurm)

# Start step 2 only if step 1 finishes successfully
sbatch --dependency=afterok:$jid step2.slurm
```

| Condition | The new job starts once the earlier job has |
| --- | --- |
| `afterok:<jobid>` | finished successfully (exit code 0) |
| `afternotok:<jobid>` | failed, which is handy for a cleanup or alert step |
| `afterany:<jobid>` | ended, whatever the outcome |
| `after:<jobid>` | started running |

You can wait on several jobs at once, as in `afterok:1234:1235`. If a condition can never be met (step 1 failed and step 2 needed `afterok`), the waiting job stays in the queue with the reason `DependencyNeverSatisfied`. Cancel it with `scancel <jobid>`.

## Make scripts safer and easier to debug {#safe}

```
# Stop at the first error instead of carrying on
set -e

# Check the input exists before doing any work
if [ ! -f "input.dat" ]; then
    echo "ERROR: input.dat not found"
    exit 1
fi

# Time the main step
start=$(date +%s)
mpirun ./my_app input.dat
echo "Computation took $(( $(date +%s) - start )) seconds"
```

- **Start with `module purge`** so modules left over from your login session don't interfere.
- **Load the same modules you compiled with.**
- **Test small first:** a short run in `debug-40core`, or an [interactive session](interactive-jobs.md), before a big submission.
- **Keep a template** for each kind of job you run often.

## Troubleshooting {#trouble}

<details markdown="1">
<summary>"sbatch: command not found"</summary>

Run `module load slurm` first.

</details>

<details markdown="1">
<summary>"Batch job submission failed: Requested node configuration is not available"</summary>

You asked for more cores, memory, or GPUs than a node in that queue has, or used a queue that isn't reachable from your login node. Compare your request with the [queue tables](../seawulf/queue-selection-guide.md), and see [which login node](connecting-cluster.md#login-nodes) reaches which queues.

</details>

<details markdown="1">
<summary>My job ended early with "TIME LIMIT" or "DUE TO TIME LIMIT"</summary>

It ran past its `--time`. Ask for more time, move to a longer queue, or save progress (checkpoint) so you can restart.

</details>

<details markdown="1">
<summary>"Out of memory" or "oom-kill"</summary>

The job used more memory than it asked for. Raise `--mem` (on shared queues) or use more nodes. `seff <jobid>` shows the peak memory used.

</details>

<details markdown="1">
<summary>Windows line endings: "/bin/bash^M: bad interpreter"</summary>

The script was saved on Windows. Convert it on the cluster with:

```
sed -i 's/\r$//' my_job.slurm
```

</details>

More commands for watching and changing jobs are in [Managing jobs](managing-jobs.md) and the [cheat sheet](hpc-cheat-sheet.md).

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/writing-job-scripts> (maintained by Research Computing and Informatics).
{: .rci-credit }
