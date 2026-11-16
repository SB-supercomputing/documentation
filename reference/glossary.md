# Glossary

Plain-language definitions of the terms used in the modules and lessons. Those pages link here when they introduce a term.

Jump to: [Using a cluster](#using-a-cluster) · [Running jobs](#running-jobs) · [Storage and data](#storage-and-data) · [Parallel programming and performance](#parallel-programming-and-performance) · [Visualization terms](#visualization) · [Chemistry](#chemistry) · [Structural biology](#structural-biology) · [Genomics](#genomics)

> [!NOTE]
> **Cluster details.** <mark>Highlighted</mark> values are placeholders. Kitsune's queue names, module versions, paths, and addresses go in when the cluster is deployed.

## Using a cluster

### Cluster
Many computers joined by a fast network and shared by many users. You reach it over the internet, and a scheduler decides whose work runs where.

### Node
One computer in a cluster, with its own processors and memory.

### Login node
The node you arrive on when you connect. It's for editing files, moving small amounts of data and submitting jobs. It's shared by everyone who is logged in, so heavy computing there slows everyone down.

### Compute node
A node that runs jobs. You reach it through the scheduler (a batch job or an OnDemand session), not by logging in directly.

### Core
One processing unit inside a processor. A compute node holds many of them (<mark>Kitsune cores per node</mark>). A program only uses more than one core if it's written to.

### Open OnDemand (OOD)
A website that gives you the cluster in a browser: files, a terminal, and graphical programs like ParaView or JupyterLab running on a compute node. Its address here is <mark>Kitsune OnDemand address</mark>.

### Interactive session
A job that gives you a live program (a desktop, JupyterLab, ParaView…) on a compute node for a set time. It counts against your time like any job. **Closing the browser tab does not end it**: you have to delete the session.

### SSH
The secure way to open a terminal on a remote computer, by running `ssh` with your username and a login node's address (<mark>Kitsune login node address</mark>). OnDemand's shell does the same job in the browser.

### Multi-factor authentication (MFA)
Proving it's you with two things: your password and something you have, such as a phone app or a passcode (<mark>Kitsune second factor</mark>).

### Module
A way to load software into your session on demand: `module load <name>/<version>` makes a program available, and `module purge` clears everything. Clusters use modules because many versions of a program can live side by side. <mark>Kitsune module names and any setup a new session needs</mark>.

### Environment variable
A named setting your programs can read, such as `$HOME` (your home directory) or `$USER` (your username on the cluster).

### Container
A packaged environment, a program plus everything it needs, that runs the same way on any machine. On HPC clusters the usual runtime is Apptainer (formerly Singularity).

## Running jobs

### Slurm
The scheduler these lessons assume. You describe what your job needs (cores, memory, time), and Slurm decides when and where it runs.

### Job
One piece of work handed to the scheduler: a batch script, or an interactive session.

### Job script
A text file with `#SBATCH` lines stating what the job needs, followed by the commands to run. Submit it with `sbatch script.slurm`.

### Queue (partition)
A named group of nodes with its own limits, such as one for short interactive work that shares a node, and one for quick tests. <mark>Kitsune queue names and their limits</mark>.

### Walltime
The longest your job may run, in clock time. Set it with `--time`. When it runs out, Slurm stops the job, no matter whether it finished.

### Priority
The scheduler's ranking of waiting jobs. It combines how long a job has waited, its size, and fairshare.

### Fairshare
A priority factor that pushes your jobs down the queue if you or your group used more than your share recently, and up if you used less.

### Backfill
The scheduler holds room for a large job that is waiting, and fills the gap before it with jobs short enough to finish in time. A short, accurate time limit makes your job eligible for those gaps.

### QOS
Short for "quality of service": a label on a job that sets limits and priority, such as a maximum run time or number of jobs.

### Allocation
The computing time (and sometimes storage) granted to you or your project.

### Job array
Many similar jobs submitted at once, each with its own index number (`$SLURM_ARRAY_TASK_ID`). Useful for running the same analysis on 100 input files.

### Job dependency
A rule that a job waits for another job to finish first (`--dependency=afterok:<jobid>`). Chains preprocessing → simulation → analysis.

### Pending reason
The reason `squeue` gives for a job that hasn't started: *Priority* (others are ahead), *Resources* (not enough free nodes yet), and others.

### Efficiency
How much of what you requested your job actually used. `seff <jobid>` reports CPU and memory efficiency after a job ends. Low efficiency wastes your allocation and lowers your priority.

### Reservation
A block of nodes held for a set time, for example so a workshop's sessions start immediately.

## Storage and data

### Home directory
Your personal space (<mark>Kitsune home path and quota</mark>). It's small but backed up. Keep code and important small files here.

### Scratch
Large, fast, temporary space (<mark>Kitsune scratch path and quota</mark>), not backed up. Old files are deleted automatically (see [purge](#purge)). Run jobs here, and copy results you need to keep somewhere safer.

### Project space
Shared, longer-term space for a research group (<mark>Kitsune project path</mark>). Not backed up.

### Quota
Your limit on a filesystem: bytes, number of files, or both. Check yours with <mark>Kitsune quota command</mark>.

### Inode
The filesystem's record for one file or directory. Many quotas limit the number of inodes as well as bytes, so a million small files can exceed an inode quota while using very little space.

### Purge
Automatic deletion of old files from scratch, once they pass a set age (<mark>Kitsune purge age</mark>).

### Parallel filesystem
Storage that many nodes read and write at the same time, fast (<mark>Kitsune parallel filesystem</mark>). It's quick for large files and slow for many tiny ones.

### Checksum
A short fingerprint of a file's contents (e.g. from `sha256sum`). If the fingerprints before and after a copy match, the copy is intact.

### Tar
A tool that bundles many files into one archive (`.tar`, often compressed as `.tar.gz`), which is faster to transfer and easier on the filesystem.

### Data transfer node (DTN)
A server dedicated to moving data in and out of a cluster, tuned for fast transfers.

### Science DMZ
A part of a campus network built for moving large research datasets quickly, without the slow inspection ordinary traffic goes through.

### Globus
A service for moving large amounts of data reliably between "collections" (storage endpoints), with automatic retries and checksum checks.

### FAIR
Findable, Accessible, Interoperable, Reusable: principles for sharing research data so others can find and use it.

### DOI
A digital object identifier: a permanent link for a dataset or paper, e.g. `doi:10.5281/zenodo.123`.

### Data management plan (DMP)
A short document, required by most funders, describing what data a project creates and how it will be stored, shared, and preserved.

### HDF5
A file format for large scientific data. One HDF5 file works like a folder system inside a single file: *groups* are the folders, *datasets* are the arrays, and *attributes* are metadata, such as units and dates, attached to either.

### Dataspace
HDF5's word for the shape of a dataset: how many dimensions, and how long each is.

### Chunking
Storing an array in fixed-size blocks, so a program can read part of it without reading all of it. Good chunk shapes match how the data is usually read.

### NetCDF
A self-describing file format common in climate and ocean science. NetCDF-4 files are HDF5 files underneath.

## Parallel programming and performance

### Serial and parallel
A serial program does one thing at a time on one core. A parallel program splits the work so several cores or nodes work at once.

### Thread
One stream of work inside a program. Threads share the program's memory. OpenMP uses threads.

### Process
A running program with its own private memory. In MPI, each process is called a *rank*.

### Shared and distributed memory
Shared memory: all workers see the same memory (threads on one node). Distributed memory: each worker has its own, and they exchange messages (MPI across nodes).

### OpenMP
A way to make loops and tasks run on several threads of one node, by adding directives such as `#pragma omp parallel for`.

### MPI
The Message Passing Interface: a library for programs whose processes, possibly on many nodes, cooperate by sending each other messages.

### Race condition
A bug where the result depends on the order in which threads run, typically two threads updating the same variable at once.

### Reduction
Combining many workers' partial results into one, such as a sum. OpenMP and MPI both have built-in reductions.

### Halo exchange
In a grid split across processes, each process keeps a thin copy of its neighbors' edge values ("halo" or "ghost" cells) and refreshes it every step by trading edges with them.

### Hybrid MPI + OpenMP
MPI between nodes and OpenMP threads within each node, used together.

### NUMA
Non-uniform memory access. On a node with two processors, each processor reaches its own memory faster than the other one's.

### First-touch
The operating system places a page of memory near the core that first writes to it. Initialize data in the thread that will use it.

### Affinity
Where threads or processes run. Pinning ("binding") them to particular cores prevents them migrating and keeps their memory local.

### SIMD and vectorization
Single instruction, multiple data: a core applies one operation to several numbers at once. Compilers do this for suitable loops ("vectorization").

### Speedup and parallel efficiency
Speedup = time on 1 core ÷ time on N cores. Efficiency = speedup ÷ N. Perfect scaling is speedup N and efficiency 100%.

### Amdahl's law
The part of a program that can't be parallelized limits the speedup, however many cores you add. If 5% is serial, the speedup can never exceed 20.

### Gustafson's law
If the problem grows with the number of cores, the serial part matters less, so many cores stay useful.

### Strong and weak scaling
Strong scaling: the same problem on more cores (does it get faster?). Weak scaling: a bigger problem on more cores, keeping work per core fixed (does the time stay flat?).

### Profiler
A tool that shows where a program spends its time. *Sampling* profilers check periodically what's running; *instrumenting* profilers add timing code.

### Hotspot
The few functions or loops that take most of the run time, and the place to start optimizing.

### Roofline model
A chart that shows whether a piece of code is limited by how fast the processor computes or by how fast memory delivers data. That tells you which kind of optimization can help.

### POP metrics
A standard set of efficiency ratios for parallel programs, among them load balance and communication efficiency. Together they show what limits a run's scaling.

### Darshan
A lightweight tool that records how a job reads and writes files, to spot slow input/output patterns.

## Visualization

### Visualization pipeline
The chain from data to picture: a *reader* loads the data, *filters* transform it (slice it, contour it, compute something from it), and a *display* draws the result. In ParaView the Pipeline Browser shows this chain.

### Filter
One transformation step in a pipeline, such as Slice, Contour, or Stream Tracer. Its output feeds the next step.

### Point data and cell data
Values stored at the corners (points) of a mesh, or one value per cell. ParaView marks them with different icons. Point data is blended smoothly across a cell; cell data is constant over it.

### Scalar field and vector field
A scalar field gives one number at each place (temperature, density). A vector field gives a direction and size at each place (velocity, force).

### Mesh, grid, and image data
The points and cells data is stored on. A regular grid of equal boxes is called *image data* in ParaView, the format volumes such as CT scans and density maps usually come in.

### Slice
A flat cut through 3-D data, showing the values on that plane.

### Isosurface
The surface where a scalar field equals one chosen value, its *isovalue*, like a contour line on a topographic map. ParaView makes one with the Contour filter.

### Volume rendering
Drawing a whole 3-D field as a semi-transparent cloud rather than as surfaces. A *transfer function* sets the color and opacity for each data value.

### Streamline
A curve that follows the flow direction everywhere along its length, showing where a massless particle would travel. Streamlines start from *seed* points you choose.

### Glyph
A small shape such as an arrow or cone, drawn at many points, each pointing along the vector field and sized by its length.

### Color map
The rule turning numbers into colors. *Sequential* maps (viridis) show amounts; *diverging* maps (blue, white, red) show values above and below a meaningful middle; *categorical* maps show kinds. Rainbow maps create false boundaries and fail for colorblind readers.

### Offscreen rendering
Drawing images without a window on a screen, which batch jobs need because compute nodes have no display.

### The ParaView family
`paraview` is the graphical program. `pvpython` runs ParaView Python scripts. `pvbatch` runs them offscreen, in parallel if you like, for batch jobs. `pvserver` is the server half of a connection whose client runs elsewhere.

### Client and server visualization
Running the ParaView window on your own computer while a `pvserver` on the cluster reads and renders the data. The client and server versions must match.

### In situ visualization
Making pictures while a simulation runs, instead of saving all its data to disk first. ParaView Catalyst and Ascent do this.

### State file
A saved ParaView pipeline (`.pvsm`) that rebuilds your whole view when loaded. PyMOL (`.pse`) and ChimeraX (`.cxs`) have session files for the same purpose.

## Chemistry

### Electron density
How much electron charge is at each point around a molecule, in electrons per cubic bohr (e/bohr³).

### Molecular orbital (HOMO, LUMO)
A region an electron in a molecule occupies, with a positive and a negative lobe. The HOMO is the highest occupied orbital and the LUMO the lowest unoccupied one; together they largely determine how a molecule reacts.

### Electrostatic potential (ESP)
The electrical "pull" a molecule's charges exert at each point. Drawn on a density surface, it shows electron-rich (negative, usually red) and electron-poor (positive, usually blue) regions.

### Cube file
A text file of numbers on a 3-D grid, holding a density, an orbital, or a potential, with the molecule's atoms listed at the top. Gaussian's `cubegen` writes them. GaussView, ParaView, and PyMOL read both the grid and the atoms; ChimeraX reads the grid and takes the atoms from a separate file.

### Checkpoint file
Gaussian's saved results. The `.chk` file is binary and machine-specific; `formchk` converts it to a portable text `.fchk` that other tools read.

### Level of theory
The method and basis set used for a calculation, written as, e.g., `B3LYP/6-31G(d)`: the B3LYP density functional with the 6-31G(d) basis set.

### Geometry optimization
Moving a molecule's atoms until the energy is at a minimum, to find its stable shape.

### Bohr
The atomic unit of length: about 0.529 ångström (Å). Cube files are usually in bohr.

## Structural biology

### PDB and mmCIF
The Protein Data Bank is the public archive of 3-D structures of biological molecules. Each entry has a four-character ID (e.g. 4HHB, hemoglobin). mmCIF is the archive's current file format; `.pdb` is the older one.

### Chain, residue, and atom
A protein structure is one or more *chains*. Each chain is a string of *residues* (amino acids), and each residue is a set of *atoms*. Hemoglobin 4HHB has four chains: two α and two β.

### B-factor
How smeared out an atom's position is in a crystal structure, whether from motion or disorder. High values mean the position is less certain.

### Cryo-EM map
A 3-D density map of a molecule, rebuilt from many electron-microscope images of frozen samples. Its *resolution* in ångströms measures the detail; a smaller number means finer detail.

### Map threshold
The density value at which a map's surface is drawn (the contour level). A low threshold shows noise. A high one hides real features.

### Fitting
Placing an atomic model into a density map so the atoms sit where the density is.

### AlphaFold, pLDDT, and PAE
AlphaFold predicts protein structures from their sequences. **pLDDT** (0 to 100) is its confidence in each residue's local position: above 90 is very high, below 50 usually means a floppy region. **PAE** (predicted aligned error) says how confident it is about the relative position of two parts, such as two domains.

### Rotamer
One of the few common shapes an amino acid's side chain takes. Mutation tools offer them, ordered by how often they occur in real proteins.

### Mutation notation
A protein change is written as original residue, position, new residue: *Glu6Val*, or *E6V*. HGVS, the standard notation, counts from the start codon's methionine, so hemoglobin's classic sickle-cell "Glu6Val" is *p.Glu7Val* in HGVS.

## Genomics

### Reference genome
The standard sequence that reads are compared against. For humans the current one is GRCh38, also called hg38.

### Read and alignment
A *read* is one short piece of sequenced DNA or RNA. *Alignment* finds where each read belongs on the reference genome.

### BAM and CRAM
File formats for aligned reads. CRAM is smaller because it stores only the differences from the reference.

### Index file
A small companion file (`.bai`, `.crai`, `.tbi`) that lets a program jump straight to one region of a large file. This is how IGV can show one gene from a large remote file.

### Coverage
How many reads overlap a position. Higher coverage means more confidence in what's there.

### Variant, VCF, and rs number
A *variant* is a position where a genome differs from the reference. VCF files list variants. An *rs number* (e.g. rs334, the sickle-cell variant) is the variant's ID in the dbSNP database.

### ClinVar
A public archive of how genetic variants relate to disease, with each variant's clinical interpretation.
