# SeaWulf

SeaWulf is Stony Brook's general-purpose cluster: more than 200 CPU nodes, high-bandwidth and high-memory nodes, and A100 GPUs, open to the campus community and Brookhaven Lab staff.

- **228** compute nodes
- **18,152** CPU cores
- **44** NVIDIA A100 GPUs
- **1 TB** RAM on the largest nodes

## Get connected {#about}

*In your browser*

### Open OnDemand

Jupyter, RStudio, MATLAB, a full desktop and 14 more apps, with nothing to install. Sign in with your NetID and Duo.

[Launch Open OnDemand](https://sn-ood.seawulf.stonybrook.edu/)

*From a terminal*

### SSH

The milan login nodes reach most queues. Use `xeonmax` for the HBM nodes.

```
ssh <netid>@milan.seawulf.stonybrook.edu
```

Windows setup, Duo tips and every login address: [Connecting to the cluster](../shared/connecting-cluster.md).

## Specifications

| Node type | Details |
| --- | --- |
| 40-core Intel Skylake | 192 GB memory per node, AVX-512 |
| 96-core AMD EPYC Milan | 256 GB memory per node, AVX2 |
| High-bandwidth memory | Intel Sapphire Rapids, 256 GB DDR5 plus 128 GB HBM (one 1 TB node) |
| A100 GPU nodes | 4 NVIDIA A100 80 GB GPUs per node, 64-core Ice Lake, 256 GB memory |
| High-memory nodes | 4 nodes with about 1 TB RAM |
| Size | 228 nodes and 18,152 CPU cores (after the November 2026 retirement of the 28-core Haswell, K80, P100 and V100 nodes) |

## Which queue?

| Your job | Try this queue |
| --- | --- |
| A quick test, under 1 hour | `debug-40core` |
| A few cores, not a whole node | `short-40core-shared` or `short-96core-shared` |
| Whole nodes, up to 4 hours | `short-40core` or `short-96core` |
| Up to 12 hours | `medium-40core` or `medium-96core` |
| Up to 2 days | `long-40core` or `long-96core` |
| Up to 7 days, 1 to 2 nodes | `extended-40core` or `extended-96core` |
| Needs a GPU | `a100`, or NVwulf for large AI work |

Every queue, its limits and where to submit it from: [Queue selection guide](queue-selection-guide.md). Or let the [job script builder](https://rci.stonybrook.edu/hpc/script-builder) write the script.

## Storage

| Space | Size | Backed up | Good to know |
| --- | --- | --- | --- |
| Home `/gpfs/home/<netid>` | 20 GB | Yes | Scripts, settings and small files |
| Scratch `/gpfs/scratch/<netid>` | 20 TB | No | Files older than 45 days are deleted |
| Project `/gpfs/projects/<group>` | Up to 10 TB | No | Shared by your group, on request |

Details and how to ask for project space: [Storage layout & policies](storage-layout-policies.md).

## Popular apps in your browser

- [Jupyter](../shared/jupyter-notebooks.md)
- [RStudio](../shared/rstudio.md)
- [MATLAB](matlab-open-ondemand.md)
- [VS Code](../shared/code-server.md)
- [Desktop](../shared/seawulf-desktop.md)
- [Gaussian](ondemand-gaussview.md)
- [ChimeraX](ondemand-chimerax.md)
- [ParaView](../shared/ondemand-paraview.md)
- [All 18 apps](seawulf-ondemand-apps.md)

> [!NOTE]
> **No patient data.** SeaWulf isn't approved for PHI or other HIPAA-covered data. Work with PHI belongs on [ClinWulf](https://rci.stonybrook.edu/hpc/clusters/clinwulf).

## Best suited for

- Physics and climate science
- Bioinformatics and materials science
- Machine learning and AI
- Engineering and data science

## Getting access

1. **Join a project**: If your PI already has a SeaWulf project, open a ticket with the help topic "Request an account for SeaWulf" and include your NetID, your PI's name and the project number.

    [How to request an account](../shared/requesting-accounts-project-numbers.md)
2. **Or start one (faculty)**: Faculty request a project number with a one-page PDF describing the work, computing needs, software, storage and group members.

    [Request a project number](../shared/requesting-accounts-project-numbers.md#project)
3. **Set up Duo, then connect**: Every login needs a Duo approval. Then sign in with Open OnDemand or SSH and run your first job.
    - [Duo setup](../shared/duo-authentication.md)
    - [Quick start guide](quick-start-guide.md)

## Related guides

- [Quick start guide](quick-start-guide.md)
- [Queue selection guide](queue-selection-guide.md)
- [Writing job scripts](../shared/writing-job-scripts.md)
- [Storage layout & policies](storage-layout-policies.md)
- [Using modules](../shared/using-modules.md)
- [Good conduct on the RCI clusters](../shared/hpc-good-conduct.md)

Other clusters

## Also available

- [Cluster**NVwulf**

    GPU and AI

    GPU acceleration for AI and machine learning, on H200 and Blackwell GPUs.

    View cluster →](../nvwulf/README.md)
- [Cluster**ClinWulf**

    HIPAA

    HIPAA-compliant computing for IRB-approved research on PHI.

    View cluster →](https://rci.stonybrook.edu/hpc/clusters/clinwulf)
- [Cluster**SecureWulf**

    Coming Christmas 2026

    Secure computing for controlled-access research data.

    View cluster →](https://rci.stonybrook.edu/hpc/clusters/securewulf)

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/clusters/seawulf> (maintained by Research Computing and Informatics).
