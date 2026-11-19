# Choosing a time limit

Every job asks for a time limit with `--time`. Slurm uses it to plan: it reserves your resources for that long and fits shorter jobs into the gaps. Ask for far too much and your job waits longer than it needs to, and so does everyone else's. Ask for too little and Slurm stops the job before it finishes. This page shows how to pick a limit from your own past jobs.

**On this page:** [Why it matters](#why) · [Look at your past jobs](#history) · [A simple rule](#rule) · [How to write it](#format) · [Partition limits](#limits) · [Long jobs: save progress](#checkpoint)

## Why it matters {#why}

- **Shorter requests often start sooner.** When a big job is waiting for a node to free up, Slurm lets smaller jobs run first if they will finish in time. This is called backfill, and it depends on your limit, not your real run time.
- **Running out of time wastes the whole run** unless your program saves its progress. The job ends with the state `TIMEOUT`.
- **A good limit is close to the real run time, with a margin.** Jobs that use under a quarter of what they asked for, and jobs that keep hitting the limit, both point to a limit worth changing.

## Look at your past jobs {#history}

After `module load slurm`, this lists your jobs from the last 30 days with the time each one used and the limit it asked for:

```
sacct -u $USER -S now-30days -X --format=JobID,JobName%20,Partition,Elapsed,Timelimit,State
```

Compare `Elapsed` with `Timelimit` for jobs of the same kind. For one finished job, `seff <jobid>` shows the same along with memory and CPU use.

## A simple rule {#rule}

1. Find the longest recent run of this kind of job.
2. Add about 25% for slow nodes, busy file systems and bigger inputs.
3. Round up to a tidy number, and stay within the partition's limit.

Example: training runs took between 3 hours 10 minutes and 4 hours. Ask for 5 hours (`--time=05:00:00`), not the 48 hours a long partition allows.

For a new job with no history, run a short test (a few steps or a small input), time it, and scale up. The first run can ask for a generous limit; tighten it once you know.

## How to write it {#format}

| You write | Slurm reads |
| --- | --- |
| `--time=30` | 30 minutes |
| `--time=02:30:00` | 2 hours 30 minutes |
| `--time=1-12:00:00` | 1 day 12 hours |

To change the limit of a job that is still waiting, use `scontrol update JobId=<jobid> TimeLimit=04:00:00`. You can lower the limit of a running job, but only administrators can raise it.

## Partition limits {#limits}

The partition you choose sets the longest limit you can ask for. On NVwulf:

| Partitions | Longest limit | Use for |
| --- | --- | --- |
| `debug-h200x4`, `debug-b40x4` | 1 hour | Tests and quick fixes |
| `h200x4`, `h200x8`, `b40x4` | 8 hours | Most jobs |
| The `-long` versions | 48 hours | Runs that truly need more than 8 hours |

Full details are in [NVwulf queues](../nvwulf/nvwulf-queues.md). For SeaWulf, see the [queue selection guide](../seawulf/queue-selection-guide.md).

## Long jobs: save progress {#checkpoint}

A job that saves its progress (a checkpoint) every so often can pick up where it left off after a time limit or a [node failure](job-failures.md#node-fail). It can also be split into several shorter jobs, which often start sooner than one long one. Most training frameworks can save and resume checkpoints; set it to save every 30 to 60 minutes, then have the job script resume when a checkpoint exists:

```
if [ -f checkpoint.pt ]; then
  python train.py --resume checkpoint.pt   # carry on from the last save
else
  python train.py                          # first run
fi
```

Chain the parts so each starts when the one before it ends:

```
jid=$(sbatch --parsable train.slurm)
sbatch --dependency=afterany:$jid train.slurm
```

Related: [Writing job scripts](writing-job-scripts.md) · [Managing jobs](managing-jobs.md) · [GPU interactive sessions](../nvwulf/gpu-interactive-sessions.md) · [Job script builder](https://rci.stonybrook.edu/hpc/script-builder)

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/choosing-time-limits> (maintained by Research Computing and Informatics).
