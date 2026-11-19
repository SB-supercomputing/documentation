# Python package management

## Choosing a tool

Use conda for most science work. Use venv for small projects. Use pip only to add packages to an environment you already have.

| Tool | Primary purpose | Key benefits | Sample command |
| --- | --- | --- | --- |
| **Conda** (recommended) | Scientific work with substantial dependencies | Precompiled binaries, cross-language, environment export | `conda create -n myenv python=3.10` |
| **venv** | Smaller projects, personal utilities | Uses system Python, built into Python 3 | `python3 -m venv myenv` |
| **pip** | Adding packages to an existing environment | Straightforward, broadly compatible | `pip install requests` |

> [!NOTE]
> **Avoid:** don't use `pip install --user`. It puts packages straight into your home folder. Use a conda or venv environment instead, so each project stays separate.

## Conda workflow

```
module load anaconda/3
conda create -n analysis python=3.10
conda activate analysis
conda install numpy scipy matplotlib
```

## venv workflow

```
python3 -m venv myenv
source myenv/bin/activate
pip install numpy scipy matplotlib
```

## Recommendations

- Load anaconda before you work with any environment.
- Keep environments in your `$HOME` or project folder.
- Export your environment so others can rebuild it: `conda env export > environment.yml`
- Try not to mix pip and conda in one environment.

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/python-package-management> (maintained by Research Computing and Informatics).
