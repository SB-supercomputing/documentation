# Getting started on NVwulf

Your first hour on NVwulf: log in, bring your data over from SeaWulf, load software, and run a first GPU job.

**On this page:** [Log in](#login) · [Move data from SeaWulf](#data) · [Load software](#modules) · [First GPU job](#job) · [Interactive GPU session](#interactive) · [Tips](#tips)

> [!NOTE]
> **Need an account?** See [Getting access to NVwulf](getting-access-nvwulf.md).

## 1. Log in {#login}

Use SSH (Duo required):

```
ssh -X <netid>@login.nvwulf.stonybrook.edu
```

Or use your browser with [Open OnDemand for NVwulf](https://nvwulf-ood.nvwulf.stonybrook.edu/), which has Jupyter, RStudio, VS Code, AI chat, and science apps ready to launch (see [the full app list](nvwulf-ondemand-apps.md)). Windows setup and Duo tips are in [Connecting to the cluster](../shared/connecting-cluster.md).

## 2. Move data from SeaWulf {#data}

NVwulf has its own storage, separate from SeaWulf. Copy what you need with `rsync`, running the command **on NVwulf**:

```
# One file
rsync -v <netid>@login.seawulf.stonybrook.edu:~/test.txt ~/test.txt

# A whole folder, including subfolders
rsync -av <netid>@login.seawulf.stonybrook.edu:~/test/ ~/test/
```

For very large datasets, [Globus](../seawulf/globus-file-transfer.md) may be faster.

## 3. Load software {#modules}

```
module avail                  # see what's available
module load miniconda/3       # load a module
module load slurm             # needed for job commands
```

More in [Using modules](../shared/using-modules.md).

## 4. Your first GPU job {#job}

See the GPU partitions (`h200x4`, `h200x8`, `b40x4`, plus `-long` and `debug-` versions):

```
sinfo
```

Save this as `test_job.slurm`. It asks for 1 GPU, 8 CPUs, and 25 GB of memory for 5 minutes:

```
#!/bin/bash
#SBATCH --job-name=test-tf
#SBATCH --output=res.txt
#SBATCH --partition=h200x4
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem=25g
#SBATCH --gpus=1
#SBATCH --time=05:00

module load tensorflow/2.19.0
python tf_test_nn_training.py
```

Submit it and watch it:

```
sbatch test_job.slurm
squeue -u $USER
```

When it finishes, the output is in `res.txt`. To check the GPU was really used, add `nvidia-smi` as a line before your program.

## Interactive GPU session {#interactive}

For testing and debugging, get a shell on a GPU node:

```
srun -p h200x4 --gpus=1 --cpus-per-task=8 --mem=25g --time=01:00:00 --pty bash
```

Type `exit` when you're done so the GPU goes back to others.

## Tips {#tips}

- **Ask only for the GPUs you'll use.** Idle GPUs are expensive and slow down everyone's queue.
- **Start in a debug partition** for short tests before a big run.
- **Use the [job script builder](https://rci.stonybrook.edu/hpc/script-builder)** to make NVwulf scripts with the right partition limits.
- **Read [Good conduct on the RCI clusters](../shared/hpc-good-conduct.md)** before running large jobs.

**Applies to:** NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/getting-started-nvwulf> (maintained by Research Computing and Informatics).
