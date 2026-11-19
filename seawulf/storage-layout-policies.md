# Storage layout & policies

SeaWulf gives you several places to keep files, each with a different size limit, backup policy, and purpose. Knowing which is which keeps your work safe and your jobs fast.

**On this page:** [Storage areas](#areas) · [What goes where](#where) · [Keep your data safe](#safe) · [Request project space](#project) · [Check your usage](#check)

## Storage areas {#areas}

| Path | Size limit | File limit | Backed up? | How long files stay | Use it for |
| --- | --- | --- | --- | --- | --- |
| `/gpfs/home/<netid>` | 20 GB | about 200,000 | Yes | Kept | Scripts, settings, small files, software you install |
| `/gpfs/scratch/<netid>` | 20 TB | 10 million | No | Files older than 45 days are deleted | Job input and output while you're working on it |
| `/gpfs/projects/<group>` | Up to 10 TB | about 10 million | No | Until the project ends | Data your group shares |
| `/gpfs/software/` | Managed by RCI |  |  | Kept | System-wide software (read only) |

All of these are the same on every login and compute node, so a file you save in one place is there for all your jobs.

## What goes where {#where}

- **Home** is small but backed up. Keep code, job scripts, configuration, and anything you'd hate to lose here.
- **Scratch** is huge and fast but temporary. Run jobs here, then copy the results you want to keep somewhere safe. Never install software in scratch, since the purge will break it.
- **Project space** is shared with your group and lasts for the life of the project, but it isn't backed up.

## Keep your data safe {#safe}

!!! note ""
    **Only home is backed up.** Scratch is purged by file age, and project space has no backup. Keep a second copy of anything irreplaceable, for example in Stony Brook BOX. See [Backing up with rclone](backing-rclone.md).

To move data on and off the cluster, see [File transfer from the CLI](../shared/file-transfer-cli.md) or, for large datasets, [Globus](globus-file-transfer.md).

## Request project space {#project}

PIs can ask for shared project space when they request a project, or later through a ticket at [iacs.supportsystem.com](https://iacs.supportsystem.com/). Include:

- how much space you need,
- what the data is and how it will be used,
- how long you'll need it, and
- confirmation that your group understands project space isn't backed up.

Requests up to 10 TB are routine. Larger requests need a detailed justification and may be granted for a limited time. For long-term or archival storage, see the [Research Storage picker](https://rci.stonybrook.edu/storage).

## Check your usage {#check}

```
myquota                  # space and file counts for home and scratch
du -sh * | sort -h       # what's using space in the current folder
```

More in [Checking storage quotas](checking-storage-quotas.md). If you hit a limit, jobs can fail with "Disk quota exceeded", so check before big runs.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/storage-layout-policies> (maintained by Research Computing and Informatics).
{: .rci-credit }
