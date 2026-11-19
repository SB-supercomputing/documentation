# Open OnDemand apps on NVwulf

NVwulf's Open OnDemand portal gives you 19 GPU-ready apps in your web browser, from Jupyter and RStudio to cryo-EM, pathology imaging, and private AI chat. This page lists every app, what it's for, and the settings that matter when you launch it.

**On this page:** [All apps at a glance](#glance) · [Launching an app](#launch) · [Coding and notebooks](#code) · [Desktops and visualization](#viz) · [AI and LLMs](#ai) · [Structural biology](#bio) · [Imaging and pathology](#img) · [Troubleshooting](#trouble)

> [!NOTE]
> **Where to find it:** sign in at [nvwulf-ood.nvwulf.stonybrook.edu](https://nvwulf-ood.nvwulf.stonybrook.edu/) with your NetID and Duo, then open **Interactive Apps** in the top menu. You need an NVwulf account first. See [Getting access to NVwulf](getting-access-nvwulf.md).

## All apps at a glance {#glance}

| App | What it's for | Menu group |
| --- | --- | --- |
| [Jupyter Notebook](#code) | Python notebooks on a GPU | Servers |
| [RStudio Server](#code) | R and RStudio in the browser | Servers |
| [Code Server](#code) | VS Code in the browser | Servers |
| [MATLAB](#code) | MATLAB's full desktop (R2025a) | GUIs |
| [NVwulf Desktop](#viz) | A full Linux desktop for any graphical program | Desktops |
| [3D CT Scan](ondemand-3d-ct-scan.md) | 3D Slicer, Blender, MeshLab, and ImageJ for CT data | Desktops |
| [ParaView](../shared/ondemand-paraview.md) | Scientific 3D visualization | GUIs |
| [LLM Chat (llama.cpp)](ondemand-llm-chat.md) | Chat with an open model, including your own GGUF files | AI |
| [Ollama (Open WebUI)](ondemand-ollama.md) | ChatGPT-style interface for Ollama models | AI |
| [vLLM (Open WebUI)](ondemand-vllm.md) | Fast serving of Hugging Face models, with a chat interface | AI |
| [CryoSPARC](ondemand-cryosparc.md) | Cryo-EM data processing | Science |
| [RELION](ondemand-relion.md) | Cryo-EM structure determination | Cryo-EM |
| [Protein Prediction](ondemand-protein-prediction.md) | Protein structures with AlphaFold 2 or AlphaFold 3 | Science |
| [MOE](../shared/ondemand-moe.md) | Molecular modeling and drug discovery | Molecular Modeling |
| [Napari](ondemand-napari.md) | Viewer for large multi-dimensional images | Imaging & Pathology |
| [QuPath](ondemand-qupath.md) | Digital pathology and whole-slide image analysis | Image Analysis |
| [CellProfiler](ondemand-cellprofiler.md) | Automated cell image analysis, with optional Cellpose on GPU | Imaging & Pathology |
| [CyLinter](ondemand-cylinter.md) | Quality control for multiplex tissue images | Imaging |
| [Minerva Author](ondemand-minerva-author.md) | Build interactive Minerva Stories from tissue images | Imaging |

The portal also has the everyday tools: **Nvwulf Cluster Shell Access** (a terminal), **Files** (your home directory), **Active Jobs**, **Job Composer** for batch jobs, and **System Status**. See the [OnDemand overview](../shared/ondemand-overview.md) and [Job Composer](../seawulf/job-composer.md).

## Launching an app {#launch}

Every interactive app runs as a job on NVwulf's **B40 GPU nodes** (NVIDIA RTX PRO 6000 Blackwell, 96 GB of GPU memory each, up to 4 per node). Most launch forms ask for the same things:

| Setting | What to choose |
| --- | --- |
| Queue | `b40x4` (Regular) for sessions up to 8 hours, `b40x4-long` (Long) for up to 48 hours. |
| Hours | How long the session runs. It ends at this limit, so save your work before then. |
| GPUs | 1 is enough for almost everything. Ask for more only if the app uses them (CryoSPARC, RELION, larger AI models). |
| Cores and memory | Start small and use the app's hint. Big requests wait longer in the queue. |
| Working directory | Many science apps start in your scratch folder, `/lustre/nvwulf/scratch/<netid>`. Point it at your data. |
| Email | Optional. Handy when the queue is busy and you want to know when the session starts. |

1. Fill in the form and click **Launch**. The session card moves from *Queued* to *Starting* to *Running*.
2. Click the connect button on the card to open the app in a new tab.
3. When you're done, click **Delete** on the card so the GPU goes back to others. Closing the browser tab doesn't stop the job.

> [!NOTE]
> **Scratch is temporary.** Several apps keep their data in scratch by default (CryoSPARC projects, Open WebUI chats, downloaded models). NVwulf scratch is purged after 30 days, so copy anything you want to keep to project space. See [Storage layout & policies](../seawulf/storage-layout-policies.md).

If your group has priority access on NVwulf, the CryoSPARC and RELION forms also show **Priority b40x4** queues. Everyone else should use Regular or Long.

## Coding and notebooks {#code}

| App | Good to know |
| --- | --- |
| Jupyter Notebook | Starts a Jupyter server with the GPUs you ask for. For your own Python packages, see [Jupyter notebooks](../shared/jupyter-notebooks.md) and [Conda environments](../shared/conda-environments.md). |
| RStudio Server | RStudio in the browser. Choose cores and memory for your analysis; most R work doesn't need more than 1 GPU. See [RStudio](../shared/rstudio.md). |
| Code Server | VS Code in the browser, with a terminal on the GPU node. Set the working directory to your project folder. See [Code Server](../shared/code-server.md). |
| MATLAB | MATLAB R2025a with its full desktop. The **Modules** box loads extra modules first, for example a compiler for MEX files. See [MATLAB](../seawulf/matlab-open-ondemand.md). |

## Desktops and visualization {#viz}

| App | Good to know |
| --- | --- |
| NVwulf Desktop | A full Linux desktop on a GPU node. Use it for any graphical program that doesn't have its own app. Open a terminal from the desktop to load modules and start programs. More in [WolfieHPCDesktop](../shared/seawulf-desktop.md). |
| 3D CT Scan | A desktop with **3D Slicer**, **Blender**, **MeshLab**, and **ImageJ** ready for CT viewing, segmentation, meshing, and rendering. Keep **GPU accelerated** rendering on, and ask for about 64 GB of memory for typical scans. Start the tools from the desktop icons or the Applications menu. |
| ParaView | ParaView's full interface for visualizing simulation and imaging data, running on the GPU node so large datasets stay on the cluster. |

## AI and LLMs {#ai}

These apps run open-source language models on NVwulf's GPUs. The model runs inside your own session, not on a cloud service. Each B40 GPU has 96 GB of memory, enough for many popular models. For bigger models, ask for more GPUs.

| App | Pick it when | Good to know |
| --- | --- | --- |
| LLM Chat (llama.cpp) | You want a quick chat with a ready-made model, or you have your own GGUF file | Choose a preloaded model from the list, or **Use my own model** and give the path to your `.gguf` file. Leave **GPU layers** on All for the best speed. |
| Ollama (Open WebUI) | You like Ollama's model library and a ChatGPT-style interface | System models appear in Open WebUI automatically. To add one, type its name (for example `codellama:7b`) in **Pull new model**; it downloads to your own models folder. |
| vLLM (Open WebUI) | You need fast serving of a Hugging Face model, or want to split a large model across GPUs | Pick a system model or enter a Hugging Face ID such as `microsoft/Phi-3-mini-4k-instruct`. More GPUs let vLLM split a model across them. If it runs out of GPU memory, lower the context length. |

> [!NOTE]
> **No patient data.** Don't use these apps with patient information (PHI). Work with PHI belongs on [ClinWulf](https://rci.stonybrook.edu/hpc/clusters/clinwulf). Downloaded models count toward your scratch space and are purged with it.

## Structural biology and cryo-EM {#bio}

| App | Good to know |
| --- | --- |
| CryoSPARC | You need your own CryoSPARC license ID, which is free for academic use from [cryosparc.com](https://cryosparc.com/download). Use the same email address you registered with. Your CryoSPARC database and projects stay in the folders on the form between sessions. Ask for at least 64 GB of memory (128 GB or more is better) and 8 or more cores; more GPUs process faster. |
| RELION | RELION's interface for cryo-EM structure determination, in a project folder you choose. One GPU is enough to use the interface; ask for more if you'll run processing jobs from the session. 64 GB of memory or more is recommended for refinement. |
| Protein Prediction | Predicts a structure from an amino acid sequence with **AlphaFold 2** (paste FASTA) or **AlphaFold 3** (paste JSON). AlphaFold 3 needs your own copy of the model parameters from Google DeepMind, under their [terms of use](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md); enter the folder that holds them. Results are saved in the working directory. |
| MOE | Molecular Operating Environment, for molecular modeling and drug discovery, in a desktop session. Molecular dynamics and large databases can need a lot of memory. |

## Imaging and pathology {#img}

| App | Good to know |
| --- | --- |
| Napari | Fast viewer for large 2D, 3D, and multi-channel images, including whole-slide pathology. Keep the GPU on for smooth rendering, and ask for about 64 GB of memory for typical SVS or NDPI slides. |
| QuPath | Digital pathology and whole-slide image analysis. Whole-slide work can need a lot of memory; turn on the GPU if your workflow uses it. |
| CellProfiler | Automated analysis of biological images with pipelines. Standard pipelines run on CPU and 16 GB of memory is usually enough. Choose **Use GPU: Yes** only for Cellpose segmentation. |
| CyLinter | Quality control for multiplex tissue images, viewed in napari. You need a `cylinter_config.yml` file; enter its full path on the form. |
| Minerva Author | Turns multiplex tissue images (OME-TIFF, SVS and others) into interactive Minerva Stories to share. It runs on CPU; 8 to 16 cores and 64 GB of memory suit typical images. Stories are saved next to your input image. |

## Troubleshooting {#trouble}

<details markdown="1">
<summary>My session stays Queued</summary>

The B40 nodes are busy. Try the Regular queue instead of Long, ask for fewer GPUs, cores, or memory, or shorten the hours. You can check how busy the nodes are under **Clusters** then **System Status**.

</details>

<details markdown="1">
<summary>The app says it ran out of memory</summary>

Delete the session and launch again with more memory. For AI apps, running out of *GPU* memory means the model is too big: pick a smaller or more compressed model, lower the context length, or ask for more GPUs.

</details>

<details markdown="1">
<summary>I can't find my files in the app</summary>

Check the working directory on the launch form. Many apps start in your scratch folder, `/lustre/nvwulf/scratch/<netid>`, rather than your home folder.

</details>

<details markdown="1">
<summary>My session ended in the middle of my work</summary>

Sessions stop at the hours you asked for. Save often, and use the Long queue (up to 48 hours) for longer work.

</details>

<details markdown="1">
<summary>My CryoSPARC or Open WebUI data disappeared</summary>

Both store their data in scratch by default, and scratch is purged after 30 days. Copy projects you want to keep to project space, or change the data folders on the form.

</details>

Need an app that isn't here, or stuck on a problem? [Open a ticket](https://iacs.supportsystem.com/) and mention NVwulf, or drop into [HPC virtual office hours](https://rci.stonybrook.edu/events/hpc-virtual-office-hours).

Related: [OnDemand overview](../shared/ondemand-overview.md) · [OnDemand apps on SeaWulf](../seawulf/seawulf-ondemand-apps.md) · [OnDemand apps on ClinWulf](https://rci.stonybrook.edu/docs/clinwulf-ondemand-apps) · [Getting started on NVwulf](getting-started-nvwulf.md) · [About NVwulf](README.md)

**Applies to:** NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/nvwulf-ondemand-apps> (maintained by Research Computing and Informatics).
