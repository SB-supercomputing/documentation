# Getting Started Guide

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

Have a look a this guide

[Ookami - Getting Started](../../files/support/faq/_docs/Ookami_GettingStarted_012025.pdf)

## Introduction

This guide assumes that you already have access to Ookami and that you are able to log in. It serves to get you acquainted with the environment you will be interacting with once on the system.

## Basic Linux Commands

Unlike a desktop, you interact with this operating system through the **terminal**, sometimes referred to as the **commandline**. Windows and OS X both have their own version of the terminal, even though most users choose not to use them. Here, the use of the terminal is mandatory, so it is important that you know your way around it.

### mkdir

When you first log in you will arrive in your **homedirectory**. This is your own private folder to store things related to your work. You can make subdirectories, files, and even install software here. Making a subdirectory is simple. Use the **mkdir** command:

```
mkdir <directory name>
```

Here, &lt;directory name> is the name you want to give the folder.

### ls and pwd

After you have done this, you can use the **ls** command to verify that the directory has been created without issue. Typing in **ls** will result in a list of files and subdirectories being printed back to you, all of which are located in your **present working directory.** Your **working directory** is the command line equivalent of your current folder in Windows Explorer or Finder - it's the directory that you're currently looking at. When you type the **pwd** command, your working directory will be printed out to you:

```
 /lustre/home/<my netid>
```

The top-level directory, equivalent to C: on Windows, is always /lustre. The home subdirectory of /lustre contains all users' home directories.

### cd

To change your present working directory, you can use the **cd** command, which stands for **change directory.**

```
cd <path>
```

You can change your directory using either an **absolute** or **relative** path. An absolute path begins with a forward-slash and specifies each level of subdirectories, starting from the root folder (which contains lustre). A relative path does not start with a forward-slash, and fills in each subdirectory level up to the directory you're currently in. For example, if you are in /lustre/home/&lt;your username> and want to move to a subdirectory in that folder, just give cd the subdirectory name.

### touch

If instead of a folder you would rather create a blank text file, you can use the **touch** command:

```
touch <new filename>
```

You can then edit this file with a text editor of your choice (e.g., nano, vim, or emacs).

### rm

If you want to delete a file or folder, you can use the **rm** command (short for **remove).** This command will permanently delete anything you tell it to (no trash bin!). You will pass this command different **options,** depending on what it is you want to remove. For a regular file, you can choose not to pass it any options at all:

```
rm <file to remove>
```

However, if you want to remove an entire directory (even if it's empty), you will have to pass it the **-r** option (short for **recursive**):

```
rm -r <folder to remove>
```

This will remove *everything* in that directory, files and subdirectories included. The recursive option is called such because it recursively deletes everything it finds.

A word of warning - it is very easy to accidentally delete important information. Be very careful when using this command.

Most of these commands have a **help** or **-h** option. If you forget how to use a command, simply type that command followed by **-h** to get a description of it.

## Modules

All of the commands described above are not programs, but functionality built into the **shell.** The shell is the program you're interacting with whenever you type something into the terminal, and is always running. In addition to these commands, the shell has a few helpful features, one of which is the existence of **environment variables.** These are little bits of data that all programs can access, but which go away any time you log out. Typically they are used for storing paths to directories so that programs know where to look for the files they need.

Yet another command is the **env** command, which lists all of your environment variables. When you type this command, you will see something like this printed to your screen:

```
...
COLLECTION_DATA=/data/collection
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session0
rvm_path=/home/austin/.rvm
XDG_SEAT_PATH=/org/freedesktop/DisplayManager/Seat0
SSH_AUTH_SOCK=/run/user/1000/keyring/ssh
DEFAULTS_PATH=/usr/share/gconf/ubuntu.default.path
XDG_CONFIG_DIRS=/etc/xdg/xdg-ubuntu:/usr/share/upstart/xdg:/etc/xdg
rvm_prefix=/home/austin
...
```

Each line is an individual environment variable. The name of the environment variable is in all caps (e.g. COLLECTION_DATA), and its value to the right of the equals sign.

Dealing with defining these every time you log in is cumbersome, which is why we have installed a software package to simplify the process. Using the **module** command (a program, this time), you can load and unload environment variables that you commonly need, depending on the software you use. The module command has several subcommands that perform different functions. The most common subcommands are:

```
module avail
module load <some module>
module list
module unload <some module>
```

The **load** subcommand will load a module. This will make a certain software package callable from the terminal. If, for example, you load the cmake/3.22.1 module, you will be able to start CMake by typing in the command "cmake".

The **list** subcommand will show you a list of all the modules you have loaded since logging in.

The **avail** subcommand will list all of the modules that are available to be loaded. When you first log in, only a limited selection of local modules will be displayed. To view all of the software that is installed globally on Ookami, you must first load the shared module with:

```
module load shared
```

Special requests can be made to install software globally (outside of a home directory) through the ticketing system and are reviewed for notoriety of the software in question.

If you accidentally load the wrong software package or want to switch to a different version of the same software, you should use the **unload** command to erase the environment variables associated with that software. If, for example, you decide that gcc/10.3.0 is insufficient and want to switch to the gcc/11.3.0 release, you would first unload the gcc/10.3.0 module, then load the gcc/11.3.0 module.

Other subcommands exist. To see a list of these subcommands and how to use them, type the following command.

```
module help
```

## Slurm

Now that you know the basic ways of interacting with Ookami, the next step is to understand how to use it to run computational software. Ookami has what is called the **login node.** Each node on Ookami is an individual computer that is networked to all the other nodes, forming a computing cluster. The login node is the entry point to the cluster and only exists as an interface to use the other nodes. Since the beginning of this guide, you have been interacting with this node. Because everybody will be on this node, it shouldn't be used for heavy computation—otherwise, the system would slow down and become unusable. To actually run heavy computation, you will have to run your software on the **compute nodes.**

To manage demand, we use a scheduling system called **Slurm** to grant you access to the compute nodes and run your job when nodes become available. All Slurm commands can only be used after loading its module:

```
module load slurm
```

## Running an interactive job

Loading the Slurm module gives you access to several commands, one of which is **srun.** There are several different ways to use this command. To start off, we will begin an **interactive job** which asks for one compute node.

All Slurm commands can only be used after loading its module:

```
module load slurm
```

After loading the slurm module, you can request an interactive job with:

```
 srun -p short -N 1 -n 48 --pty bash
```

In the command above, **-N 1** indicates that we are requesting a single node, while **-n 48** requests access to all 48 cores on that node. The **--pty bash** option indicates that we want to manually control a node through the terminal. The **-p** flag specifies which queue you want to wait in. Slurm documentation uses the word "partition" instead of "queue"; our FAQ pages will use these terms interchangeably.

After running this command you will either be waiting in the short queue or given a node immediately. This depends on the demand at the time. You can use the **squeue** command to show a list of jobs and their status to estimate how long you may be waiting in the queue.

Once granted access, your terminal will be interacting with the compute node instead of the login node. Here, you can test software you have installed, as you are the only user on this node and have access to all its resources.

To end the interactive job session and return to the login node, type **exit.**

### Loading the Cray environment/modules

The Ookami cluster includes several modules comprising the Cray Programming Environment (CPE), which is aimed at providing compilers, libraries, and performance analysis tools for the ARM-based compute nodes.

In order to load the Cray environment, please do the following (Note: currently only available on the compute nodes):

```
module load CPE
```

You can use the **module list** command to see which modules have just been loaded. Note also that loading the CPE module makes several additional modules available (e.g., cray-based mvapich2 MPI), which can be checked with **module avail.**

You should now be able to use the Cray computing environment on a compute node.

## Running an automated job with Slurm

Interactive jobs are good for testing your code or installed software, but should not be used for long running computational jobs since your job will end once you log off. An automated job will run until finished, and with it you won't have to retype commands all the time.

To run an automated job with Slurm, you will need to write a job script. A job script is a text file that contains all of the information needed to run your job. Your job script will contain special Slurm directives starting with **#SBATCH** that specify job options, like the number of nodes desired and the expected completion time. Make sure that your #SBATCH directives look exactly like the example below (no space between # and SBATCH and SBATCH is all capitalized).

Here is an example Slurm script and the example MPI program modified from the [Cray Programming Environment User Guide](https://pubs.cray.com/bundle/HPE_Cray_Programming_Environment_User_Guide_For_Apollo_80_ARM_Apollo80/page/Example_MPI_Program_Source.html).

(Save this as mpi_hello.c)

```
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);

int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;

MPI_Get_processor_name(processor_name, &name_len);

printf (
    "Hello world from node %s, rank %d out of %d processors\n",
    processor_name,
    world_rank,
    world_size
);
MPI_Finalize();

return 0;
}
```

Slurm script:

```
#!/usr/bin/env bash

#SBATCH --job-name=mpi_test
#SBATCH --output=mpi_test.log
#SBATCH --time=05:00
#SBATCH -p short
#SBATCH -N 2
#SBATCH --ntasks-per-node=48
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=<your email>@stonybrook.edu

module load slurm
module load CPE
module load cray-mvapich2_nogpu_sve/2.3.6

mpicc mpi_hello.c -o mpi_hello

srun -N2 ./mpi_hello
```

The **--job-name** option gives the job a name so that it can be easily found in the list of queued and running jobs. The next lines specify the **--output** file, to which script results will be written, the **--time** that the job is expected to take (if you run without a specified time, the queues have default runtimes), the partition (**-p**) that the job will be submitted to, the number of nodes to use (**-N 2**), and the number of cores per node (**--ntasks-per-node**). The **--mail-type** and **--mail-user** options are not required but control whether the user should be notified via email when the job state changes (in this case when the job starts and finishes). There are many other potentially useful SBATCH options that you can set. You can read about them [here](https://slurm.schedmd.com/sbatch.html).

The next three lines load the modules required to find the software run by the script.

Note that the Slurm script for Ookami differs from MPI scripts that you may have used on Seawulf in that the command to run the compiled program is called with **srun,** and not **mpirun** or **mpiexec.**

Save this job submission script as mpi_hello.slurm (the ".slurm" extension is arbitrary but useful for differentiating Slurm scripts from regular shell scripts )

Make sure that you have already loaded the Slurm module, and then submit your job with:

```
sbatch mpi_hello.slurm
```

Your job will be placed in the specified queue and will run without your involvement. If you want to cancel the job at any point, you can use the **scancel** command, providing the number at the beginning of the job id found in the first column of the squeue printout.

Once your job has finished running, you should see a "Hello World" statement from each of 96 cores across two different nodes printed in the output file.

## Checking job status

First, make sure you have loaded the Slurm module:

```
module load slurm
```

After you've submitted a job, you can check the status of your job in the queue using the **squeue** command. Issuing this command alone will return the status of every job currently managed by the scheduler. As a result we recommend narrowing the results by user name or job number:

```
squeue -j <your_job_number>
```

or

```
squeue -u <your_user_name>
```

Or, for a full list of options available to the squeue command:

```
man squeue
```

The documentation for all Slurm commands can be found [here](https://slurm.schedmd.com/documentation.html).

## DUO Two Factor Authentication

You are required to use DUO security to authenticate your login to Ookami. DUO provides an additional layer of security on the Ookami cluster by asking you to confirm your login attempt by accepting a push notification to your smart phone.

Please check your email for a personalized invitation allowing you to enroll with DUO. Please click the link in your email and follow this article on the DUO enrollment process. It is recommended to enroll two devices in DUO.

The Division of Information Technology offers the [DUO service page](https://it.stonybrook.edu/services/duo-security-two-step-login), which can be referred to for additional information regarding this service.

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/getting-started-guide.php`, retrieved November 5, 2026.
{: .archive-credit }
