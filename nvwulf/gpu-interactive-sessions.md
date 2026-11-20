# GPU interactive sessions on NVwulf

An interactive session gives you a shell or a notebook on a GPU node, which is the right tool for testing, debugging and exploring. The GPU is yours for the whole session, whether you are using it or not, so a session left open overnight keeps that GPU away from everyone else. This page shows how to start a session that fits the work, and how to make sure it ends when you are done.

**On this page:** [Which kind of session](#which) · [Start a shell on a GPU](#start) · [End it](#end) · [Close idle shells on their own](#idle) · [Check the GPU is working](#check) · [Turning it into a batch job](#batch)

!!! note ""
    **The one habit that matters most:** ask for the time you need now, not the most the partition allows, and type `exit` when you are done. Many NVwulf shell sessions run until the time limit closes them, which often means the GPU was held long after the work was done.

## Which kind of session {#which}

| You want to | Use | Time to ask for |
| --- | --- | --- |
| Check a script runs, or try a quick fix | A shell in a debug partition (`debug-h200x4` or `debug-b40x4`) | 30 to 60 minutes (the limit is 1 hour) |
| Work in a notebook, RStudio or VS Code | An [Open OnDemand app](nvwulf-ondemand-apps.md) | The hours you plan to work, not a whole day |
| Debug something that needs a longer run | A shell in `h200x4` or `b40x4` | A few hours (the limit is 8 hours) |
| Train or process for many hours | A [batch job](#batch), not an interactive session | Your usual run time plus a margin |

## Start a shell on a GPU {#start}

From the NVwulf login node, after `module load slurm`:

```
# a quick test: 1 GPU for 30 minutes in the debug partition
srun -p debug-h200x4 --gpus=1 --cpus-per-task=8 --mem=25g --time=00:30:00 --pty bash

# a longer debugging session: 1 GPU for 2 hours
srun -p h200x4 --gpus=1 --cpus-per-task=8 --mem=25g --time=02:00:00 --pty bash
```

Ask for one GPU unless you are testing code that uses several. Keep memory in proportion to the GPUs: on a B40 node the even share is about 125 GB per GPU.

## End it when you are done {#end}

```
exit                     # leaves the shell and gives the GPU back
squeue -u $USER          # check nothing is still running
scancel <jobid>          # end a session you left behind
```

If you started the session inside `tmux` or `screen`, closing your laptop does not end it. If you were cut off, run `squeue -u $USER` when you log back in. For Open OnDemand apps, use the **Delete** button on the My Interactive Sessions page when you finish, rather than just closing the browser tab.

## Close idle shells on their own {#idle}

Bash can log you out after a stretch with no typing. Inside the GPU shell, run:

```
TMOUT=1800               # exit after 30 minutes idle at the prompt
```

When the shell exits, the session ends and the GPU is released. This only counts time spent sitting at the prompt, so a program that is still running is not interrupted. To have it in every GPU shell, add this to your `~/.bashrc`; it only takes effect inside Slurm jobs:

```
[ -n "$SLURM_JOB_ID" ] && [ -n "$PS1" ] && TMOUT=1800
```

## Check the GPU is working {#check}

```
nvidia-smi                       # the GPU you were given and what is using it
watch -n 5 nvidia-smi            # refresh every 5 seconds; Ctrl+C to stop
```

If `GPU-Util` stays near 0% while your program runs, the program is probably running on the CPU. Check that your framework sees the GPU (for PyTorch, `python -c "import torch; print(torch.cuda.is_available())"`) and that you loaded the GPU build of your software.

## Turning it into a batch job {#batch}

Once a command works in your session, put it in a job script and submit it with `sbatch`. The job runs without you, ends when the work ends, and you can close your laptop. The commands you typed become the last lines of the script:

```
#!/bin/bash
#SBATCH --job-name=train
#SBATCH --partition=h200x4
#SBATCH --gpus=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=25g
#SBATCH --time=06:00:00          # your usual run time plus a margin
#SBATCH --output=%x_%j.out

module load miniconda/3
# ...the same setup you used in the session...
python train.py
```

The [job script builder](https://rci.stonybrook.edu/hpc/script-builder) writes NVwulf scripts with the right partition limits, and [Choosing a time limit](../shared/choosing-time-limits.md) helps you pick `--time`.

Related: [Getting started on NVwulf](getting-started-nvwulf.md) · [NVwulf queues](nvwulf-queues.md) · [Interactive jobs](../shared/interactive-jobs.md) · [Why did my job fail?](../shared/job-failures.md)

**Applies to** <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/gpu-interactive-sessions> (maintained by Research Computing and Informatics).
{: .rci-credit }
