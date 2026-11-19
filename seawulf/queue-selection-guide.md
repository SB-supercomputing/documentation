# Queue selection guide

Every SeaWulf job runs in a queue (also called a partition). The queue decides which kind of node you get, how long the job may run, and how many nodes it can use. Pick the smallest, shortest queue that fits your job and it will usually start sooner.

**On this page:** [How long can a job run](#walltime) · [Quick picks](#pick) · [How to choose](#tips) · [Limits per person](#tips) · [40-core Skylake](#40) · [96-core Milan](#96) · [HBM](#hbm) · [A100 GPU](#a100)

> [!NOTE]
> **Where you log in matters.** The 40-core, 96-core, HBM, and A100 queues are reached from `milan.seawulf.stonybrook.edu` (or `xeonmax`). The 28-core Haswell nodes and the older K80, P100 and V100 GPU nodes were retired in November 2026. See [Which SeaWulf login node?](../shared/connecting-cluster.md#login-nodes)

## How long can a job run? (maximum walltime) {#walltime}

The longest a single job can run depends on the cluster and the queue.

| Cluster | Longest run | Queues |
| --- | --- | --- |
| **SeaWulf (CPU)** | 7 days | `extended-40core`, `extended-96core` and `hbm-extended-96core`, up to 2 nodes. Their `-shared` versions allow 3.5 days, and the long queues 48 hours. |
| **SeaWulf (A100 GPUs)** | 48 hours | `a100-long`, 1 node. `a100` and `a100-large` allow 8 hours. |
| **NVwulf (H200 and RTX PRO 6000 GPUs)** | 48 hours | The `-long` queues: `h200x4-long`, `h200x8-long` and `b40x4-long`. Standard queues allow 8 hours and `debug-` queues 1 hour. See [NVwulf queues](../nvwulf/nvwulf-queues.md). |
| **ClinWulf** | 10 days | The "extra" queues. The long queues allow 8 hours. See [Open OnDemand apps on ClinWulf](https://rci.stonybrook.edu/docs/clinwulf-ondemand-apps). |

Ask for the time your job needs plus a margin; shorter requests usually start sooner. If your work needs longer than the limit, save checkpoints so a new job can pick up where the last one stopped, or [ask HPC support](https://rci.stonybrook.edu/hpc/support) about options. To check a queue's limit on the cluster, run `module load slurm` and then `sinfo -p <queue> -o "%P %l"`.

## Quick picks {#pick}

| Your job | Try this queue |
| --- | --- |
| A quick test (under 1 hour) | `debug-40core` |
| A few cores, doesn't need a whole node | `short-40core-shared` or `short-96core-shared` |
| Whole nodes, up to 4 hours | `short-40core` or `short-96core` |
| Up to 12 hours | `medium-40core` or `medium-96core` |
| Up to 2 days | `long-40core` or `long-96core` |
| Up to 7 days, 1 to 2 nodes | `extended-40core` or `extended-96core` |
| Many nodes at once (up to 8 hours) | `large-40core` or `large-96core` |
| Limited by memory speed | an [HBM queue](#hbm) |
| Needs a GPU | `a100` (or NVwulf for large AI work, see [Getting started on NVwulf](../nvwulf/getting-started-nvwulf.md)) |

## How to choose {#tips}

- **Start small.** Run a short test to learn how much time and memory your job really needs.
- **Ask for what you'll use.** Smaller requests usually start sooner.
- **Use shared queues** for jobs that don't need a whole node. On shared queues, always set `--mem`; on the others, you get all of each node's memory automatically.
- **Check the architecture.** Make sure your software was built for the node type (Skylake, Milan, Sapphire Rapids, or GPU).
- **See how busy a queue is** with `sinfo -p <queue>`, after `module load slurm`.

In the tables, **Time** is the range of run times each queue is meant for; the upper number is the maximum you can request.

> [!NOTE]
> **Limits per person.** On SeaWulf you can use up to 32 nodes at once across all your running jobs, unless you're using one of the `large` queues, and you can have up to 100 jobs in the queue at one time.

## 40-core Intel Skylake {#40}

AVX-512 support, 192 GB memory per node. Reached from the milan login nodes.

| Queue | Time | Max nodes | Shared | Best for |
| --- | --- | --- | --- | --- |
| `debug-40core` | 1 hr | 8 | No | Testing and debugging |
| `short-40core` | 1 to 4 hr | 8 | No | Standard jobs |
| `short-40core-shared` | 1 to 4 hr | 4 | Yes | Smaller jobs |
| `medium-40core` | 4 to 12 hr | 16 | No | Medium jobs |
| `long-40core` | 8 to 48 hr | 6 | No | Long jobs |
| `long-40core-shared` | 8 to 24 hr | 3 | Yes | Shared long jobs |
| `extended-40core` | 8 hr to 7 days | 2 | No | Very long jobs |
| `extended-40core-shared` | 8 hr to 3.5 days | 1 | Yes | Shared extended jobs |
| `large-40core` | 4 to 8 hr | 50 | No | Large parallel jobs |

## 96-core AMD EPYC Milan {#96}

AVX2 support, 256 GB memory per node. Reached from the milan login nodes.

| Queue | Time | Max nodes | Shared | Best for |
| --- | --- | --- | --- | --- |
| `short-96core` | 1 to 4 hr | 8 | No | Parallel jobs |
| `short-96core-shared` | 1 to 4 hr | 4 | Yes | Moderate shared jobs |
| `medium-96core` | 4 to 12 hr | 16 | No | Parameter sweeps |
| `long-96core` | 8 to 48 hr | 6 | No | Long parallel jobs |
| `long-96core-shared` | 8 to 24 hr | 3 | Yes | Shared long jobs |
| `extended-96core` | 8 hr to 7 days | 2 | No | Very long jobs |
| `extended-96core-shared` | 8 hr to 3.5 days | 1 | Yes | Shared extended jobs |
| `large-96core` | 4 to 8 hr | 38 | No | Large parallel jobs |

## High-bandwidth memory (HBM) nodes {#hbm}

Intel Sapphire Rapids with AMX and AVX-512, 384 GB per node (256 GB DDR5 plus 128 GB HBM). Best for work limited by how fast data moves in and out of memory. Reached from the milan or xeonmax login nodes.

| Queue | Time | Max nodes | Notes | Best for |
| --- | --- | --- | --- | --- |
| `hbm-short-96core` | 1 to 4 hr | 8 | High-bandwidth memory | Memory-intensive jobs |
| `hbm-medium-96core` | 4 to 12 hr | 16 | Faster memory | Large datasets |
| `hbm-long-96core` | 8 to 48 hr | 6 | 2 to 4 times faster memory | Memory-bound simulations |
| `hbm-extended-96core` | 8 hr to 7 days | 2 | Longest HBM runs | Long memory-bound jobs |
| `hbm-large-96core` | 4 to 8 hr | 38 | Many HBM nodes at once | Very large memory-bound jobs |
| `hbm-1tb-long-96core` | 8 to 48 hr | 1 | 1 TB memory plus 128 GB HBM cache | Extremely large datasets |

## NVIDIA A100 GPU nodes {#a100}

Four A100 80 GB GPUs per node, on 64-core Intel Ice Lake nodes with 256 GB memory. Request GPUs with `--gres=gpu:N`, and check that your software supports CUDA first. These queues are shared.

| Queue | Time | Max nodes | Best for |
| --- | --- | --- | --- |
| `a100` | 1 to 8 hr | 2 | GPU workloads, AI and ML |
| `a100-long` | 8 to 48 hr | 1 | Long GPU jobs |
| `a100-large` | 1 to 8 hr | 4 | Multi-node GPU jobs |

## Related

- [Shared nodes](shared-nodes.md): how the shared queues work and how to size memory.
- [Writing job scripts](../shared/writing-job-scripts.md) and the [job script builder](https://rci.stonybrook.edu/hpc/script-builder).
- [Fairshare & job priority](../shared/fairshare-job-priority.md): why some jobs start before others.
- [Cluster picker](https://rci.stonybrook.edu/hpc/cluster-picker): whether SeaWulf, NVwulf, or ClinWulf fits best.

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/queue-selection-guide> (maintained by Research Computing and Informatics).
