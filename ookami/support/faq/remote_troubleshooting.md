# Remote Assistance Procedure

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

**Please note:** the following steps should only be followed after submitting a ticket and being requested to grant remote access by the HPC support team.

For hard-to-solve problems on the Ookami cluster, you can grant the HPC Support team remote access to troubleshoot the issue. This will give us access to a session with your login, allowing us to access your files, and test the issue with your specific environment. You will need the ticket number from an open [support ticket.](https://iacs.supportsystem.com/) Please be sure to mention in the ticket that you have requested a remote support session.

On Ookami, run the following commands:

```
module load shared
module load remote-assistance
request-support -t TICKET_NUMBER 
```

This will create a temporary session which the HPC Support team can use to troubleshoot your issue from your account.

You can cancel this session at any time with

```
request-support --cancel
```

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/remote_troubleshooting.php`, retrieved November 5, 2026.
{: .archive-credit }
