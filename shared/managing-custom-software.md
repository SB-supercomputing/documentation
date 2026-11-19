# Managing custom software

## Five ways to get software

1. **System modules (recommended).** Check first: `module avail software-name`, then `module load software-name/version`.
2. **Conda environments.** Best for Python and data science packages such as numpy, pandas, TensorFlow and PyTorch. See [Conda environments](conda-environments.md).
3. **Python venv.** Best for lightweight Python projects without compiled dependencies.
4. **Install from source.** Use this when the software isn't a module or a package, or when you need to build it your own way. See [Installing from source](../seawulf/installing-source.md).
5. **Request a system-wide install.** Submit at [iacs.supportsystem.com](https://iacs.supportsystem.com/) for multi-user needs.

## Where to install

| Location | Quota | Backed up | Persistent | Best for |
| --- | --- | --- | --- | --- |
| Home `/gpfs/home/` | 20 GB | Yes | Yes | Personal tools, small apps |
| Project `/gpfs/projects/` | Large | No | Yes | Shared tools, group use |
| Scratch `/gpfs/scratch/` | 20 TB | No | No (45-day purge) | Temp files ONLY |

> [!IMPORTANT]
> Don't install software in scratch. Files there are deleted after 45 days, even if you still use them, and your software will stop working.

## Best practices

- Keep each tool in a folder named for what it does and its version, for example under `$HOME/software/`.
- Check your quota often with `myquota`, and clean the conda cache with `conda clean --all`.
- Write down how you installed each tool and what it needs.
- Set group permissions with `chmod` on software you share.

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/managing-custom-software> (maintained by Research Computing and Informatics).
