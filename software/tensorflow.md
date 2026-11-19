# TensorFlow

An open-source machine learning library for deep learning and AI applications.

TensorFlow is an open-source library for numerical computation and machine learning. It is widely used for developing and training deep learning models in fields such as computer vision, natural language processing, and reinforcement learning. SeaWulf provides CPU and GPU optimized versions allowing users to select based on system requirements and workload demands.

**Module name** `tensorflow`

## Loading TensorFlow

- module `tensorflow-cpu/latest`
- module `tensorflow/1.10`
- module `tensorflow/2.4.1`
- module `tensorflow/2.10`
- module `tensorflow-gpu/latest`
- module `tensorflow2-gpu/2.1.0`
- module `tensorflow2-gpu/2.2.0`
- module `tensorflow2-gpu/2.7.0`
- module `tensorflow-rocm/2.17.0`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load a TensorFlow module**

```
module load tensorflow/2.10
```

## Availability

TensorFlow is available on: SeaWulf, NVwulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/tensorflow> (maintained by Research Computing and Informatics).
{: .rci-credit }
