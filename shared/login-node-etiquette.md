# Login node etiquette

## Overview

Login nodes are where everyone signs in to the clusters. Use them only for light work, such as editing files, building code, and starting and checking jobs. Heavy computing should always run on compute nodes.

## Appropriate use

- Edit scripts, look at files and manage data.
- Build code and load modules.
- Submit and check Slurm jobs (`sbatch`, `squeue`).
- Run quick, small tests.

## What to avoid

- Don't run long or heavy work on a login node.
- Don't start work that needs many cores or a lot of memory on a login node.
- Don't leave idle programs running that hold memory or CPU.

## Tips

- Log out when finished
- Use `srun --pty bash` or batch scripts for interactive or large jobs on compute nodes
- Monitor your login-node usage and respect CPU/memory limits
- Contact support via [iacs.supportsystem.com](https://iacs.supportsystem.com/) for job-placement help

!!! note ""
    **Key message:** Login nodes are shared by everyone. Following these rules keeps them fast for everyone.

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/login-node-etiquette> (maintained by Research Computing and Informatics).
{: .rci-credit }
