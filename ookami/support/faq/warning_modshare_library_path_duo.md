# DUO and LD_LIBRARY_PATH

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

If you have module load statements in your ~/.bashrc file, you may have noticed the following error show up:

```
WARNING: LD_LIBRARY_PATH_modshare exists
( /cm/shared/apps/slurm/19.05.7/lib64/slurm:1:/cm/shared/apps/slurm/19.05.7/lib64:1),
but LD_LIBRARY_PATH doesn't. Environment is corrupted.
```

This is due to an issue with the DUO two factor authentication system. For some reason, DUO's authentication script prevents module load statements in your .bashrc from modifying the LD_LIBRARY_PATH environment variable. Luckily, the issue can be solved by adding this line to the top of your .bashrc:

```
[[ $- != *i* ]] && return
```

This line will prevent your .bashrc from being run if you're starting a non-interactive session. The initial DUO login script runs non-interactively and then starts an interactive shell session after you've authenticated, so this way it no longer interferes with things loaded in your .bashrc. This does come with a caveat: if you are setting the DUO_PASSCODE environment variable in your .bashrc, it will need to be declared above the line to implement this fix. So your entire .bashrc should look something like this:

```
# .bashrc
export DUO_PASSCODE=push
[[ $- != *i* ]] && return

# Source global definitions
if [ -f /etc/bashrc ]; then
       . /etc/bashrc
fi

# User specific aliases and functions
module load slurm
```

More information about the DUO_PASSCODE environment variable can be found on our [Logging In FAQ page](logging-into-ookami.md).

You may occasionally notice similar looking errors when loading or unloading modules. For example, a common one looks like this:

```
WARNING: $PATH does not agree with $PATH_modshare counter.
The following directories' usage counters were adjusted to match.
Note that this may mean that module unloading may not work correctly.
/cm/local/apps/environment-modules/4.0.0//bin
```

These kinds of errors could be due to small incompatibilities in the modulefile system or minor typos in our modulefiles. 99% of the time this warning is benign and can be ignored.

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/warning_modshare_library_path_duo.php`, retrieved November 5, 2026.
{: .archive-credit }
