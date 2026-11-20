# Open OnDemand apps on SeaWulf

SeaWulf's Open OnDemand portal gives you 18 apps in your web browser: notebooks, R, VS Code, MATLAB and Mathematica, chemistry and structural biology tools, genome and data viewers, and a full Linux desktop. This page lists every app, what it's for, and the settings that matter when you launch it.

**On this page:** [All apps at a glance](#glance) · [Launching an app](#launch) · [Coding and notebooks](#code) · [Desktops and math](#math) · [Chemistry and structural biology](#chem) · [Visualization and data](#viz) · [Troubleshooting](#trouble)

!!! note ""
    **Where to find it:** sign in at [sn-ood.seawulf.stonybrook.edu](https://sn-ood.seawulf.stonybrook.edu/) with your NetID and Duo, then open **Interactive Apps** in the top menu. You need a SeaWulf account first. See [Requesting accounts & project numbers](../shared/requesting-accounts-project-numbers.md).

## All apps at a glance {#glance}

| App | What it's for | Menu group |
| --- | --- | --- |
| [Jupyter Notebook](#code) | Python notebooks | Servers |
| [JupyterLab](ondemand-jupyterlab.md) | The newer Jupyter interface, with files, notebooks, and terminals side by side | Sandbox |
| [RStudio Server](#code) | R and RStudio in the browser | Servers |
| [Code Server](#code) | VS Code in the browser | Servers |
| [Galaxy](ondemand-galaxy.md) | Your own private Galaxy server for point-and-click bioinformatics | Servers |
| [SeaWulf Desktop](#math) | A full Linux desktop for any graphical program | Desktops |
| [MATLAB](matlab-open-ondemand.md) | MATLAB's full desktop, R2016 through R2025a | GUIs |
| [Mathematica](ondemand-mathematica.md) | Wolfram Mathematica notebooks | Visualization |
| [GNU Octave](ondemand-octave.md) | Free, MATLAB-compatible numerical computing | Visualization |
| [Gaussian/GaussView](ondemand-gaussview.md) | Quantum chemistry calculations with a graphical builder | Chemistry |
| [MOE](../shared/ondemand-moe.md) | Molecular modeling and drug discovery | Molecular Modeling |
| [UCSF ChimeraX](ondemand-chimerax.md) | Molecular structure and cryo-EM map viewing and analysis | Visualization |
| [PyMOL](ondemand-pymol.md) | Molecular visualization (open-source PyMOL) | Visualization |
| [Coot](ondemand-coot.md) | Building and fitting models into crystallography and cryo-EM maps | Visualization |
| [Phenix](ondemand-phenix.md) | Crystallographic structure determination, with Coot | Visualization |
| [ParaView](../shared/ondemand-paraview.md) | Scientific 3D visualization | Visualization |
| [IGV](ondemand-igv.md) | Integrative Genomics Viewer for sequencing data | Visualization |
| [TensorBoard](ondemand-tensorboard.md) | Browse machine learning training logs | Visualization |

The portal also has the everyday tools: **Seawulf Cluster Shell Access** (a terminal), **Files** (with shortcuts to both your home folder and your scratch folder), **Active Jobs**, and **Job Composer** for batch jobs. See the [OnDemand overview](../shared/ondemand-overview.md) and [Job Composer](job-composer.md).

## Launching an app {#launch}

Every app runs as a job on SeaWulf's shared CPU queues, on either the 40-core Intel nodes or the 96-core AMD nodes. SeaWulf's OnDemand apps don't use GPUs; for GPU work, use [NVwulf's OnDemand apps](../nvwulf/nvwulf-ondemand-apps.md). Most launch forms ask for the same things:

| Setting | What to choose |
| --- | --- |
| Queue | `short-40core-shared` or `short-96core-shared` for up to 4 hours, `long-…-shared` for up to 24 hours, `extended-…-shared` for up to 3.5 days. Start with a short queue. |
| Hours | How long the session runs. It ends at this limit, so save your work before then. |
| Cores | 1 to 4 is plenty for most interactive work. Ask for more only if your program runs in parallel. |
| Memory | From 2 GB up to 164 GB. Start small; big requests wait longer in the queue. |
| Working directory | Where the app starts. Most default to your home folder, `/gpfs/home/<netid>`. Point it at your data. |
| Email | Optional. Handy when the queue is busy and you want to know when the session starts. |

1. Fill in the form and click **Launch**. The session card moves from *Queued* to *Starting* to *Running*.
2. Click the connect button on the card to open the app in a new tab.
3. When you're done, click **Delete** on the card so the cores go back to others. Closing the browser tab doesn't stop the job.

The full list of queues and limits is in the [queue selection guide](queue-selection-guide.md).

## Coding and notebooks {#code}

| App | Good to know |
| --- | --- |
| Jupyter Notebook | The classic notebook interface. For your own Python packages, see [Conda environments](../shared/conda-environments.md). More in [Jupyter notebooks](../shared/jupyter-notebooks.md). |
| JupyterLab | The newer Jupyter interface. It's listed under **Sandbox** while it's being tested. The **Modules to load** box starts with `jupyter/latest`. |
| RStudio Server | Choose R 4.5.1 or 4.3.2. If an R package needs a system library to install, add its module in **Additional modules** (for example `hdf5/1.12.1`). More in [RStudio](../shared/rstudio.md). |
| Code Server | VS Code in the browser, with a terminal on the compute node. Set the working directory to your project folder. More in [Code Server](../shared/code-server.md). |
| Galaxy | Starts your own private Galaxy server. Choose which SeaWulf folders Galaxy can see (home, scratch, projects). Galaxy keeps its data in `~/ondemand/data/galaxy` unless you pick another folder; your home folder is only 20 GB, so point it at project space for real datasets. If you leave the password blank, one is created and saved in `credentials.txt` in that folder. Memory is typed as, for example, `16G`. |

## Desktops and math {#math}

| App | Good to know |
| --- | --- |
| SeaWulf Desktop | A full XFCE Linux desktop on a compute node, for any graphical program that doesn't have its own app. Open a terminal from the desktop to load modules and start programs. More in [WolfieHPCDesktop](../shared/seawulf-desktop.md). |
| MATLAB | Pick any version from R2016 to R2025a. The **Modules** box loads extra modules first, for example a compiler for MEX files. More in [MATLAB](matlab-open-ondemand.md). |
| Mathematica | Mathematica 13.1 with its full notebook interface, in a desktop session. |
| GNU Octave | Octave 9.3, a free alternative that runs most MATLAB code. |

## Chemistry and structural biology {#chem}

| App | Good to know |
| --- | --- |
| Gaussian/GaussView | Gaussian 16 (C.01) and GaussView 6 in a desktop. Build molecules in GaussView and run calculations from it. This is the one app that also offers whole-node queues (such as `short-40core`) for bigger calculations. Match the processor count in your Gaussian input to the cores you request. |
| MOE | Molecular Operating Environment 2024, for molecular modeling and drug discovery. Molecular dynamics and large databases can need a lot of memory. |
| UCSF ChimeraX | ChimeraX 1.11 for viewing and analyzing structures, sequences, and density maps. |
| PyMOL | Open-source PyMOL 3.1 for molecular graphics and figures. |
| Coot | Coot 1.1 for model building. **Force software rendering** is on by default; keep it on if you see EGL or OpenGL errors. |
| Phenix | Phenix 2.0 (CPU version) for crystallographic structure determination, with Coot loaded alongside it. |

## Visualization and data {#viz}

| App | Good to know |
| --- | --- |
| ParaView | ParaView 6.0.1 or 5.11.0 for visualizing simulation and imaging data, so large files stay on the cluster. |
| IGV | IGV 2.19 for viewing alignments, variants, and other genomic tracks. Set the working directory to where your BAM or VCF files are. |
| TensorBoard | Browse TensorFlow or PyTorch training logs. Set **log directory** to the folder with your `events` files. It runs on CPU only. |

!!! note ""
    **Scratch is temporary.** Your scratch folder (`/gpfs/scratch/<netid>`) is handy for big data, but files older than 45 days are deleted. Keep anything you need in home or project space. See [Storage layout & policies](storage-layout-policies.md).

## Troubleshooting {#trouble}

<details markdown="1">
<summary>My session stays Queued</summary>

The queue is busy. Try a short queue, fewer cores or less memory, or the other node type (40-core or 96-core).

</details>

<details markdown="1">
<summary>A graphics app shows OpenGL or EGL errors, or a black window</summary>

These apps run without a GPU. For Coot, keep **Force software rendering** on. For other apps, delete the session and try again; if it keeps happening, [open a ticket](https://iacs.supportsystem.com/) with the app name.

</details>

<details markdown="1">
<summary>"Disk quota exceeded" or the app won't start</summary>

Your 20 GB home folder may be full; Galaxy data, conda environments, and caches add up fast. Check with `myquota` in a shell, then clean up or move data to project space. See [Checking storage quotas](checking-storage-quotas.md).

</details>

<details markdown="1">
<summary>I can't find my files</summary>

Check the working directory on the launch form. In the **Files** menu you can jump straight to your home or scratch folder.

</details>

<details markdown="1">
<summary>My session ended in the middle of my work</summary>

Sessions stop at the hours you asked for. Save often, and use a long or extended queue for longer work.

</details>

Need an app that isn't here, or stuck on a problem? [Open a ticket](https://iacs.supportsystem.com/), or drop into [HPC virtual office hours](https://rci.stonybrook.edu/events/hpc-virtual-office-hours).

Related: [OnDemand overview](../shared/ondemand-overview.md) · [OnDemand apps on NVwulf](../nvwulf/nvwulf-ondemand-apps.md) · [OnDemand apps on ClinWulf](https://rci.stonybrook.edu/docs/clinwulf-ondemand-apps) · [About SeaWulf](README.md)

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/seawulf-ondemand-apps> (maintained by Research Computing and Informatics).
{: .rci-credit }
