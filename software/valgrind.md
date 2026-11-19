# Valgrind

An instrumentation framework for building dynamic analysis tools for debugging and profiling.

Valgrind is an instrumentation framework used for dynamic analysis of programs, particularly for memory debugging, memory leak detection, and profiling.

**Module name:** `valgrind`

## Loading Valgrind

- module: `valgrind/3.12.0`
- module: `valgrind/3.15.0`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load the Valgrind module**

```
module load valgrind/3.12.2
```

## Availability

Valgrind is available on: SeaWulf.

**Category:** Monitoring & debugging

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/valgrind> (maintained by Research Computing and Informatics).
