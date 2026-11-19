# Requesting accounts & project numbers

Access to RCI's clusters works in two layers. A **project** belongs to a Stony Brook faculty member (the PI) and has a project number. Each person then gets an **account** on that project, tied to their NetID. Most people only need an account on a project that already exists.

**On this page:** [Which do you need?](#which) · [Request an account](#account) · [Request a project number](#project) · [External collaborators](#external) · [After you're approved](#next) · [Questions](#faq)

## Which do you need? {#which}

| If you are… | You need | Go to |
| --- | --- | --- |
| A student, postdoc, or staff member whose PI already has a SeaWulf project | An account | [Request an account](#account) |
| Faculty starting new research or a course on SeaWulf | A project number, then accounts for your group | [Request a project number](#project) |
| A collaborator from outside Stony Brook without a NetID | A NetID first, then an account | [External collaborators](#external) |
| Working with GPUs and AI on NVwulf | NVwulf access (a similar process) | [Getting access to NVwulf](../nvwulf/getting-access-nvwulf.md) |
| Working with PHI on an IRB-approved study in Health Sciences / Medicine | ClinWulf access | [ClinWulf](https://rci.stonybrook.edu/hpc/clusters/clinwulf) |

Not sure which cluster fits? The [cluster picker](https://rci.stonybrook.edu/hpc/cluster-picker) asks three questions and suggests one.

## Request an account {#account}

Anyone in a project group can get an account once the project exists. The PI can request accounts for the whole group in one ticket, or you can request your own with your PI's OK.

1. Go to the IACS support system at [iacs.supportsystem.com](https://iacs.supportsystem.com/) and choose **Open a New Ticket**.
2. Pick the help topic **Request an account for SeaWulf**.
3. Include:
    - your **NetID** (or the NetIDs of everyone to add),
    - the **PI's name**, and
    - the **project number**. Ask your PI if you don't know it.
4. You'll get an email when your account is ready.

## Request a project number {#project}

Project numbers are requested by **Stony Brook faculty**, for research or for a course. BNL staff without their own Stony Brook appointment can join as collaborators on a project sponsored by a Stony Brook faculty member.

### 1. Write a one-page PDF

A review committee approves each request, and it needs all of the following. Keep it to one page, including any graphics. Requests may be made public, so leave out anything confidential.

- **Description.** A short overview of the project, course, or use case and why it needs SeaWulf. Detailed technical information isn't needed.
- **Computing needs.** Your best estimates of:
    - CPU or GPU hours per year
    - memory (RAM) per job
    - GPUs per job, if any
    - how many nodes one job uses at the same time
    - how long a typical job runs
- **Software.** Packages you'd like installed. You can ask later too, but listing them now speeds things up.
- **Storage.** Say whether the standard storage below is enough, and describe any shared project space you need.
- **Group members.** Full names and NetIDs of everyone who needs access, including you.

Every account comes with this storage:

| Space | Size | Backed up? | Good to know |
| --- | --- | --- | --- |
| Home `/gpfs/home/<netid>` | 20 GB | Yes | For scripts, settings, and small files |
| Scratch `/gpfs/scratch/<netid>` | 20 TB | No | Temporary. Files older than 45 days are deleted. |
| Project `/gpfs/projects/<group>` | Up to 10 TB, on request | No | Shared space your whole group can read and write |

More detail is in [Storage layout & policies](../seawulf/storage-layout-policies.md).

<details markdown="1">
<summary>See a sample one-page request</summary>

**Project:** Modeling protein folding under thermal stress. PI: Jane Smith, Department of Biochemistry.

**Description:** We run molecular dynamics simulations of small proteins at several temperatures to study how they unfold. SeaWulf lets us run many simulations in parallel instead of one at a time on a lab workstation.

**Computing needs:** about 200,000 CPU hours a year; 4 GB of RAM per core; no GPUs; 1 to 2 nodes per job; jobs usually run 12 to 24 hours.

**Software:** GROMACS and Python with NumPy and MDAnalysis.

**Storage:** the standard home and scratch are fine for running jobs. We'd like 2 TB of shared project space for finished trajectories.

**Group members:** Jane Smith (jsmith), Alex Lee (alee), Priya Patel (ppatel).

</details>

### 2. Submit it

1. Go to [iacs.supportsystem.com](https://iacs.supportsystem.com/) and choose **Open a New Ticket**.
2. Pick the help topic **Request a Project Number**.
3. Use your verified `@stonybrook.edu` or `@stonybrookmedicine.edu` email and attach the PDF.
4. The committee reviews it. If it's approved, your project number arrives by email. If they can't accommodate the request as written, they'll contact you to talk through options.

> [!NOTE]
> **The most common cause of delays is a missing piece.** Include the computing estimates and the full list of group members from the start, and approval goes much faster.

## External collaborators without a NetID {#external}

Collaborators from outside Stony Brook need a NetID before they can have an account.

1. The PI fills out the [external affiliation form](https://drive.google.com/file/d/1FT9_wZXtayFgAmc1XOp_WRPKyHHDyQS3/view).
2. The PI emails it to [Sarena Romano](mailto:sarena.romano@stonybrook.edu) to request a volunteer affiliation.
3. Once the collaborator has a NetID, [request their account](#account) the usual way.

## After you're approved {#next}

1. Set up [Duo two-factor authentication](duo-authentication.md). Every login needs it.
2. [Connect to the cluster](connecting-cluster.md) in your browser with Open OnDemand, or with SSH.
3. Run your first job with the [Quick Start Guide](../seawulf/quick-start-guide.md), or build a script with the [job script builder](https://rci.stonybrook.edu/hpc/script-builder).
4. Skim [Good conduct on the RCI clusters](hpc-good-conduct.md) so your work runs smoothly alongside everyone else's.

## Questions {#faq}

<details markdown="1">
<summary>I'm a student. Can I request my own project?</summary>

Projects are requested by faculty. Ask your advisor or instructor to request a project (or to confirm the number of an existing one), then request your account on it.

</details>

<details markdown="1">
<summary>Can I use SeaWulf for a course?</summary>

Yes. The instructor requests a project number and describes the course in the one-page PDF, then lists the students (or requests their accounts once the project exists).

</details>

<details markdown="1">
<summary>Can I add people or software later?</summary>

Yes. Request accounts for new group members at any time with the account ticket above, and ask for software through a regular support ticket. Listing both up front just makes the first setup quicker.

</details>

<details markdown="1">
<summary>We need more shared storage than 10 TB</summary>

Explain what you need and why in a support ticket. Requests over 10 TB need a detailed justification and, if approved, may be granted for a limited time. For long-term or archival storage, see the [Research Storage picker](https://rci.stonybrook.edu/storage).

</details>

<details markdown="1">
<summary>My collaborator already has a NetID from another Stony Brook role</summary>

Then they don't need the affiliation form. Request their account with their NetID, the PI's name, and the project number.

</details>

Questions about a request? [Open a ticket with IACS support](https://iacs.supportsystem.com/) or drop into [HPC virtual office hours](https://rci.stonybrook.edu/events/hpc-virtual-office-hours).

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/requesting-accounts-project-numbers> (maintained by Research Computing and Informatics).
