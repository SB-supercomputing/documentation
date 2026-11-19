# Handling job output

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

### Bash Script Redirection

One simple method for handling the output of your job is redirecting the program output directly in your batch script (the .slurm file you use to submit your job). This can be done with the > symbol.

```
ping stonybrook.edu > output.txt
```

This will write output from the ping command to a file called output.txt in the current working directory. Using this method, the output is written in real time. This means that if you submitted a job script with the command above and waited for it to start running, you could see the output being appended to output.txt from the login node in real time using a command like [tail](https://linux.die.net/man/1/tail):

```
tail -f output.txt
```

### Types of output

There are actually two types of output a program will produce: standard output and standard error. Normally, all of the output from the ping command will be sent to standard output. But if the network is down, the domain name cannot be found, the server doesn't respond, etc. these errors will be sent to standard error. The > symbol will by default overwrite any existing data in output.txt with the standard output of the command to the left of the symbol. We can place a 1 or 2 in front of the > symbol to explicitly redirect standard output or standard error, respectively. We can also use two greater than symbols (>>) to append the output to a file rather than overwrite. For example, this following command will write standard output to a file called out.txt, clearing out any previously existing data in that file. Standard error will be appended to the end a file called err.txt, and previous data in the file will not be overwritten.

```
ping notadomain.stonybrook.edu 1> out.txt 2>> err.txt
```

Or you could redirect both standard output and standard error using an ampersand:

```
ping stonybrook.edu &> alloutput.txt
```

### Slurm Output Handling

By default, Slurm creates a file of the form slurm-&lt;job ID>.txt for both standard output and standard error combined. You can specify specific files to store standard output and standard error with the -e and -o option respectively. You can also choose to append your output to the end of the specified file or clear out previously existing data using the --open-mode=append|truncate option. The default is truncate. Below is an example of appending your output to a standard output and standard error file using Slurm. Just like with bash script redirection, your output will be written in real time.

```
#SBATCH -e stderr.txt
#SBATCH -o stdout.txt
#SBATCH --open-mode=append
```

[SUBMIT A TICKET](https://iacs.supportsystem.com/)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/handling-job-output.php`, retrieved November 5, 2026.
{: .archive-credit }
