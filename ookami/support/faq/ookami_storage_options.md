# Ookami storage policies

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

There is a 0.8 Pbyte high-performance, Lustre file system, which is divided into home, project, and scratch areas. The home and project areas are backed up daily.

## Home Directory

- All users on Ookami have their own home directory which is accessible only by them. The default size is 20 Gbyte, but an increase can be requested.

---

## Scratch Directory

- The scratch directory has no quota, but has a policy of deleting files older than 20 days. There is a limit on the total number of files a user can create per directory. **This space is NOT backed up.**

---

## Project Space

- Upon request from the project's PI, each project will be granted a shared (project) directory, accessible only to project members. The default is 1TB, which can be increased to multiple terabytes. Project directories larger than 5 TB will have to renew their requests annually and be prepared to move their data if space becomes limited. Large project directories may not be backed up.

---

## Summary

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Location** | **Size** | **Backed Up?** | **Shareable?** | **Cleared?** |
| /lustre/home/&lt;netid> | 20GB | Yes | No | never |
| /lustre/scratch/&lt;netid> | 20TB | No | No | 30 days |
| /lustre/projects/&lt;your_group>\* | up to 5TB | Yes\*\* | Yes | per request |

\*Project directories are granted upon request from the group's PI

\*\*Some large project directories may not be backed up

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/ookami_storage_options.php`, retrieved November 5, 2026.
{: .archive-credit }
