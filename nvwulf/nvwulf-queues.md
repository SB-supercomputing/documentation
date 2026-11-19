# NVwulf queues

NVwulf has three kinds of GPU node, and each has a standard queue, a `-long` queue and, for two of them, a `debug-` queue for quick tests. Every NVwulf node is shared: several people's jobs can run on the same node, so ask for exactly the GPUs, CPUs and memory you need.

**On this page:** [Queues and limits](#queues) · [Default CPUs and memory](#defaults) · [Priority queues](#priority)

## Queues and limits {#queues}

| Queue | GPU | GPUs per node | CPUs per node | Host memory | Longest run | Max nodes |
| --- | --- | --- | --- | --- | --- | --- |
| `debug-h200x4` | H200 NVL, 141 GB | 4 | 64 (62 usable) | about 750 GB | 1 hour | 1 |
| `debug-b40x4` | RTX PRO 6000 Blackwell, 96 GB | 4 | 64 (62 usable) | about 512 GB | 1 hour | 1 |
| `h200x4` | H200 NVL | 4 | 64 (62 usable) | about 750 GB | 8 hours | 2 |
| `h200x4-long` | H200 NVL | 4 | 64 (62 usable) | about 750 GB | 48 hours | 1 |
| `h200x8` | H200 NVL | 8 | 64 (62 usable) | about 1,500 GB | 8 hours | 1 |
| `h200x8-long` | H200 NVL | 8 | 64 (62 usable) | about 1,500 GB | 48 hours | 1 |
| `b40x4` | RTX PRO 6000 Blackwell | 4 | 64 (62 usable) | about 512 GB | 8 hours | 2 |
| `b40x4-long` | RTX PRO 6000 Blackwell | 4 | 64 (62 usable) | about 512 GB | 48 hours | 1 |

Start with a `debug-` queue for short tests. Open OnDemand apps on NVwulf run in these same queues; see [Open OnDemand apps on NVwulf](nvwulf-ondemand-apps.md).

## Default CPUs and memory {#defaults}

If you don't ask for CPUs or memory, Slurm gives your job a default based on the number of GPUs you request. To see the defaults and limits for a queue, run:

```
scontrol show partition h200x4
```

To list every queue you can use with its time limit:

```
sinfo -o "%P %l %D"
```

## Priority queues {#priority}

Users and groups with a dedicated allocation on NVwulf also have priority queues. They run on the same kinds of hardware with the same limits as the standard queue they mirror, but their jobs are scheduled ahead of general jobs:

- `p-h200x4` and `p-h200x4-long`
- `p-h200x8` and `p-h200x8-long`
- `p-b40x4` and `p-b40x4-long`
- `p-h200x8-03-long`: 8 H200 SXM GPUs, 48 hours

To ask about a dedicated allocation, [contact HPC support](https://rci.stonybrook.edu/hpc/support).

**Related:** [Getting started on NVwulf](getting-started-nvwulf.md) · [Fairshare and job priority](../shared/fairshare-job-priority.md) · [How long can a job run?](../seawulf/queue-selection-guide.md#walltime) · [NVwulf](README.md)

**Applies to** <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/nvwulf-queues> (maintained by Research Computing and Informatics).
{: .rci-credit }
