# Why did my job fail?

When a job fails, Slurm records a state and an exit code, and your program usually leaves a message in the job's output file. This page shows how to find both, what the common codes mean, and the fix for each. Most failed GPU jobs on NVwulf stop within the first 10 minutes, which almost always means a script or software setup problem you can fix in a few minutes.

**On this page:** [First look](#first-look) · [Reading the exit code](#read-code) · [Exit code 1](#exit-1) · [Exit code 2](#exit-2) · [Exit codes 127 and 126](#exit-127) · [Out of memory](#oom) · [Killed or stopped](#killed) · [Crashed](#segfault) · [Node failure](#node-fail) · [Anything else](#find-error) · [Getting help](#help)

> [!NOTE]
> **Test small first.** Run a short version of your job in a debug partition (`debug-h200x4` or `debug-b40x4` on NVwulf, 1 hour limit) before a long run. Most problems show up in the first minute.

## First look: state, exit code and output {#first-look}

Run `module load slurm` first, then:

```
sacct -j <jobid> --format=JobID,JobName,State,ExitCode,Elapsed,Timelimit,MaxRSS
seff <jobid>                     # memory and CPU used against what you asked for
tail -n 40 slurm-<jobid>.out     # or the file you named with --output
```

The output file is the most useful of the three. The last lines usually name the problem: a Python traceback, "command not found", "Killed", or a message from Slurm.

## Reading the exit code {#read-code}

Slurm shows `ExitCode` as two numbers, `code:signal`. `1:0` means your program exited with code 1. `0:9` means it was stopped by signal 9 before it could exit.

| What sacct shows | What it usually means | Go to |
| --- | --- | --- |
| `FAILED`, `1:0` | Your program reported an error | [Exit code 1](#exit-1) |
| `FAILED`, `2:0` | Wrong arguments, a missing script file, or a shell syntax error | [Exit code 2](#exit-2) |
| `FAILED`, `127:0` or `126:0` | A command could not be found or run | [127 and 126](#exit-127) |
| `OUT_OF_MEMORY` | The job used more memory than it asked for | [Out of memory](#oom) |
| `0:9` or `0:15`, or `CANCELLED` | Something stopped the job | [Killed or stopped](#killed) |
| `0:11`, "Segmentation fault" | The program crashed | [Crashed](#segfault) |
| `NODE_FAIL` | The node had a hardware problem | [Node failure](#node-fail) |
| `TIMEOUT` | The job reached its time limit | [Choosing a time limit](choosing-time-limits.md) |

## Exit code 1: the program reported an error {#exit-1}

This is the most common failure by far. It is a general "something went wrong" from your program, so the real reason is in the output file. The usual ones:

- **`ModuleNotFoundError` or `ImportError`**: the job did not load the same software you had when you tested. Put the `module load` and environment activation lines inside the job script, not only in your login session.
- **`FileNotFoundError`**: a path is wrong on the compute node. Use full paths, or check what folder the job starts in with `echo $PWD` at the top of the script.
- **CUDA errors such as "no CUDA-capable device"**: the job did not ask for a GPU. Add `#SBATCH --gpus=1` (or more) and check with `nvidia-smi` as the first line of the work.
- **"CUDA out of memory"**: the GPU's own memory is full, which is different from the node running out of memory. Reduce the batch size or model size, or use mixed precision.

## Exit code 2: usage or syntax error {#exit-2}

The command was given something it did not understand. Common causes: a misspelled option, a missing argument, a script file that is not where the command expects it (`python: can't open file`), or a syntax error in a bash script. Run the same command by hand in a short [interactive session](../nvwulf/gpu-interactive-sessions.md) to see the full message.

## Exit codes 127 and 126: command not found or not runnable {#exit-127}

**127** means the shell could not find the command. The module or environment that provides it was not loaded in the job, the name is misspelled, or the script was saved on Windows (the error then mentions `^M`). Fix Windows line endings with:

```
sed -i 's/\r$//' my_job.slurm
```

**126** means the file was found but could not be run, usually because it is not marked as executable:

```
chmod +x my_program.sh
```

## Out of memory (the node's memory) {#oom}

The state is `OUT_OF_MEMORY`, or the output ends with "oom-kill". The job used more of the node's memory (RAM) than it asked for with `--mem`. Check the peak with `seff <jobid>`, then ask for that much plus a margin of about 20%.

On NVwulf, ask for memory in proportion to the GPUs you use. A B40 node has 512 GB for its 4 GPUs, about 125 GB per GPU. A job that asks for much more than its share can leave the node's other GPUs unusable while it runs.

## Killed or stopped (signals 9 and 15) {#killed}

- **Signal 9 (killed)**: the job was stopped at once. The usual cause is going over a memory limit; check `seff` first. It can also mean an administrator stopped the job, in which case you will normally hear from RCI.
- **Signal 15 (stopped)** or `CANCELLED`: the job was asked to stop, by `scancel` or by Slurm. If you did not cancel it, check whether it reached its time limit.

## Crashed (segmentation fault) {#segfault}

The program tried to use memory it does not own and the system stopped it (signal 11). On a shared cluster this is usually a software mix-up rather than a bug in your code: a program built on another system, or modules from different toolchains loaded together. Start the script with `module purge`, load only what you need, and rebuild compiled code on NVwulf. If it still crashes, send us the job ID.

## Node failure {#node-fail}

The state is `NODE_FAIL`: the node had a hardware or system problem. This is not caused by your job. Resubmit it, and if the same node fails your jobs more than once, open a ticket with the job IDs so the HPC team can check that node. Long jobs that save checkpoints lose the least work when this happens (see [saving progress](choosing-time-limits.md#checkpoint)).

## Anything else {#find-error}

1. Read the end of the output file and the error file, if you set one with `--error`.
2. Search the first error line, not the last one. Later errors are often caused by the first.
3. Rerun the failing step by hand in a short [interactive session](../nvwulf/gpu-interactive-sessions.md) in a debug partition, where you can see what happens.
4. Still stuck? Open a ticket (below).

## Getting help {#help}

Open an HPC ticket and include the cluster, the job ID, the path to your job script and the path to the output file. That is usually enough for us to find the cause without a back and forth. We are also happy to review a job script before a big run.

Related: [Managing jobs](managing-jobs.md) · [Writing job scripts](writing-job-scripts.md) · [Getting started on NVwulf](../nvwulf/getting-started-nvwulf.md)

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/job-failures> (maintained by Research Computing and Informatics).
