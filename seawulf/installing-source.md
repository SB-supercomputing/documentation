# Installing from source

## When to install from source

- The software is not available as a module ( check `module avail` and `conda search` first)
- You need a newer version than provided, or specific compile-time options
- You're developing or modifying the software yourself
- The software needs architecture-specific optimizations

## Choosing a location

Home (`--prefix=$HOME/software/myapp-1.0`) is backed up but capped at 20 GB; project space is large and shared but not backed up. **Never** install in scratch: the 45-day purge will break the installation.

## Match the architecture

| Architecture | GCC/Clang flag | Intel flag | Example partition |
| --- | --- | --- | --- |
| 40-core Intel Skylake | `-march=skylake-avx512` | `-xCORE-AVX512` | `short-40core` |
| 96-core AMD EPYC Milan | `-march=znver3` | None | `short-96core` |
| 96-core Sapphire Rapids | `-march=sapphirerapids` (GCC ≥12) | `-xCORE-AVX512` | `hbm-short-96core` |

> [!TIP]
> Running on multiple architectures? Compile separate versions, or use generic flags like `-march=x86-64` for compatibility at some performance cost.

## Load compilers and dependencies

```
module avail gcc && module avail intel
module load gcc/11.2.0            # or: module load intel/oneAPI/2023.1 compiler
module load cmake/3.24.2
module load openmpi/4.1.4

# specify compilers explicitly when needed
export CC=gcc CXX=g++ FC=gfortran        # GNU
export CC=icx CXX=icpx FC=ifx            # Intel oneAPI
```

## Basic process

1. **Download and extract.**

    ```
    wget https://example.com/software-1.0.tar.gz
    tar -xzf software-1.0.tar.gz && cd software-1.0
    ```

2. **Configure.** Autotools:

    ```
    ./configure --prefix=$HOME/software/myapp-1.0 \
                CFLAGS="-O3 -march=skylake-avx512" \
                CXXFLAGS="-O3 -march=skylake-avx512"
    ```

    or CMake:

    ```
    mkdir build && cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/software/myapp-1.0 \
             -DCMAKE_BUILD_TYPE=Release \
             -DCMAKE_C_FLAGS="-O3 -march=skylake-avx512"
    ```

3. **Compile.**

    ```
    make -j $(nproc)
    ```

    Avoid more than a few cores on login nodes: request an [interactive job](../shared/interactive-jobs.md) for large builds (see [login node etiquette](../shared/login-node-etiquette.md)).

4. **Test.**

    ```
    make check   # or: make test
    ```

5. **Install.**

    ```
    make install
    ```

## After installation

```
export PATH=$HOME/software/myapp-1.0/bin:$PATH
export LD_LIBRARY_PATH=$HOME/software/myapp-1.0/lib:$LD_LIBRARY_PATH
```

Add these to `~/.bashrc` for interactive use, and include them in every SBATCH script that uses the software: **loading the same modules at runtime that you used at compile time**.

## Personal modulefiles (advanced)

```
mkdir -p $HOME/privatemodules/myapp
# create $HOME/privatemodules/myapp/1.0 following the system modulefile format
module use $HOME/privatemodules    # add to ~/.bashrc
module load myapp/1.0
```

## Troubleshooting

- **Compiler not found**: load a compiler module first
- **Missing dependencies**: check `module avail dependency-name`
- **Crashes immediately**: library path issue; check with `ldd` and fix `LD_LIBRARY_PATH`
- **Undefined references**: load the same modules as at compile time
- **Poor performance**: recompile with `-O3` and the right `-march` flag
- **Won't run on another node type**: architecture-specific build; use generic flags or separate builds

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/installing-source> (maintained by Research Computing and Informatics).
