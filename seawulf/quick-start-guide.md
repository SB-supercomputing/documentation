# Quick Start Guide

This guide takes you from a brand-new account to your first finished job on SeaWulf in about 30 minutes. You'll connect, load software, write a tiny job script, submit it, and read the result.

**On this page:** [Before you start](#before) · [1. Connect](#connect) · [2. Load software](#modules) · [3. Your first job](#job) · [4. Watch it run](#states) · [What next](#next) · [If something goes wrong](#trouble)

## Before you start {#before}

- **A SeaWulf account.** Accounts sit under a project led by a Stony Brook faculty member. See [Requesting accounts & project numbers](../shared/requesting-accounts-project-numbers.md).
- **Duo set up** on your phone. Every login asks for it. See [Duo authentication](../shared/duo-authentication.md).

## 1. Connect {#connect}

The easiest start is **Open OnDemand** in your browser at [sn-ood.seawulf.stonybrook.edu](https://sn-ood.seawulf.stonybrook.edu/). Sign in with your NetID, approve Duo, then open the **SeaWulf Cluster Shell Access** app for a terminal. See the [OnDemand overview](../shared/ondemand-overview.md).

Prefer a terminal on your own computer? Use SSH:

```
ssh <netid>@milan.seawulf.stonybrook.edu
```

Windows users can use MobaXterm or the built-in Windows Terminal. [Connecting to the cluster](../shared/connecting-cluster.md) has step-by-step instructions and explains which login address to use.

> [!NOTE]
> **You're now on a shared login node.** It's fine for editing files and submitting jobs, but don't run real computations here. Anything heavy goes in a job. See [Login node etiquette](../shared/login-node-etiquette.md).

## 2. Load software {#modules}

Software on SeaWulf comes as *modules* that you load when you need them. Start by loading Slurm, the job scheduler, which you'll need in every session:

```
module load slurm             # job commands: sbatch, squeue, scancel
module avail                  # see what software is available
module load gcc/12.3.0        # load a specific package and version
module list                   # check what's loaded
```

More in [Using modules](../shared/using-modules.md) and the [software catalog](../software/README.md).

## 3. Your first job {#job}

1. **Make a folder for it.**

    ```
    mkdir ~/my_first_job && cd ~/my_first_job
    ```

2. **Create a job script** called `hello.slurm`. Open an editor with `nano hello.slurm`, paste this in, then save with **Ctrl+O** and exit with **Ctrl+X**:

    ```
    #!/bin/bash
    #SBATCH --job-name=hello_world
    #SBATCH --partition=short-40core-shared   # a small, shared queue
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --mem=1G
    #SBATCH --time=00:05:00                   # 5 minutes is plenty
    #SBATCH --output=hello_%j.out             # %j becomes the job ID
    #SBATCH --error=hello_%j.err

    echo "Hello from SeaWulf!"
    echo "Job ID: $SLURM_JOB_ID"
    echo "Running on node: $(hostname)"
    echo "Date and time: $(date)"
    ```

3. **Submit it.**

    ```
    sbatch hello.slurm
    ```

    Slurm replies with something like `Submitted batch job 12345`. That number is your job ID.

4. **Read the result** once it finishes (use your own job ID):

    ```
    cat hello_12345.out
    ```

## 4. Watch it run {#states}

```
squeue -u $USER
```

The **ST** column shows where your job is:

| State | Meaning |
| --- | --- |
| `PD` Pending | Waiting in the queue for resources |
| `R` Running | Running now |
| `CG` Completing | Finishing up |

When the job disappears from `squeue`, it's done. Check how it went with `sacct -j <jobid>`.

## What next {#next}

- [Writing job scripts](../shared/writing-job-scripts.md): the full template and every common option.
- [Queue selection guide](queue-selection-guide.md): pick the right queue for your job size and length.
- [Interactive jobs](../shared/interactive-jobs.md): a live shell on a compute node for testing.
- [File transfer](../shared/file-transfer-cli.md): get your data onto the cluster.
- [Job script builder](https://rci.stonybrook.edu/hpc/script-builder): answer a few questions and get a script.
- [HPC cheat sheet](../shared/hpc-cheat-sheet.md): the commands you'll use every day, on one page.

## If something goes wrong {#trouble}

<details markdown="1">
<summary>"sbatch: command not found"</summary>

Load Slurm first with `module load slurm`.

</details>

<details markdown="1">
<summary>My job stays in PD (pending) for a long time</summary>

The queue may be busy, or you may have asked for more than the queue allows. Check the reason in the last column of `squeue -u $USER`, try a smaller request, or test your script without running it:

```
sbatch --test-only hello.slurm
```

</details>

<details markdown="1">
<summary>"invalid partition specified"</summary>

Each set of login nodes reaches different queues. The queues in this guide run from `milan.seawulf.stonybrook.edu`. See [Which SeaWulf login node?](../shared/connecting-cluster.md#login-nodes)

</details>

<details markdown="1">
<summary>I can't log in</summary>

Repeated failed logins can block your address or lock your Duo. See [login troubleshooting](../shared/connecting-cluster.md#trouble) and [Duo troubleshooting](../shared/duo-authentication.md#trouble).

</details>

<details markdown="1">
<summary>A graphical program won't open</summary>

Connect with `ssh -X`, or use [WolfieHPCDesktop](../shared/seawulf-desktop.md) in Open OnDemand. See [X11 forwarding](x11-forwarding.md).

</details>

Still stuck? [When to ask for help](../shared/when-ask-help.md) explains how to reach HPC support and virtual office hours.

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/quick-start-guide> (maintained by Research Computing and Informatics).
