# Interactive jobs

An interactive job gives you a live shell on a compute node, so you can test commands, debug code, compile, or try out software with real resources behind you. It's the right place for anything too heavy for the login node but not yet ready to become a batch job.

**On this page:** [Start a session](#start) · [Examples](#examples) · [Options](#options) · [During the session](#during) · [Graphical programs](#gui) · [Troubleshooting](#trouble)

## Start a session {#start}

1. Log in to `milan.seawulf.stonybrook.edu` and load Slurm:

    ```
    module load slurm
    ```

2. Ask for a shell on a compute node. Replace `short-40core` with the queue you want:

    ```
    srun -p short-40core --time=01:00:00 --pty bash
    ```

3. Wait for the prompt to change to a compute node name (for example `[netid@dn045 ~]$`). You're now on your own node.
4. When you're done, type `exit` to give the node back.

## Examples {#examples}

```
# A quick session on a whole 40-core node for an hour
srun -p short-40core -N 1 -n 40 --time=01:00:00 --pty bash

# Part of a node: 10 cores and 32 GB on a shared queue (starts sooner for small work)
srun -p short-40core-shared -N 1 -n 10 --mem=32GB --time=02:00:00 --pty bash

# One A100 GPU for an hour
srun -p a100 --gres=gpu:1 --time=01:00:00 --pty bash

# A short test in the debug queue
srun -p debug-40core --time=00:30:00 --pty bash
```

## Common options {#options}

| Option | What it sets | Example |
| --- | --- | --- |
| `-p` | Queue | `-p short-40core` |
| `-N` | Number of nodes | `-N 1` |
| `-n` | Number of tasks | `-n 20` |
| `-c` | Cores per task | `-c 2` |
| `--mem` | Memory per node (needed on shared queues) | `--mem=64GB` |
| `--time` | How long you need it | `--time=02:00:00` |
| `--gres` | GPUs | `--gres=gpu:1` |
| `--pty bash` | Gives you the interactive shell. Always put it last. |  |

Not sure which queue? See the [queue selection guide](../seawulf/queue-selection-guide.md).

## During the session {#during}

- Load modules, compile, run and test programs, and check how your code behaves with MPI or OpenMP.
- Everything you had on the login node is here too: home, scratch, and project folders are the same on every node.
- Interactive sessions aren't good for timing benchmarks at scale, because performance can vary. Use a batch job for that.
- If your connection drops, the session ends. For long work, write a [job script](writing-job-scripts.md) instead.

## Graphical programs {#gui}

To open program windows from a compute node, connect to SeaWulf with `ssh -X`, get an allocation with `salloc`, then SSH to the node you were given, again with `-X`:

```
module load slurm
salloc -N 1 -p short-40core --time=01:00:00
ssh -X $SLURM_NODELIST
```

Run your program as usual from there, and type `exit` twice when done (once to leave the node, once to end the allocation). For a smoother experience, use a [WolfieHPCDesktop](seawulf-desktop.md) session in Open OnDemand. See [X11 forwarding](../seawulf/x11-forwarding.md).

## Troubleshooting {#trouble}

<details markdown="1">
<summary>The command just waits with "job has been allocated resources" never appearing</summary>

The queue is busy. Ask for less (fewer cores, less time), try a shared queue, or check how busy it is with `sinfo -p <queue>`. Press **Ctrl+C** to give up waiting.

</details>

<details markdown="1">
<summary>"srun: command not found"</summary>

Run `module load slurm` first.

</details>

<details markdown="1">
<summary>"invalid partition specified"</summary>

That queue isn't reachable from the login node you're on. See [Which SeaWulf login node?](connecting-cluster.md#login-nodes)

</details>

<details markdown="1">
<summary>My session ended unexpectedly</summary>

It probably reached its time limit or your connection dropped. Ask for a longer `--time`, and consider a batch job for anything that runs for hours.

</details>

## Good habits

- Ask only for what you need, and set a realistic `--time`.
- Use interactive sessions for testing and debugging, then move real runs to batch jobs.
- Always `exit` when you're finished so the node goes back to others.

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/interactive-jobs> (maintained by Research Computing and Informatics).
{: .rci-credit }
