# Good conduct on the RCI clusters

Our clusters are shared by hundreds of researchers at once. A few good habits keep SeaWulf, NVwulf, and ClinWulf fast and fair for everyone. Please read this before you run heavy work, and treat it as the ground rules for using RCI's high-performance computing resources.

## Don't run work on the login nodes

When you connect to a cluster you land on a **login node**, a shared gateway used by many people at the same time. Login nodes are for light, interactive tasks only:

- Editing scripts, viewing files, and managing data
- Compiling code and loading modules
- Submitting and monitoring SLURM jobs (`sbatch`, `squeue`)
- Small, short tests

Everything else belongs on a **compute node**. Do not run research applications (MATLAB, R, Python analyses, simulations), large multi-core builds, or long or high-memory processes on a login node. A single heavy process can slow the login node for everyone. For a live shell on a compute node, start an interactive job:

```
srun -p short-40core --pty bash
```

See [Login node etiquette](login-node-etiquette.md) and [Interactive jobs](interactive-jobs.md) for details, and use [job scripts](writing-job-scripts.md) for anything that runs at scale.

> [!NOTE]
> **AI coding tools and IDEs.** Tools like VS Code Remote, Cursor, and AI agents can spawn heavy background processes on the node they connect to. Point them at a compute node (start an interactive job first), not a login node, and remember you are responsible for everything they launch under your account.

## Right-size your jobs and respect fair share

Requesting far more than you use keeps resources idle and pushes back everyone else's jobs. Job priority on our clusters is governed by [fair share](fairshare-job-priority.md), so considerate use also helps your own turnaround.

- Request only the cores, memory, GPUs, and walltime your job needs, and always set a realistic `--time`.
- Send small or single-core work to a [shared partition](../seawulf/shared-nodes.md) instead of holding a whole node.
- Pick the right queue with the [queue selection guide](../seawulf/queue-selection-guide.md), and cancel jobs you no longer need ([managing jobs](managing-jobs.md)).
- Don't leave interactive sessions or GPUs allocated after you're done: type `exit` to release them.
- When checking on jobs, poll gently. Watching `squeue` in a tight loop hammers the scheduler; every few minutes is plenty.

## Be considerate on the shared file systems

All clusters mount the same GPFS file systems. Each has a purpose, a quota, and a backup policy:

| Path | Quota | Backed up? | Use it for |
| --- | --- | --- | --- |
| `/gpfs/home/<netid>` | 20 GB | Yes | Scripts, configs, small files |
| `/gpfs/scratch/<netid>` | 20 TB | No (45-day purge) | Active job input/output |
| `/gpfs/projects/<group>` | Up to 10 TB | No | Shared group data |
| `/gpfs/software` | System | Managed | System applications |

> [!NOTE]
> **Scratch is temporary, and project space is not backed up.** Files on scratch are deleted once they pass 45 days old. Anything irreplaceable needs a second copy somewhere else: see [backing up with Rclone](../seawulf/backing-rclone.md). Keep an eye on your usage with the `myquota` tool ([checking storage quotas](../seawulf/checking-storage-quotas.md)), and read [storage layout & policies](../seawulf/storage-layout-policies.md) for the full picture.

## Keep I/O light

The file systems are shared, so heavy or sloppy input/output slows jobs across the whole cluster. A few habits go a long way:

- Run your job's working files from `/gpfs/scratch`, not from home or project space.
- Avoid writing one file per process, or having many processes read and write the same file at once. Consolidate output where you can.
- Keep data in memory rather than round-tripping to disk when it's feasible.
- For jobs that create lots of tiny temporary files, use the compute node's local disk for that scratch and copy back only the results.

## Move data considerately

Large transfers can saturate a login node and stall everyone's sessions. For anything sizable, use tools built for it: [Globus](../seawulf/globus-file-transfer.md) for large, restartable transfers between institutions, [Rclone](../seawulf/backing-rclone.md) for cloud backups, and the CLI options in [file transfer from the CLI](file-transfer-cli.md). Don't launch giant copies in the foreground on a login node and walk away.

## Protect your account

- Your account is yours alone. Don't share credentials or let others run under your login.
- Keep [DUO two-step](duo-authentication.md) active, and protect any [SSH keys](passwordless-ssh.md) with a strong passphrase.
- Don't try to work around scheduler limits, quotas, or node protections. If a limit is blocking legitimate work, ask us and we'll help.
- Only run work you're authorized to run, and keep regulated data (PHI, controlled data) on the cluster approved for it. ClinWulf is our HIPAA-aligned environment.

## Give credit and stay in touch

Grants and continued investment depend on knowing how our systems support research. Please [acknowledge RCI](https://rci.stonybrook.edu/acknowledge) in publications that used the clusters, and let us know about resulting papers and awards.

> [!NOTE]
> **A note on enforcement.** These are guidelines, not threats, but when a job is genuinely harming the shared environment we may pause or cancel it, and repeated problems can lead to throttled access, so that the clusters stay usable for everyone. We'll always reach out to help you fix the underlying issue.

## Quick reference

#### ✅ Please do

- Use login nodes only for editing, compiling, and job submission
- Run real work on compute nodes via `sbatch` or `srun --pty bash`
- Request only the resources and walltime you need
- Keep working data on scratch and back up anything irreplaceable
- Release interactive sessions and GPUs when you're done

#### 🚫 Please don't

- Run simulations, analyses, or big builds on a login node
- Point AI tools or IDEs at a login node
- Hold whole nodes or GPUs idle, or poll the scheduler in a tight loop
- Rely on scratch for anything you can't lose
- Share your account or work around limits

## When something's wrong

Even experienced users hit snags. Open a ticket at [iacs.supportsystem.com](https://iacs.supportsystem.com), drop into [virtual office hours](https://rci.stonybrook.edu/events), or check the [documentation](https://rci.stonybrook.edu/hpc/docs) and FAQs first: most common issues are already covered. See [when to ask for help](when-ask-help.md) for what to include in a good ticket.

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/hpc-good-conduct> (maintained by Research Computing and Informatics).
