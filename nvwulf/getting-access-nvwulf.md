# Getting access to NVwulf

NVwulf is Stony Brook's GPU cluster for AI and machine learning. It's open to Stony Brook instructors, researchers, staff, and students. Like SeaWulf, access works through projects: a faculty member leads each project, and everyone else gets an account on one.

**On this page:** [Join an existing project](#join) · [Request a new project](#new) · [What to put in the PDF](#pdf) · [After you're approved](#next)

## Option 1: join an existing project {#join}

If your PI already has an active SeaWulf or NVwulf project:

1. Open a ticket at [iacs.supportsystem.com](https://iacs.supportsystem.com/).
2. Pick the help topic **Request an Account for NVwulf**.
3. Include your **NetID**, your **PI's name**, and the **project number**.

## Option 2: request a new NVwulf project (faculty only) {#new}

1. Write a **one-page PDF**, including any graphics, covering the points below.
2. Open a ticket at [iacs.supportsystem.com](https://iacs.supportsystem.com/) with the help topic **Request a Project Number – NVwulf** and attach the PDF.
3. A review committee looks at it. If approved, your project number arrives by email; if not, they'll contact you to talk about alternatives.

> [!NOTE]
> Project requests become publicly available once submitted, so leave out anything confidential.

## What to put in the PDF {#pdf}

- **Usage description:** a short overview of the project and why it needs NVwulf's GPUs.
- **Computing needs:** your best estimates of CPU and GPU hours per year, memory per job, GPUs per job, how many nodes a job uses at once, and how long a typical job runs.
- **Software:** packages you'd like installed. You can ask later too, but listing them now speeds things up.
- **Disk space:** each account gets a 20 GB home folder (backed up, never deleted) and a 20 TB scratch folder (not backed up; files deleted after 30 days). Describe any extra long-term or shared storage you need.
- **User accounts:** full names and NetIDs of everyone in your group who needs access.

The [SeaWulf project guide](../shared/requesting-accounts-project-numbers.md#project) has a sample one-page request you can adapt.

## After you're approved {#next}

1. Set up [Duo](../shared/duo-authentication.md) if you haven't already.
2. Follow [Getting started on NVwulf](getting-started-nvwulf.md) to log in, move your data, and run a first GPU job.

Not sure NVwulf is the right cluster? Try the [cluster picker](https://rci.stonybrook.edu/hpc/cluster-picker) or see the [NVwulf page](README.md).

**Applies to:** NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/getting-access-nvwulf> (maintained by Research Computing and Informatics).
