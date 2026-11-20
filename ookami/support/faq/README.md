# Frequently Asked Questions

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

## What is Ookami?

Ookami is a testbed for researchers nationwide to explore future supercomputing technologies and to advance computational and data-driven research on pressing science challenges.

Unique and novel features include:

- First access for US research and first planned install of A64fx outside of Japan
- First CPU worldwide with on-package high bandwidth memory (1 TB/s, 82% peak measured on STREAM triad is 8x Sky Lake socket)
- First CPU worldwide to implement the ARM scalable vector extensions with multiple features to facilitate auto-vectorization
- High CPU performance (2.76dpTFLOP/s, dgemm 94% peak) balanced to match memory speed giving ~0.4 bytes/dpFLOP is unparalleled in modern CPUs (4.6x Sky Lake, 3x NVIDIA V100)
- Green technology with high power efficiency.

What does this mean for science? Compared with the best CPUs anticipated for the deployment era, A64fx offers 2-4x better performance on memory-intensive applications such as sparse-matrix solvers found in many engineering and physics codes. For nearly all other applications performance is also better or competitive.

## Getting Started

#### [How do I request an Ookami account?](ookami-account-request.md)

#### [How do I get a project on Ookami?](getting-a-project-on-ookami.md)

#### [How do I log into Ookami?](logging-into-ookami.md)

#### [How do I enroll in DUO Security?](enroll-in-duo-security.md)

#### [Getting Started Guide](getting-started-guide.md)

## SLURM Jobs

#### [Can you give me an example of a Slurm job script?](example-slurm-script.md)

#### [How do I control threads and CPUs on Ookami using Slurm?](core-thread-control-ookami.md)

#### [How do I control threads and CPUs on Ookami using MPI flags?](core-thread-control-mpi-flags.md)

#### [How do I control threads and CPUs on Ookami using OpenMP?](thread_binding.md)

#### [How can I submit, delete, and check the status of Slurm jobs?](submit-delete-check-slurm-jobs.md)

#### [How do I handle output from my job?](handling-job-output.md)

#### [How do I submit interactive jobs?](interactive_slurm_session.md)

## Environment

#### [What are the login nodes?](understanding_login_nodes.md)

#### [What are modules?](what_are_modules.md)

#### [What are the Ookami queues?](queues_on_ookami.md)

#### [What software is installed on Ookami?](software_on_ookami.md)

#### [Using Open OnDemand](open_ondemand.md)

## Compilers

#### [How can I use the ARM compilers?](ookami-arm-compilers.md)

#### [How can I use the Cray compilers?](ookami-cray-compilers.md)

#### [How can I use the GCC compilers?](ookami-gcc-compilers.md)

#### [How can I use the AMD compilers?](ookami-amd-compilers.md)

#### [How can I use the NVIDIA compilers?](ookami-nvidia-compilers.md)

## Storage

#### [What are the Ookami storage options?](ookami_storage_options.md)

#### [How do I make sure permissions are set properly in my project space?](project_space_permissions.md)

## Optimization

#### [Useful flags for vectorization](vectorization_flags.md)

#### [Simple example: Vectorization for different compilers](vectorization_example.md)

#### [Profiling tools on Ookami](profilers.md)

## Miscellaneous

#### [How should I acknowledge the Ookami in my publication?](iacs_acknowledgement.md)

#### [Are there HIPAA concerns associated with Ookami?](hipaa_concerns.md)

#### [How do I reset my Ookami password?](resetting_ookami_password.md)

#### [How do I set up passwordless SSH?](passwordless_ssh.md)

#### [How do I transfer files to and from Ookami?](transferring_data_to_ookami.md)

#### [What does "Connection reset by peer" or "Your account has been locked out" mean?](fixing_common_login_issues.md)

#### [What does "WARNING: LD_LIBRARY_PATH_modshare exists..." mean?](warning_modshare_library_path_duo.md)

#### [DUO and LD_LIBRARY_PATH](warning_modshare_library_path_duo.md)

#### [Getting troubleshooting help](remote_troubleshooting.md)

#### [How can I monitor Ookami's usage?](xdmod.md)

#### [How to fix common login issues](fixing_common_login_issues.md)

#### [How can I check I monitor the power consumption of my job?](power_usage.md)

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/`, retrieved November 5, 2026.
{: .archive-credit }
