# Conditional Compilation by Architecture

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

This entry covers determining your current system's architecture, finding the predefined macro for the target architecture, and using preprocessor directives to achieve conditional compilation.

Determining current system architecture

By using **lscpu** and looking at the **Architecture** field, we can determine the current system's architecture.

```
Architecture:        aarch64
Byte Order:          Little Endian
CPU(s):              256
On-line CPU(s) list: 0-255
Thread(s) per core:  4
Core(s) per socket:  32
Socket(s):           2
NUMA node(s):        2
Vendor ID:           Cavium
Model:               1
Model name:          ThunderX2 99xx
Stepping:            0x1
BogoMIPS:            400.00
L1d cache:           32K
L1i cache:           32K
L2 cache:            256K
L3 cache:            32768K
NUMA node0 CPU(s):   0-127
NUMA node1 CPU(s):   128-255
Flags:               fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics cpuid asimdrdm
```

Finding the predefined C macro for the target architecture

Using the command shown below, you can find a list of potentially useful predefined macros for your C or C++ code.

```
gcc -dM -E - < /dev/null 
```

We can use the architecture we obtained from lscpu to filter this list of macros to look for our architecture's macro. Different machines will define a different macro depending on the architecture.

```
$ gcc -dM -E - < /dev/null | grep aarch64
#define __aarch64__ 1
```

Conditional Compilation

By using preprocessor directives such as #ifdef and #else in combination with the macro we obtained in the last section, we can define code to be compiled a certain way if it's an aarch64 and a different way otherwise.

```
#ifdef __aarch64__

#include <stdint.h>

long long readTSC(void)
{
    uint64_t ticks;

    asm volatile("isb" : : : "memory");
    asm volatile("mrs %0, cntvct_el0" : "=r" (ticks));
    return (long long) ticks;
}

#else

long long readTSC(void)
{
    union { long long complete; unsigned int part[2]; } ticks;
  __asm__ ("rdtsc; mov %%eax,%0;mov %%edx,%1"
            : "=mr" (ticks.part[0]),
              "=mr" (ticks.part[1])
            : /* no inputs */
            : "eax", "edx");
  return ticks.complete;
}

#endif
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/conditional_compilation_by_architecture.php`, retrieved November 5, 2026.
{: .archive-credit }
