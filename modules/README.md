# Curriculum

Kitsune's training is organised in three tracks. A module is a short course. Each is taught as a workshop or a webinar series, and written so you can work through it alone. The tutorials listed under a module are single lessons, 5 to 15 minutes each, that you can take whenever you need them.

Modules marked *in draft* have an outline but no dates yet. Lessons without a link are still being written.

## A. Onboarding

- [**Basics of using Kitsune**](A1-cluster-basics.md) *(in draft)*: your account, the shell, where files live, and a first job.
- [**Using Slurm**](A2-slurm.md) *(in draft)*: asking for cores, memory, and time; finding out why a job waits or fails; job arrays.
- [**Open OnDemand**](A3-open-ondemand.md) *(in draft)*: using the cluster from a browser for files and for interactive apps.
  - [Start an OnDemand session](../tutorials/visualization/start/ondemand-session.md)
  - [Get your data where the app can see it](../tutorials/visualization/start/your-data.md)

## B. Productivity & Data

- [**Advanced shell**](B1-advanced-shell.md) *(in draft)*: scripting, text processing, and running many small tasks.
- [**Data management**](B2-data-management.md) *(in draft)*: where data lives, what to keep, and how to describe it.
- [**Data transfer**](B3-data-transfer.md) *(in draft)*: moving large data on and off the cluster.
- [**HDF5**](B4-hdf5.md) *(in draft)*: a portable, self-describing format for large scientific data.
- [**Visualization**](B5-visualization.md): seeing simulation output, molecules, and volumes, and making the same picture again by script.
  - [Start ParaView on OnDemand](../tutorials/visualization/tools/paraview.md)
  - [Draw streamlines in ParaView](../tutorials/visualization/vectors/streamlines/paraview.md)
  - [See orbitals and electron density in ParaView](../tutorials/visualization/densities/orbitals-and-density/paraview.md)
  - Comparisons of the programs that can do one lesson: [streamlines](../tutorials/visualization/vectors/streamlines/README.md), [orbitals and electron density](../tutorials/visualization/densities/orbitals-and-density/README.md)

## C. Parallel & Performance

- [**OpenMP**](C1-openmp.md) *(in draft)*: threads on one node.
- [**MPI**](C2-mpi.md) *(in draft)*: processes across nodes.
- [**Profiling & optimization**](C3-profiling-optimization.md) *(in draft)*: measuring where a program spends its time, and fixing what you find.

## Where to start

Do [Start an OnDemand session](../tutorials/visualization/start/ondemand-session.md) once, then take the module that matches your work. Do the A track first. It assumes no cluster experience, while tracks B and C assume you can submit a job.
