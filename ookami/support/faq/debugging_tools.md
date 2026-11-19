# Debugging tools

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

## gdb

[gdb](https://www.gnu.org/software/gdb/) is the GNU debugging tool. gdb works by default without loading a specific module.

---

## gdb4hpc

gdb4hpc is a parallel debugger for C, C++ and Fortran programs and is available on both the MACS and XCI systems as part of the Cray Programming Environment. It is a command line tool (based on gdb) and it can be used either to launch an application or attach to application which is already running.

It can be loaded via

module load CPE
module load gdb4hpc

---

## ddt

ddt is Linaro's (formerly Arm's) debbuging tool. It can be launched via a GUI.

[Guide](../../files/support/faq/_docs/Linaro-Ookami.pdf) on how to use the Forge remote client on Ookami

---

## valgrind

[valgrind](https://www.valgrind.org/) is an instrumentation framework for building dynamic analysis tools. valgrind works by default without loading any additional modules.

---

## valgrind4hpc

valgrind4hpc is a parallel memory debugging tool that aids in detection of memory leaks and errors in parallel applications.

It can be loaded via

module load CPE
module load valgrind4hpc

---

## CCDB

This is the Cray Comparative Debugger, which can be loaded via

module load CPE
module load cray-ccdb

Note that SSH X forwarding must be activated to open the GUI.

---

## ATP

Cray's Abnormal Termination Processing can be loaded via

module load CPE
module load atp

---

## STAT

Cray's Stack Trace Analysis Tool can be loaded via

module load CPE
module load cray-stat

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/debugging_tools.php`, retrieved November 5, 2026.
{: .archive-credit }
