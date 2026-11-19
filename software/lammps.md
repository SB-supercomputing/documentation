# LAMMPS

A molecular dynamics simulator widely used for materials science and molecular simulation.

LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) is a molecular dynamics program from Sandia National Laboratories. It runs on single processors or in parallel using message-passing techniques, is distributed as an open-source code under the terms of the GPL, is capable of simulating millions to billions of particles, supports GPU acceleration on compatible hardware, and is extensible via user-contributed packages for specialized applications.

**Module name** `lammps`

## Loading LAMMPS

- module `lammps/a100-gpu/2Aug2023`
- module `lammps/a100-gpu/23Jun2022`
- module `lammps/a100-gpu/29Sep2021`
- module `lammps/gcc13.2/mvapich2.3.7/2Aug2023`
- module `lammps/intel/2022.2/29Oct2020`
- module `lammps/intel/2022.2/03Aug2022`
- module `lammps/intel/2023.1/2Aug2023`
- module `lammps/intel/2024.0/29Aug2024`
- module `lammps/aocc/4.0/2Aug2023`
- module `lammps/aocc/4.0/29Aug2024`
- module `lammps/intel/2023.1/2Aug2023`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `BUILD_TOOLS` Build tools for managing and compiling LAMMPS
- `PKG_SMTBQ` Provides support for the SMTBQ package
- `PKG_MC` Monte Carlo methods for simulations
- `PKG_MEAM` Modified Embedded Atom Method potential
- `PKG_VORONOI` Computes Voronoi tessellations
- `PKG_MANYBODY` Support for many-body potentials
- `PKG_MOLECULE` Support for molecular simulations
- `PKG_PYTHON` Enables Python scripting interface
- `PKG_COMPRESS` Enables support for compressed file I/O
- `PKG_OPT` Performance optimization package
- `PKG_KSPACE` Long-range electrostatics and van der Waals interactions
- `PKG_QEQ` Charge equilibrium method for atomic systems
- `PKG_REACTION` Reactive force fields for chemical reactions
- `PKG_RIGID` Tools for rigid body dynamics simulations
- `PKG_BODY` Support for complex body simulations
- `PKG_SPH` Smoothed Particle Hydrodynamics (SPH) package
- `PKG_GRANULAR` Granular material simulations
- `PKG_DIPOLE` Polarization and dipole interactions
- `PKG_SHOCK` Shockwave and impact simulations
- `PKG_SRD` Stochastic rotation dynamics for mesoscale flows
- `PKG_CORESHELL` Core-shell particle interactions
- `PKG_VORO` Voronoi-based analysis tools
- `PKG_REPLICA` Methods for replica exchange simulations
- `PKG_PERI` Peridynamics modeling package
- `PKG_MISC` Miscellaneous features and utilities
- `PKG_OPENMP` Enables OpenMP parallelization
- `WITH_PNG` Enables PNG image support
- `WITH_JPEG` Enables JPEG image support
- `FFT=MKL` Uses Intel MKL for FFT computations
- `PKG_MPIIO` Enables MPI-IO support for parallel I/O

## Example usage

**Load a LAMMPS module (general form)**

```
module load lammps/<compiler>/<version>
```

**Load a CPU (Intel) LAMMPS module**

```
module load lammps/intel/2024.0/29Aug2024
```

**Load an A100 GPU LAMMPS module**

```
module load lammps/a100-gpu/2Aug2023
```

**Run LAMMPS in parallel with MPI**

```
mpirun -np <number_of_processes> lmp -in <input_file>
```

**Enable GPU package in a LAMMPS input**

```
package gpu 1 neigh yes newton on
```

**Run LAMMPS on 40 CPU cores**

```
mpirun -np 40 lmp_mpi -in input.lammps -log log.lammps
```

**Run GPU-enabled LAMMPS**

```
mpirun -np 4 lmp_gpu -in input.lammps -log log.lammps -var GPU 1
```

**CPU Slurm job script example**

```
#!/bin/bash
#SBATCH --job-name=lammps_cpu
#SBATCH --output=lammps_%j.out
#SBATCH --error=lammps_%j.err
#SBATCH -p short-40core
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=40 module load lammps/intel/2024.0/29Aug2024 INPUT="input.lammps"
LOG="log.lammps" mpirun -np $SLURM_NTASKS lmp_mpi -in $INPUT -log $LOG
```

**GPU Slurm job script example**

```
#!/bin/bash
#SBATCH --job-name=lammps_gpu
#SBATCH --output=lammps_%j.out
#SBATCH --error=lammps_%j.err
#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH -p a100
#SBATCH --gres=gpu:4
#SBATCH --ntasks=4 module load lammps/a100-gpu/2Aug2023 INPUT="input.lammps"
LOG="log.lammps" mpirun -np $SLURM_NTASKS lmp_gpu -in $INPUT -log $LOG
```

## Availability

LAMMPS is available on: SeaWulf, NVwulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">NVwulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/lammps> (maintained by Research Computing and Informatics).
{: .rci-credit }
