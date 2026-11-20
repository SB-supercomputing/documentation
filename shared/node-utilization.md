# Node utilization

## Overview

Efficient use of compute nodes ensures fair access for all users and maximizes throughput: proper resource management prevents waste and benefits the whole community.

## Recommendations

- **Use shared queues** whenever feasible so multiple jobs can run on the same nodes
- **Request only what you need**: cores, nodes, memory, and GPUs your job will actually use
- **Allocate full nodes for interactive sessions only when all cores will be used**; otherwise pick a shared queue to avoid idle cores
- **Monitor consumption**: track memory, CPU, and GPU usage (see [managing jobs](managing-jobs.md))
- **Optimize code**: faster completion frees resources for others
- **Release nodes promptly** after job completion

## Summary

Prioritize shared queues, monitor jobs closely, and review the [queue tables](../seawulf/queue-selection-guide.md) before submission. These practices work alongside [fairshare and job priority](fairshare-job-priority.md) to keep workflows predictable and efficient.

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/node-utilization> (maintained by Research Computing and Informatics).
{: .rci-credit }
