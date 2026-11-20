# Accessing RPX project space via CIFS

An RPX project space is shared storage for your research group that you can open like any other network folder on your own computer. Drag files in and out, open them in desktop apps, and share them with your group, all without SSH or SFTP. This page shows how to connect from Windows, macOS, and Linux, on campus or from home over the VPN.

!!! note ""
    **RPX is separate from SeaWulf.** RPX folders can't be seen from SeaWulf's login or compute nodes, and SeaWulf's own project directories (`/gpfs/projects`) can no longer be opened as a network drive. To move data between RPX and the cluster, copy it from your computer with [scp or rsync](../shared/file-transfer-cli.md), or use [Globus](globus-file-transfer.md) for large amounts.

**On this page:** [Before you start](#before) · [Windows](#windows) · [macOS](#macos) · [Linux](#linux) · [Off campus](#vpn) · [Good habits](#tips) · [Troubleshooting](#trouble)

## Before you start {#before}

You'll need four things:

1. **An RPX project space.** Your PI requests one through the IACS support system ("Request RPX CIFS Share (RPX ONLY)"), listing the storage needed, how long it's needed, and the NetIDs of everyone who should have access. See [Academic Research Storage](https://rci.stonybrook.edu/services/academic-research-storage) for details.
2. **The name of your project space**, for example `hpc_support`. If you're not sure of it, open the server as shown below and you'll see the project spaces you can access. The examples use `hpc_support`, so swap in your own.
3. **Your NetID and NetID password.**
4. **A connection to the Stony Brook network**, either on campus or through the [university VPN](https://it.stonybrook.edu/services/vpn).

| What you'll be asked for | What to enter |
| --- | --- |
| Server | `rpx-gtwy.seawulf.stonybrook.edu` |
| Share (folder) | Your project space name, e.g. `hpc_support` |
| Username | `sunysb.edu\<NetID>` (on Linux: domain `sunysb.edu`, username `<NetID>`) |
| Password | Your NetID password |

## Windows {#windows}

### Open it once

1. Make sure you're on the campus network or connected to the VPN.
2. Open **File Explorer**, click in the address bar, type `\\rpx-gtwy.seawulf.stonybrook.edu` and press **Enter**.
3. If Windows asks you to sign in, enter `sunysb.edu\<NetID>` and your NetID password.
4. Double-click your project space folder to open it.

### Keep it as a drive letter

1. In File Explorer, select **This PC**. On Windows 11, click **See more** (**…**) in the toolbar and choose **Map network drive**. On Windows 10, it's on the **Computer** tab.
2. Pick any free letter, such as **Z:**. Avoid **R:** if you also use the clinical R: drive.
3. For **Folder**, enter `\\rpx-gtwy.seawulf.stonybrook.edu\hpc_support` (with your own project name).
4. Tick **Reconnect at sign-in**. If your computer isn't signed in with your NetID, also tick **Connect using different credentials**.
5. Click **Finish** and sign in with `sunysb.edu\<NetID>` when asked.

Prefer a command? This does the same thing in Command Prompt or PowerShell:

```
net use Z: \\rpx-gtwy.seawulf.stonybrook.edu\hpc_support /user:sunysb.edu\<NetID> /persistent:yes
```

To remove the drive, right-click it under **This PC** and choose **Disconnect**, or run `net use Z: /delete`.

## macOS {#macos}

1. Make sure you're on the campus network or connected to the VPN.
2. In Finder, choose **Go → Connect to Server** (or press **⌘K**).
3. Enter `smb://rpx-gtwy.seawulf.stonybrook.edu/hpc_support` (with your own project name). Click **+** to save it as a favorite for next time, then click **Connect**.
4. Choose **Registered User**, enter `sunysb.edu\<NetID>` and your NetID password. Tick **Remember this password in my keychain** if this is your own computer.
5. Your project space opens in a new Finder window and appears under **Locations** in the sidebar.

**Connect automatically when you log in:** open **System Settings → General → Login Items & Extensions**, click **+** under "Open at Login", and choose the mounted project space. Select it and click **−** to stop.

**To disconnect,** click the eject button next to the project space in the Finder sidebar.

## Linux {#linux}

You'll need sudo rights on your computer, and the `cifs-utils` package (plus `smbclient` if you want to list shares). Package names can vary a little between distributions.

```
# Debian or Ubuntu
sudo apt install cifs-utils smbclient
# RHEL, Rocky, Alma or Fedora
sudo dnf install cifs-utils samba-client
```

1. Optional: list the project spaces you can reach.

    ```
    smbclient -L rpx-gtwy.seawulf.stonybrook.edu -W sunysb.edu -U <NetID>
    ```

2. Make a folder to mount it on, then mount it. You'll be asked for your computer password (for sudo) and then your NetID password.

    ```
    mkdir -p ~/hpc_support
    sudo mount -t cifs //rpx-gtwy.seawulf.stonybrook.edu/hpc_support ~/hpc_support \
      -o domain=sunysb.edu,username=<NetID>,uid=$(id -u),gid=$(id -g)
    ```

3. Your files are now in `~/hpc_support`.
4. When you're done, unmount it. If it says the target is busy, close anything using the folder, or add `-l`.

    ```
    sudo umount ~/hpc_support
    ```

<details markdown="1">
<summary>Mount it automatically at boot (optional)</summary>

Keep your NetID password out of `/etc/fstab` by saving it in a file only root can read. Create the file:

```
sudo nano /root/.rpx-credentials
```

Put these three lines in it, save, and lock it down:

```
username=<NetID>
password=<your NetID password>
domain=sunysb.edu
```

```
sudo chmod 600 /root/.rpx-credentials
```

Then add one line to `/etc/fstab` (change the path and IDs to match your own; `id -u` and `id -g` show them):

```
//rpx-gtwy.seawulf.stonybrook.edu/hpc_support  /home/<you>/hpc_support  cifs  credentials=/root/.rpx-credentials,uid=1000,gid=1000,_netdev,nofail  0  0
```

Run `sudo mount -a` to test it. `nofail` lets your computer start normally when you're off campus and the server can't be reached. Remember to update the file when your NetID password changes.

</details>

## From off campus (VPN) {#vpn}

1. Connect to the [Stony Brook University VPN](https://it.stonybrook.edu/services/vpn).
2. Follow the steps for your computer above. When asked to sign in, use `sunysb.edu\<NetID>` and your NetID password.

!!! note ""
    **Drive missing after a restart?** Saved drives and login items can't reconnect until the VPN is up. Connect to the VPN first, then open the drive (Windows) or reconnect from Finder's sidebar or Connect to Server (macOS).

## Good habits {#tips}

- **Use it for everyday work,** like opening, editing, and sharing documents, spreadsheets, and figures. For large datasets or many thousands of files, [Globus](globus-file-transfer.md) or [rsync](../shared/file-transfer-cli.md) is much faster and more reliable.
- **Keep your own backup.** Project space is not backed up, so keep another copy of anything you can't afford to lose.
- **Save and close files before you disconnect** or drop off the VPN. Unsaved changes can be lost if the connection goes away.
- **Don't point sync tools at it.** Apps like Box Drive, OneDrive, or Dropbox shouldn't sync this folder; they can create conflicts and heavy traffic.
- **Adding or removing people** is done by your PI through the IACS support system. Include each person's NetID.

## Troubleshooting {#trouble}

<details markdown="1">
<summary>"Windows can't access \\rpx-gtwy…" or "There was a problem connecting to the server"</summary>

Your computer can't reach the server. Check that you're on the campus network or that the VPN is connected, then try again. Double-check the spelling of the server name.

</details>

<details markdown="1">
<summary>My NetID password isn't accepted</summary>

Put the domain in front of your NetID: `sunysb.edu\<NetID>`. On Linux, keep `domain=sunysb.edu` in the mount options. If you changed your NetID password recently, update any saved password (Windows Credential Manager, macOS Keychain, or your Linux credentials file).

</details>

<details markdown="1">
<summary>I can reach the server but can't open my project folder</summary>

Your NetID probably hasn't been added to that project space yet. Ask your PI to request access for you through the IACS support system.

</details>

<details markdown="1">
<summary>Windows: "Multiple connections to a server or shared resource by the same user…"</summary>

Windows already has a connection to the server under a different username. Disconnect the old one, then connect again:

```
net use \\rpx-gtwy.seawulf.stonybrook.edu /delete
```

</details>

<details markdown="1">
<summary>Linux: "mount error(13): Permission denied"</summary>

Usually a typo in the NetID, password, or domain. Check that you used `domain=sunysb.edu` and that the share name matches your project space exactly.

</details>

<details markdown="1">
<summary>Linux: "mount error(95): Operation not supported" or "Host is down"</summary>

Your system may be trying an older SMB version. Add `vers=3.0` to the `-o` options and try again.

</details>

<details markdown="1">
<summary>I need these files on SeaWulf</summary>

RPX isn't mounted on SeaWulf. Copy the files from your computer to SeaWulf with [scp or rsync](../shared/file-transfer-cli.md), or use [Globus](globus-file-transfer.md). See [Storage layout & policies](storage-layout-policies.md) for where they belong on the cluster.

</details>

## Related

- [Academic Research Storage](https://rci.stonybrook.edu/services/academic-research-storage): what RPX is and how to request it
- [Research Storage picker](https://rci.stonybrook.edu/storage): not sure RPX is the right place for your data?
- [CIFS & SSHFS access](cifs-sshfs-access.md): mounting options across the clusters
- [Globus file transfer](globus-file-transfer.md) and [File transfer from the CLI](../shared/file-transfer-cli.md)

Still stuck? [Open a ticket with IACS support](https://iacs.supportsystem.com) and include your operating system, whether you're on campus or on the VPN, and the exact error message.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/accessing-project-space-cifs> (maintained by Research Computing and Informatics).
{: .rci-credit }
