# NVwulf

NVwulf is Stony Brook's GPU cluster for AI and machine learning, with NVIDIA H200 and RTX PRO 6000 Blackwell GPUs. It's open to Stony Brook instructors, researchers, staff and students.

- **141 GB** HBM3e on each H200 GPU
- **96 GB** on each RTX PRO 6000 Blackwell
- **8** GPUs on the largest nodes
- **96** NVIDIA GPUs on 20 nodes

## Get connected {#about}

*In your browser*

### Open OnDemand

Jupyter, RStudio, VS Code, private AI chat, AlphaFold, cryo-EM and imaging apps on GPU nodes. Sign in with your NetID and Duo.

[Launch Open OnDemand](https://nvwulf-ood.nvwulf.stonybrook.edu/)

*From a terminal*

### SSH

NVwulf has its own storage, separate from SeaWulf. Copy data over with `rsync` or Globus.

```
ssh -X <netid>@login.nvwulf.stonybrook.edu
```

Your first hour, step by step: [Getting started on NVwulf](getting-started-nvwulf.md).

## Specifications

| Node type | Details |
| --- | --- |
| H200 nodes (4-way) | 4 NVIDIA H200 NVL (141 GB HBM3e each), 64 CPUs, about 750 GB RAM |
| H200 nodes (8-way NVL) | 8 NVIDIA H200 NVL, 64 CPUs, about 1,500 GB RAM |
| H200 nodes (8-way SXM) | 8 NVIDIA H200 SXM, 192 CPUs, about 2,200 GB RAM |
| B40 nodes (4-way) | 4 NVIDIA RTX PRO 6000 Blackwell (96 GB GDDR7 each), 64 CPUs, about 512 GB RAM |
| Size | 20 GPU nodes with 96 GPUs: 48 H200 (four nodes with 4 and four with 8) and 48 RTX PRO 6000 Blackwell (12 B40 nodes with 4) |
| Scheduling | Multi-tenant Slurm, up to 8 GPUs per node |

## Queues

| Partition | GPUs | Good to know |
| --- | --- | --- |
| `h200x4` | 4 H200 NVL per node | Also `-long` and `debug-` versions |
| `h200x8` | 8 H200 per node | For the largest models and multi-GPU training |
| `b40x4` | 4 RTX PRO 6000 per node | Open OnDemand apps run here: up to 8 hours, or 48 on `b40x4-long` |

Start with a `debug-` partition for short tests, and ask only for the GPUs you'll use. Every queue's CPUs, memory and time limit, and the priority queues, are on [NVwulf queues](nvwulf-queues.md).

Need more GPUs than NVwulf has? [Empire AI](https://rci.stonybrook.edu/ai#empire-ai) and the [SUNY AI Platform](https://rci.stonybrook.edu/ai#suny-ai) are compared on [AI for Research](https://rci.stonybrook.edu/ai).

## Your first GPU job

```
#!/bin/bash
#SBATCH --job-name=test-tf
#SBATCH --output=res.txt
#SBATCH --partition=h200x4
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem=25g
#SBATCH --gpus=1
#SBATCH --time=05:00
module load tensorflow/2.19.0
python tf_test_nn_training.py
```

Save it as `test_job.slurm`, then run `sbatch test_job.slurm` and `squeue -u $USER`. Or build one with the [job script builder](https://rci.stonybrook.edu/hpc/script-builder).

## Storage

| Space | Size | Backed up | Good to know |
| --- | --- | --- | --- |
| Home `/lustre/nvwulf/home/<netid>` | 20 GB | Yes | Never deleted |
| Scratch `/lustre/nvwulf/scratch/<netid>` | 20 TB | No | Files older than 30 days are deleted |

## Popular apps in your browser

- [Jupyter](../shared/jupyter-notebooks.md)
- [AlphaFold](ondemand-protein-prediction.md)
- [LLM Chat](ondemand-llm-chat.md)
- [CryoSPARC](ondemand-cryosparc.md)
- [Napari](ondemand-napari.md)
- [QuPath](ondemand-qupath.md)
- [RStudio](../shared/rstudio.md)
- [ParaView](../shared/ondemand-paraview.md)
- [All 19 apps](nvwulf-ondemand-apps.md)

!!! note ""
    **No patient data.** NVwulf, including its AI chat apps, isn't approved for PHI. Work with PHI belongs on [ClinWulf](https://rci.stonybrook.edu/hpc/clusters/clinwulf).

## Best suited for

- AI and machine learning
- Biomedical imaging
- Molecular modeling and NLP
- Scientific computing and data science

## Getting access

1. **Join a project** If your PI already has an active SeaWulf or NVwulf project, open a ticket with the help topic "Request an Account for NVwulf" and include your NetID, your PI's name and the project number.

    [Getting access to NVwulf](getting-access-nvwulf.md)

2. **Or start one (faculty)** Send a one-page PDF with the help topic "Request a Project Number – NVwulf". A review committee replies by email.
3. **Set up Duo, then log in** Then move your data over and run a first GPU job.
    - [Duo setup](../shared/duo-authentication.md)
    - [Getting started on NVwulf](getting-started-nvwulf.md)

## Related guides

- [Getting started on NVwulf](getting-started-nvwulf.md)
- [Open OnDemand apps on NVwulf](nvwulf-ondemand-apps.md)
- [Connecting to the cluster](../shared/connecting-cluster.md)
- [Using modules](../shared/using-modules.md)
- [Good conduct on the RCI clusters](../shared/hpc-good-conduct.md)
- [Job script builder](https://rci.stonybrook.edu/hpc/script-builder)

Other clusters

## Also available

Cluster**SeaWulf**

General purpose

The general-purpose workhorse: CPU, high-memory and A100 GPU nodes.

[View cluster →](../seawulf/README.md)

Cluster**ClinWulf**

HIPAA

HIPAA-compliant computing for IRB-approved research on PHI.

[View cluster →](https://rci.stonybrook.edu/hpc/clusters/clinwulf)

Cluster**SecureWulf**

Coming Christmas 2026

Secure computing for controlled-access research data.

[View cluster →](https://rci.stonybrook.edu/hpc/clusters/securewulf)

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/clusters/nvwulf> (maintained by Research Computing and Informatics).
{: .rci-credit }
