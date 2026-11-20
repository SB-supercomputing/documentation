# Profilers on Ookami

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

There are several profiling tools available on the system

---

## gprof

You can find the documentation [here](https://sourceware.org/binutils/docs/gprof/index.html). gprof collects information of a program during runtime. To profile your program use the ‘`-pg`’ option for compiling and linking.

```
cc -g -c myprog.c utils.c -pg
cc -o myprog myprog.o utils.o -pg
```

Run the program as usual ./myprog. The program will run as usual and produce its usual output. It might be a little bit slower due to the time spent collecting and writing the profile data.

The profile are written in a file called gmon.out which is located in the same directory as where you executed your program. Your program must exit normally for this file to be written.

Now you can run `gprof` to interpret the information. The `gprof` program prints a flat profile and a call graph on standard output. Optionally you can pipe the output to a file and save it.

```
gprof ./myprog > gprof_output.txt
```

---

## perf

You can find the documentation [here](https://perf.wiki.kernel.org/index.php/Main_Page). perf is a simple command line tool profiler. No special compiler flags have to be used for using perf.

The perf tool supports a list of measurable events. Run perf list to generate the full list of events that are allowed by the -e flag. Here is an example of how to output the duration and the cpu-cycles of a program

```
perf stat -e duration_time -e cpu-cycles ./myprog
```

---

## Linaro forge tools (formerly arm forge)

To use these tools the appropriate modules have to be loaded

```
module load linaro/forge/23.0
```

Ookami has a limited number of licences for this toolchain. It's possible to get an error when compiling with arm or using the forge tools, saying that there are no available licences. If this happens, you have to wait until another user does not need his licence anymore.
Documentation can be found [here](https://www.linaroforge.com/documentation/).

## MAP

MAP is a source-level profiler and can show how much time was spent on each line of code.

Compile your code with -g to enable source code line details. The profile can be generated either by running the program

```
map --profile ./a.out
```

This will produce a .map file which can be loaded into the GUI

Or follow this [Guide](../../files/support/faq/_docs/Linaro-Ookami.pdf) on how to use the Forge remote client on Ookami

*Note:*
If you want to use map with cray-mvapich you have to

```
export ALLINEA_WRAPPER_COMPILE
```

---

## perf-report

Documentation can be found [here](https://developer.arm.com/documentation/101136/2021/Performance-Reports?lang=en).

perf-report takes samples of the program at a given intervall. Arm recommends to take at least 1000 samples. Hence choose your example such that the program runs long enough. Running your executable with

```
perf-report ./a.out
```

will produce a .html file which can be opened in a browser and provides high level analysis of the program (e.g. how much time is spent in compute, MPI and I/O). Also a .txt is produced, which gives the same information and can be opened in an editor.

---

## Cray tools

Cray has various profiling tools in its toolsuite. Start by loading cray

```
module load CPE
```

## PAPI

The documentation can be found [here](http://icl.cs.utk.edu/papi/).

PAPI provides a consistent interface and methodology for use of the performance counter hardware found in most major microprocessors. In addition, PAPI provides access to a collection of components that expose performance measurement opportunites across the hardware and software stack.

## perftools-lite

Documentation can be found [here](https://pubs.cray.com/bundle/Cray_Perftools_Quick_Start_Guide_10_S-2632/page/perftools-lite.html).

PerfTools-lite is a simplified, easy-to-use version of the Cray Performance Measurement and Analysis Tool set. It provides basic performance analysis information automatically.

## CrayPat

Documentation can be found [here](https://pubs.cray.com/bundle/Cray_Performance_Measurement_and_Analysis_Tools_Installation_Guide_632_S-2474/page/Use_CrayPat_CrayPat-lite_Apprentice2_or_Reveal.html).

CrayPat allows a user to re/instrument compiled binaries (executable files) and select aspects to specifically profile, including items such as MPI and OpenMP API’s, shared memory, and a/synchronous I/O.

## Reveal

Documentation can be found here.

Cray Reveal utilizes the Cray CCE program library for source code analysis, combined with performance data collected from CrayPat. Reveal helps to identify top time-consuming loops, with compiler feedback on dependency and vectorization.

---

## TAU

Documentation can be found [here](https://www.cs.uoregon.edu/research/tau/home.php).

TAU Performance System® is a portable profiling and tracing toolkit for performance analysis of parallel programs written in Fortran, C, C++, UPC, Java, Python. You can find recordings of a TAU webinar on Ookami in our [recordings section](../index_links_and_docs.md).

---

## likwid

Documentation can be found [here](https://github.com/RRZE-HPC/likwid).

Likwid is a simple to install and use toolsuite of command line applications and a library for performance oriented programmers. It can be loaded via

```
module load likwid/5.1.1
```

---

## OSACA

Documentation can be found [here](https://github.com/RRZE-HPC/OSACA).

For an innermost loop kernel in assembly, this tool allows automatic instruction fetching of assembly code and automatic runtime prediction including throughput analysis and detection for critical path and loop-carried dependencies. It can be loaded via

```
module load anaconda/3
source activate OSACA
```

---

## perfalloc

Documentation can be found [here](https://man7.org/linux/man-pages/man1/perfalloc.1.html).

To use this you probably have to swith off the PCP hardware counter collection.
You can do this by running the perfalloc command

```
/var/lib/pcp/pmdas/perfevent/perfalloc
```

---

## Google Performance Tools

Documentation can be found [here](https://github.com/gperftools/gperftools).

The module can be loaded via

```
module load gperftools/2.9.1
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/profilers.php`, retrieved November 5, 2026.
{: .archive-credit }
