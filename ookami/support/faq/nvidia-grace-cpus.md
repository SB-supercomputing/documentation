# Using Ookami's NVIDIA Grace CPUs

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

We are pleased to announce the addition of two [NVIDIA Grace superchips](https://www.nvidia.com/en-us/data-center/grace-cpu-superchip/) to Ookami. These new nodes with 144 cores each are now available for your testing and experimental projects.

**Learn more about the NVIDIA Grace superchip:**

- [Datasheet](https://resources.nvidia.com/en-us-grace-cpu/data-center-datasheet)
- [White Paper](https://resources.nvidia.com/en-us-grace-cpu/nvidia-grace-cpu-superchip#page=1)

---

**Access Details:**

You can access these CPUs via SSH from any other node of the cluster, i.e.

```
 ssh fj-grace1
```

or

```
 ssh fj-grace2
```

---

**Using the nodes:**

Following compilers will work on the Grace nodes:

- gcc/13.2.0
- Nvidia nvhpc
- LLVM
- Arm

Please also have a look at the

[NVIDIA guide](https://nvidia.github.io/grace-cpu-benchmarking-guide/)

[NVIDIA Grace Performance Tuning Guide](https://docs.nvidia.com/grace-performance-tuning-guide.pdf)

Recommended flags for the LLVM compiler (see the NVIDIA Grace Performance Tuning Guide)

|  |  |  |
| --- | --- | --- |
| **LLVM Compiler** | | |
| **Optimization Level** | **Flags** | **Notes** |
| Aggressive | -Ofast<br>-mcpu=neoverse-v2 | Enable fast math optimizations |
| Moderate | -O3 -mcpu=neoverse-v2 | Recommended in most cases |
| Conservative | -O3 -ffp-contract=off<br>-mcpu=neoverse-v2 | Recommended in most cases |

Recommended flags for the GCC compiler (see the NVIDIA Grace Performance Tuning Guide)

|  |  |  |
| --- | --- | --- |
| **GCC Compiler** | | |
| **Optimization Level** | **Flags** | **Notes** |
| Aggressive | -Ofast<br>-mcpu=neoverse-v2 | Enable fast math optimizations |
| Moderate | -O3 -mcpu=neoverse-v2 | Recommended in most cases |

---

**Power Measurements:**

The power on the nodes is measured using the system's ipmi tool. You can access the data in the following folder

```
/lustre/admin/power_monitoring/power/year/year&month/month&day
```

e.g. the data for 05/01/2024 would be located in

```
/lustre/admin/power_monitoring/power/2024/202405/0501
```

In the folder are several files, each containing the power measurements of a single node. The naming of the files reads as power_orginfo_ *IP address of the node* _ *date*.csv

The IP address of the grace nodes are

- 10.10.1.200 for fj-grace1
- 10.10.1.201 for fj-grace2

Hence the file containing the measurements on 05/01/2024 for fj-grace1 would be

```
/lustre/admin/power_monitoring/power/2024/202405/0501/power_orginfo_10.10.1.200_20240501.csv
```

The file contains two columns. The first column is the time of the day and the second the power measurement in W.

---

**Node Usage and Policy:**

The Grace CPU nodes are shared resources. As they are primarily intended for testing purposes, we kindly ask you to manage your usage time and computational load considerately to allow equitable access for all users.

We hope you find these new additions valuable for your research and development efforts. Should you have any questions or require further assistance, please do not hesitate to contact our support team.

[Submit a ticket](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/NVIDIA%20Grace%20CPUs.php`, retrieved November 5, 2026.
{: .archive-credit }
