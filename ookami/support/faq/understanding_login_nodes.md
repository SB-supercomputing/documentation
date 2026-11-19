# Understanding the Login Nodes

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Connecting to Ookami will now round robin users between login1 and login2 (both are ThunderX2). The login nodes provide an external interface to the Ookami computing cluster. They are for preparing submission scripts for the batch queue, submitting and monitoring jobs in the batch queue, analyzing results, and moving data. It is NOT appropriate for running computational jobs or compiling software. To do this use one of the compute queues. If necessary, you can [request an interactive session](interactive_slurm_session.md) by following the guide in our FAQ.

Optionally, users connect from the login node to one of the two debug nodes that have aarch64 architecture and are useful for compiling code that will be run on the compute nodes. To connect to them use ssh fj-debug1 or ssh fj-debug2. The login and the debug nodes are:

|  |  |  |
| --- | --- | --- |
| **Node Name** | **CPU model** | **Architecture** |
| login1 | ThunderX2 | aarch64 |
| login2 | ThunderX2 | aarch64 |
| fj-debug1 | A64FX | aarch64 |
| fj-debug2 | A64FX | aarch64 |

If you have an account on the cluster, you can access a login node via ssh: see [Logging in to Ookami](logging-into-ookami.md).

For more information about submitting slurm jobs, see [How can I submit a slurm job?](submit-delete-check-slurm-jobs.md)

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/understanding_login_nodes.php`, retrieved November 5, 2026.
{: .archive-credit }
