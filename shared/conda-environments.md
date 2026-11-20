# Conda environments

## Overview

Conda keeps each project's packages in their own environment. Projects can then use different versions without clashing, and your results are easier to repeat. Load Anaconda first:

```
module load anaconda/3
```

## Creating environments

```
# by name (lands in ~/.conda/envs/)
conda create --name myproject python=3.10

# by path (for large environments, e.g. in project space)
conda create --prefix /gpfs/projects/<Group_Name>/envs/myproject python=3.10

# with initial packages (faster than installing later)
conda create --name myproject python=3.10 numpy pandas matplotlib
```

Always specify the Python version. You cannot combine `--name` and `--prefix`.

## Managing environments

```
conda env list                     # list environments
conda activate myproject           # activate by name
conda deactivate                   # back to base
conda env remove --name myproject  # delete
```

## Installing packages

```
conda install numpy scipy matplotlib
conda install -c conda-forge package-name   # conda-forge channel
conda search package-name
```

**Combining conda and pip:** install conda packages first, then use pip only for what conda lacks. Avoid switching back and forth: see [pip vs conda](python-package-management.md).

## Using environments in jobs

```
#!/bin/bash
#SBATCH --job-name=analysis
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH -p short-40core

module load anaconda/3
conda activate myproject

python my_analysis.py
```

## Exporting and sharing

```
conda env export > environment.yml      # snapshot
conda env create -f environment.yml     # recreate anywhere
conda create --name new --clone old     # clone for testing
```

## Storage considerations

| Location | Pros | Cons | Best for |
| --- | --- | --- | --- |
| Home directory (default) | Backed up, persistent | 20 GB limit | Most environments |
| Project space | Shared with group, large capacity | Not backed up | Collaborative or large environments |

!!! warning ""
    **Warning:** never build environments in scratch. Old files there are deleted on a schedule, even while you use them, and the environment will break.

```
du -sh ~/.conda/envs/*   # check environment sizes
conda clean --all        # clear package cache (keeps environments)
```

## Troubleshooting

- **Activation fails**: load the module first with `module load anaconda/3`.
- **Out of quota**: check `myquota`, clean the cache, or move environments to project space.
- **Package conflicts**: make a new environment and install everything at once.
- **PackagesNotFoundError**: try `conda search -c conda-forge package-name`, or pip.
- **Slow to create**: install Python first, then add packages a few at a time.

## Best practices

- One environment per project; always pin the Python version
- Export `environment.yml` before major production runs
- Never install into the base environment
- Test interactively before submitting large jobs; monitor disk usage regularly

**Applies to** <span class="rci-chip">All clusters</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/conda-environments> (maintained by Research Computing and Informatics).
{: .rci-credit }
