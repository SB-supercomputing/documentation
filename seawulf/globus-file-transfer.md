# Globus file transfer

Globus moves large research datasets reliably: it runs the transfer for you, retries on errors, and checks that files arrived intact. On SeaWulf you create a temporary personal Globus endpoint from the command line, then transfer between it and any other Globus endpoint.

**On this page:** [When to use Globus](#when) · [One-time setup](#setup) · [Start, transfer, stop](#transfer) · [Command reference](#ref) · [Troubleshooting](#trouble)

!!! note ""
    **Run Globus from the milan login nodes** (`milan.seawulf.stonybrook.edu`).

## When to use Globus {#when}

- Hundreds of gigabytes or more, or very many files.
- Transfers between SeaWulf and another institution or data center that has a Globus endpoint.
- Anything you'd rather not babysit: Globus keeps going if your laptop sleeps.

For everyday copies, `scp` and `rsync` are simpler. See [File transfer from the CLI](../shared/file-transfer-cli.md).

## One-time setup {#setup}

1. **Load Globus.**

    ```
    module load globus/3.15.0
    ```

2. **Log in to Globus.**

    ```
    globus login
    ```

    Open the link it prints, choose **Stony Brook University**, sign in with your NetID, and paste the authorization code back into the terminal.

3. **Create your SeaWulf endpoint.**

    ```
    globus endpoint create --default-directory /gpfs/scratch/$USER/ --personal seawulf
    ```

    Write down the **Endpoint ID** and **Setup Key** it prints.

4. **Finish setup** with the Setup Key:

    ```
    globusconnectpersonal -setup <setup-key>
    ```

## Start, transfer, stop {#transfer}

1. **Save the endpoint IDs** in variables so commands are shorter. `ep1` is your SeaWulf endpoint; `ep2` is wherever the data is going (find it on [app.globus.org](https://app.globus.org) or with `globus endpoint search "<name>"`):

    ```
    ep1=<your-seawulf-endpoint-id>
    ep2=<destination-endpoint-id>
    ```

2. **Start your endpoint** in the background, limited to your own folders:

    ```
    globusconnectpersonal -start -restrict-paths rw/gpfs/scratch/$USER,rw/gpfs/home/$USER &
    ```

3. **Check it can see your files:**

    ```
    globus ls $ep1
    ```

4. **Transfer a folder:**

    ```
    globus transfer $ep1:/gpfs/scratch/$USER/myfolder $ep2:~/myfolder --recursive --label "SeaWulf results"
    ```

    Globus prints a task ID. You can close your terminal; the transfer carries on, and you can watch it on [app.globus.org](https://app.globus.org/activity).

5. **Stop your endpoint** when the transfer is done:

    ```
    globusconnectpersonal -status
    globusconnectpersonal -stop
    ```

## Command reference {#ref}

| To… | Run |
| --- | --- |
| Load Globus tools | `module load globus/3.15.0` |
| Log in | `globus login` |
| Create your endpoint (once) | `globus endpoint create --default-directory /gpfs/scratch/$USER/ --personal seawulf` |
| Finish setup (once) | `globusconnectpersonal -setup <setup-key>` |
| Start the endpoint | `globusconnectpersonal -start -restrict-paths rw/gpfs/scratch/$USER,rw/gpfs/home/$USER &` |
| List files | `globus ls $ep1` |
| Transfer a folder | `globus transfer $ep1:/path $ep2:/path --recursive` |
| Check the endpoint | `globusconnectpersonal -status` |
| Stop the endpoint | `globusconnectpersonal -stop` |

## Troubleshooting {#trouble}

<details markdown="1">
<summary>"globus: command not found"</summary>

Load the module with `module load globus/3.15.0`, and make sure you're on a milan login node.

</details>

<details markdown="1">
<summary>The transfer can't read or write a folder</summary>

Your endpoint only sees the folders you listed in `-restrict-paths`. Stop it and start it again with the extra path, for example `rw/gpfs/projects/<group>`.

</details>

<details markdown="1">
<summary>The transfer is stuck at "waiting"</summary>

Your SeaWulf endpoint has probably stopped, for example because you logged out. Start it again with `globusconnectpersonal -start …`; Globus resumes the transfer.

</details>

Need help planning a big data move? [Open a ticket](https://iacs.supportsystem.com/) with HPC support.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/globus-file-transfer> (maintained by Research Computing and Informatics).
{: .rci-credit }
