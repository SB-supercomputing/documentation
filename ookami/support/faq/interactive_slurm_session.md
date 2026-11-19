# Interactive Sessions

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

## Requesting an Interactive Session in Slurm

The Slurm scheduler allows for running an interactive shell on compute nodes. First, load the slurm module.

```
module load slurm
```

To enter an interactive session, use the srun command with the --pty directive. At a minimum, provide the following options to srun to enable the interactive shell:

```
srun -p <queue> --pty bash
```

You can pass the same additional options to srun as you would in your Slurm job script files. Some useful options are:

- -N &lt;# of nodes>
- -t hh:mm:ss or w-hh:mm:ss
- -n &lt;tasks per node>

For an interactive job using 1 node and 24 tasks per node with a 4 hour run time on the short queue, this would look like:

```
srun -N 1 -n 24 -t 04:00:00 -p short --pty bash
```

## Running an interactive job

Upon initializing the interactive shell, you will be taken away from the login node.

All of your environment variables from the login node will be copied to your interactive shell (just as when you submit a job). This means all of your modules will still be loaded and you will remain in the same working directory as before. You can immediately run your program for testing:

All contents sent to stdout will be printed directly to the terminal unless otherwise directed. For more infornation on handling output see the associated FAQ page.

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/interactive_slurm_session.php`, retrieved November 5, 2026.
{: .archive-credit }
