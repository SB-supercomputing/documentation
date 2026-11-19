# Compiling-for-performance checklist on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

For getting good performance on Fujitsu A64FX there are a few things to consider during compilation. Please have a look at the [getting-started guide](../../files/support/faq/_docs/Ookami_GettingStarted_032023.pdf) and also see the checklist below for guidance:

- [Compiler(s)](vectorization_flags.md)
    - [Version(s)](vectorization_flags.md)
- [Optimization flags](vectorization_flags.md)
- [Vectorization flags](vectorization_flags.md)
- [Introspection flags](vectorization_flags.md) (ask compiler to tell you what it is optimizing/vectorizing)
- Is the code parallelized?
    - How?
        - MPI + version + underlying compilers
        - OpenMP
        - Threads
        - Other
- Layout of code in NUMA regions, threads, and across compute nodes
    - MPI ranks
    - Threads per rank
    - Placement of ranks

We put together a matrix of useful options for our various compilers [here](vectorization_flags.md)

If you have any questions please use the slack channel, the office hours, or [submit a ticket](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/compiling.php`, retrieved November 5, 2026.
{: .archive-credit }
