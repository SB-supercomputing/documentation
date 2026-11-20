# How to submit, delete, and check the status of Slurm job

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

To submit your slurm job to the scheduler, first load the slurm modules:

```
module load slurm
```

Then to submit the job, you can execute the command:

```
sbatch <jobfile>
```

Note that your job script must be saved to a file - copying and pasting the script into the shell will not work!

For a full list of options available to the squeue command issue:

```
man sbatch
```

After you've submitted a job, you chan check the status of the job using the **squeue** command. Issuing this command alone will return the status of every job currently managed by the scheduler. As a result we recommend narrowing the results by user name or job number:

```
squeue --job <your_job_number>
```

or

```
squeue -u <your_user_name>
```

Or, for a full list of options available to the squeue command issue:

```
man squeue
```

If desired, you can issue the following command to delete a job:

```
scancel <job_id>
```

If you are unsure of what your job ID is (it was displayed when you ran sbatch), you can use squeue to get the job ID's of all of your jobs in the queue:

```
squeue -u <your_username>
```

You can learn about more options for the scancel command by reading through the manual page with the command:

```
man scancel
```

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/submit-delete-check-slurm-jobs.php`, retrieved November 5, 2026.
{: .archive-credit }
