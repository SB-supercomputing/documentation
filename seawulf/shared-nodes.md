# Shared nodes

Shared queues allow multiple users to run jobs on the same node simultaneously. Unlike exclusive nodes, they make efficient use of hardware when your job doesn’t need a whole node, and queue waits are often shorter when you request only what you need. All shared queues are reached through the `milan1` / `milan2` login nodes.

## CPU shared queues

**Intel Skylake: 40 cores, 192 GB per node**

- `short-40core-shared`: 1 h default / 4 h max
- `long-40core-shared`: 8 h default / 24 h max
- `extended-40core-shared`: 8 h default / 3.5 days max

**AMD EPYC Milan: 96 cores, 256 GB per node**

- `short-96core-shared`: 1 h default / 4 h max
- `long-96core-shared`: 8 h default / 24 h max
- `extended-96core-shared`: 8 h default / 3.5 days max

## GPU shared queues

Intel Ice Lake nodes: 64 cores and 4× NVIDIA A100 per node:

- `a100`: 1 h default / 8 h max · up to 2 nodes, 2 simultaneous jobs per user
- `a100-long`: 8 h default / 2 days max · 1 node, 2 simultaneous jobs
- `a100-large`: 1 h default / 8 h max · up to 4 nodes, 1 simultaneous job

## Request memory explicitly

The critical difference from exclusive queues: you share the node’s memory with other jobs, so you must say how much you need:

```
#SBATCH --mem=<amount>
```

!!! note ""
    **Why it matters:** without an explicit request your job can exceed the memory available on a shared node and fail, or crowd out other users’ jobs.

## Best practices

- Check the queue’s per-user limits before submitting.
- Monitor your jobs with `squeue -u $USER`.
- Request cores and memory precisely: smaller, well-sized requests schedule faster.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/shared-nodes> (maintained by Research Computing and Informatics).
{: .rci-credit }
