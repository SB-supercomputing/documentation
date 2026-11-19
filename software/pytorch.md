# PyTorch

An open-source machine learning framework used for computer vision and NLP.

PyTorch is an open-source machine learning framework widely used for deep learning research and production. It provides flexibility and speed when building complex neural networks, especially in research areas such as computer vision and natural language processing. SeaWulf provides multiple PyTorch versions supporting both CPU and GPU configurations.

**Module name** `pytorch-gpu`

## Loading PyTorch

- module `pytorch-gpu/2.0.1 (latest GPU)`
- module `pytorch-gpu/latest`
- module `pytorch-cpu/latest`
- module `pytorch-latest/1.13.0`
- module `pytorch/1.4.0`
- module `pytorch-lightning/2.1.3`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load a PyTorch module**

```
module load pytorch/1.4.0
```

## Availability

PyTorch is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/pytorch> (maintained by Research Computing and Informatics).
{: .rci-credit }
