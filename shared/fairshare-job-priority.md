# Fairshare & job priority

## Overview

The clusters use fairshare to share computing time fairly among all users. Job priority depends on how much you have used lately, how big the job is and how much time it asks for. Knowing how it works helps you wait less and get more done.

## Key concepts

- **Fairshare**: if you have used less of the cluster lately, your jobs get a higher score.
- **Scheduling priority**: the order in which Slurm looks at waiting jobs. It depends on the queue, what you ask for, your time limit and your fairshare.
- **Priority access**: certain queues give specific groups higher scheduling priority when resources are constrained.

## Tips for maximizing throughput

- Submit several small jobs instead of one large job. Small jobs often start sooner.
- Pick queues that match your job's time limit and node needs.
- Spread out your submissions instead of sending many at once.
- Check your place in the queue with `squeue -u <username>` and your fairshare with `sshare -u $USER`.
- Use job arrays for repeated tasks. They are easier on the scheduler.

Right-sized jobs in the right queue start sooner and make better use of the clusters.

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/fairshare-job-priority> (maintained by Research Computing and Informatics).
{: .rci-credit }
