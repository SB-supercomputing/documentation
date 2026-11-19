# htop

An interactive process viewer for Unix systems with a user-friendly interface.

htop is an interactive process viewer for Unix systems. It provides a real-time, color-coded interface for monitoring system resources such as CPU, memory, and process usage, allowing easier navigation, sorting, and killing of processes.

**Module name:** `htop`

## Loading htop

- module: `htop/2.2.0`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the htop module**

```
module load htop/2.2.0
```

## Availability

htop is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Monitoring & debugging

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/htop> (maintained by Research Computing and Informatics).
