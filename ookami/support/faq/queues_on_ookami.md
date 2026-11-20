# Ookami Queues / Partitions

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

There are several queues available on Ookami. The queues are managed by the Slurm scheduling software. Six of the eight Ookami queues use the same 48 core A64FX nodes so your choice among these queues depends on the length of time needed to run your job. The milan-64core provides acess to a single AMD Rome node (64 cores) with 512GB memory and the skylake-36core queue provides access to a single Intel Skylake node (36 cores) with 192 GB memory.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Queue** | **Time Limit** | **Min Nodes** | **Max Nodes** | **CPU Architecture** |
| short | 4 hours | 1 | 32 | A64FX |
| medium | 12 hours | 8 | 40 | A64FX |
| large | 8 hours | 24 | 80 | A64FX |
| long | 2 days | 1 | 8 | A64FX |
| extended | 7 days | 1 | 2 | A64FX |
| all-nodes | 4 hours | 81 | 174 | A64FX |
| milan-64core | 1 day | 1 | 1 | AMD Milan |
| skylake-36core | 1 day | 1 | 1 | Intel Skylake |

You can also check the queues using

```
sinfo -s
```

Note that slurm has to be loaded.

To enable a fair use of the cluster there are two restrictions in place:

- The maximum number of nodes a user can use at the same time is 120 (the all-nodes queue is excluded from this restriction to allow for full system runs)
- The maximum number of nodes a user can use at the same time in the extended queue is 28.

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/queues_on_ookami.php`, retrieved November 5, 2026.
{: .archive-credit }
