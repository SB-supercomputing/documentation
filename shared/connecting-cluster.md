# Connecting to the cluster

There are two ways onto RCI's clusters: **Open OnDemand** in your web browser, or **SSH** from a terminal. Both use your NetID, your NetID password, and a Duo approval. If you're new to HPC, start with Open OnDemand; you can move to SSH whenever you like.

**On this page:** [Addresses](#addresses) · [Before you connect](#before) · [Open OnDemand](#ondemand) · [SSH](#ssh) · [SeaWulf login nodes](#login-nodes) · [Log in faster](#faster) · [Troubleshooting](#trouble)

## Where to connect {#addresses}

| Cluster | SSH address | Open OnDemand (browser) |
| --- | --- | --- |
| [**SeaWulf**](../seawulf/README.md)<br>General-purpose computing | `milan.seawulf.stonybrook.edu`<br>or `xeonmax.seawulf.stonybrook.edu` for HBM (see [which one](#login-nodes)) | [sn-ood.seawulf.stonybrook.edu](https://sn-ood.seawulf.stonybrook.edu/) |
| [**NVwulf**](../nvwulf/README.md)<br>GPU computing for AI and ML | `login.nvwulf.stonybrook.edu` | [nvwulf-ood.nvwulf.stonybrook.edu](https://nvwulf-ood.nvwulf.stonybrook.edu/) |
| [**ClinWulf**](https://rci.stonybrook.edu/hpc/clusters/clinwulf)<br>HIPAA-compliant computing on PHI | `login02.uhmc.sbuh.stonybrook.edu` | [clinwulf-ood.uhmc.sbuh.stonybrook.edu](https://clinwulf-ood.uhmc.sbuh.stonybrook.edu/) |

> [!NOTE]
> **ClinWulf network access:** ClinWulf OnDemand can only be reached from within Health Sciences and Stony Brook University Hospital and Medical Center. From anywhere else, connect through Citrix Desktop or the Stony Brook Hospital & Medical Center VPN first.

Not sure which cluster fits your work? Try the [cluster picker](https://rci.stonybrook.edu/hpc/cluster-picker).

## Before you connect {#before}

1. **An account on the cluster.** See [Requesting accounts & project numbers](requesting-accounts-project-numbers.md) for SeaWulf and [Getting access to NVwulf](../nvwulf/getting-access-nvwulf.md) for NVwulf. ClinWulf is for IRB-approved studies in Health Sciences / Medicine working with PHI.
2. **Duo two-factor authentication.** Every login needs a Duo approval, so enroll a device first. See [Duo authentication](duo-authentication.md).
3. **Your NetID and NetID password.** Type your NetID in lowercase.

## Option 1: Open OnDemand in your browser {#ondemand}

Open OnDemand gives you files, a job composer, a shell, and apps like Jupyter, RStudio, MATLAB, and a full desktop, all in the browser. Nothing to install.

1. Open the OnDemand address for your cluster from the [table above](#addresses).
2. Sign in with your NetID and NetID password.
3. Approve the Duo request on your phone.
4. You're in. The [OnDemand overview](ondemand-overview.md) shows what everything does.

## Option 2: SSH from a terminal {#ssh}

### macOS and Linux

1. Open **Terminal**.
2. Connect to your cluster's SSH address, for example SeaWulf:

    ```
    ssh <netid>@milan.seawulf.stonybrook.edu
    ```

3. The first time, you'll be asked whether to trust the server's key. Type `yes`.
4. Enter your NetID password (nothing shows as you type), then approve the Duo push.

**Graphical programs:** add `-X`, as in `ssh -X <netid>@milan.seawulf.stonybrook.edu`. On a Mac, install [XQuartz](https://www.xquartz.org/) first. See [X11 forwarding](../seawulf/x11-forwarding.md).

### Windows

**MobaXterm (recommended).** The free Home Edition includes a terminal, a file browser, and a built-in X server, so graphical programs work without extra setup.

1. Install [MobaXterm Home Edition](https://mobaxterm.mobatek.net/download.html) and open it.
2. Click **Session**, then **SSH**.
3. For **Remote host**, enter your cluster's SSH address. Tick **Specify username** and enter your NetID.
4. Click **OK**, enter your NetID password, and approve the Duo push. The session is saved in the left panel for next time.

**Built-in Windows terminal.** Windows 10 and 11 include SSH. Open **Windows Terminal** or **PowerShell** and use the same command as macOS and Linux:

```
ssh <netid>@milan.seawulf.stonybrook.edu
```

PuTTY also works if you already use it.

> [!NOTE]
> **You land on a shared login node.** Login nodes are for editing, managing files, and submitting jobs. Run real work as a job or in an [interactive session](interactive-jobs.md). See [Login node etiquette](login-node-etiquette.md) and [Good conduct on the RCI clusters](hpc-good-conduct.md).

## Which SeaWulf login node? {#login-nodes}

SeaWulf has more than one set of login nodes, and each reaches different compute nodes. Pick the one that matches the queues you'll use. Your files are the same on all of them.

| Address | Login nodes | Reaches these compute nodes |
| --- | --- | --- |
| `milan.seawulf.stonybrook.edu` | milan1, milan2 | 40-core Skylake, 96-core AMD EPYC Milan, Sapphire Rapids. The best choice for most work. |
| `xeonmax.seawulf.stonybrook.edu` | xeonmax | Sapphire Rapids and high-bandwidth memory (HBM) nodes |

The [queue selection guide](../seawulf/queue-selection-guide.md) lists every queue and where to submit it from.

The older login1 and login2 nodes (`login.seawulf.stonybrook.edu`) were retired in November 2026, along with the 28-core Haswell nodes and the K80, P100 and V100 GPU nodes. If you built software there, rebuild it on a milan login node.

## Log in faster {#faster}

### Short names with an SSH config file

On macOS, Linux, or the Windows terminal, save your usual settings in `~/.ssh/config` (create the file if it doesn't exist):

```
Host seawulf
    HostName milan.seawulf.stonybrook.edu
    User <netid>
    ForwardX11 yes

Host nvwulf
    HostName login.nvwulf.stonybrook.edu
    User <netid>
```

Then connect with just `ssh seawulf` or `ssh nvwulf`. The same names work with `scp` and `rsync`.

### Fewer Duo prompts

- **Pick your Duo method ahead of time** with the `DUO_PASSCODE` setting, for example always send a push. This also helps file-transfer tools. See [Duo authentication](duo-authentication.md).
- **Use the Stony Brook VPN.** You approve Duo once when the VPN connects, and later logins through the VPN don't ask again.
- **Set up an SSH key** so you don't type your password each time. See [Passwordless SSH](passwordless-ssh.md).

## Troubleshooting {#trouble}

<details markdown="1">
<summary>"Connection reset by peer" or the connection closes right away</summary>

Your IP address has probably been blocked after too many failed logins, usually from a mistyped password. [Open a ticket](https://iacs.supportsystem.com) and ask for it to be unblocked, including your public IP address. You can find it by searching "what is my IP" or running:

```
curl ifconfig.me
```

Setting up [passwordless SSH](passwordless-ssh.md) avoids password typos in future.

</details>

<details markdown="1">
<summary>"Your account has been locked out due to excessive authentication failures"</summary>

This happens after 10 Duo requests in a row go unanswered. You'll get an email asking you to confirm the lockout; reply to it and the Computer Accounts Office will unlock your account. Then find the cause: either your phone isn't receiving Duo pushes (send a test from the Duo Mobile app, or check the Duo self-service portal), or a program or script is triggering many logins. For scripts and file-transfer tools, connect through the VPN so they don't each need Duo.

</details>

<details markdown="1">
<summary>The Duo push never arrives</summary>

Open Duo Mobile and check that your Stony Brook account is there and can receive a test push. As a fallback, choose a phone call or a passcode instead of a push, or set `DUO_PASSCODE` (see [Duo authentication](duo-authentication.md)). For Duo enrollment problems, contact DoIT through the [DoIT service portal](https://it.stonybrook.edu).

</details>

<details markdown="1">
<summary>My password isn't accepted, or I forgot it</summary>

The clusters use your NetID password, so type your NetID in lowercase and check Caps Lock. To reset it, change your NetID password through DoIT's [NetID service](https://it.stonybrook.edu/services/netid). The new password applies everywhere you use your NetID, including email and Wi-Fi.

</details>

<details markdown="1">
<summary>"Could not resolve hostname" or the connection times out</summary>

Check the spelling of the address against the [table above](#addresses). If it still can't connect, try again on the campus network or the VPN, and check the [system status page](https://rci.stonybrook.edu/status) for maintenance.

</details>

<details markdown="1">
<summary>Graphical programs won't open</summary>

Connect with `ssh -X`. On a Mac, install XQuartz and log out and back in. On Windows, use MobaXterm, which has an X server built in. For heavier graphical work, a desktop session in [Open OnDemand](seawulf-desktop.md) is usually smoother.

</details>

<details markdown="1">
<summary>My jobs can't find the queue I want</summary>

You're probably on a login node that doesn't reach that queue. Log in to the address listed for it in [Which SeaWulf login node?](#login-nodes), or check the [queue selection guide](../seawulf/queue-selection-guide.md).

</details>

## Still stuck?

[Open a ticket with HPC support](https://iacs.supportsystem.com) and include the cluster, the address you used, your operating system, and the exact error message. For problems specific to your account, support may ask you to start a remote-assistance session so they can look from your login. Only do this when support asks, using the ticket number they give you:

```
module load remote-assistance
request-support -t <ticket-number>
```

Cancel it at any time with `request-support --cancel`.

## Related

- [Get started with HPC](https://rci.stonybrook.edu/hpc/get-started): the whole path from account to first job
- [Quick Start Guide](../seawulf/quick-start-guide.md): your first SLURM job
- [File transfer from the CLI](file-transfer-cli.md) and [Globus file transfer](../seawulf/globus-file-transfer.md)
- [Getting started on NVwulf](../nvwulf/getting-started-nvwulf.md)

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/connecting-cluster> (maintained by Research Computing and Informatics).
