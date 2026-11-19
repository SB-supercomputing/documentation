# CIFS & SSHFS access

## Overview

There are two ways to work with cluster files from your own computer as if they were local. CIFS (Common Internet File System) mounts storage as a network drive, which today means an RPX project space. [SSHFS](#sshfs) mounts any SeaWulf folder you can reach over SSH.

## General project space (/gpfs/projects)

> [!NOTE]
> **Service notice:** Mounting SeaWulf project directories via CIFS is currently **disabled**. If you need local-machine access to shared storage, use the RPX option below instead.

## RPX project space

Does your group need a shared folder that works as a network drive on Windows, Mac or Linux? Ask for an **RPX Project Space** with a support ticket.

> [!NOTE]
> **Key constraint:** RPX directories are **not** accessible from SeaWulf itself: RPX is for storage, local mounting, and external sharing only.

## SSHFS: mount your cluster folders on your computer {#sshfs}

SSHFS shows a SeaWulf folder on your own computer, like a local folder. It works for your home, scratch or project folder. You can then open and edit the files with your usual apps. It works anywhere you can log in with SSH, and it doesn't depend on the CIFS service.

> [!NOTE]
> **Good for editing, not for big transfers.** Every file you open travels over the network. To move a lot of data, use [rsync or scp](../shared/file-transfer-cli.md) or [Globus](globus-file-transfer.md).

### macOS and Linux

1. Install SSHFS. On Linux, use your package manager:

    ```
    sudo apt install sshfs       # Debian or Ubuntu
    sudo dnf install fuse-sshfs  # RHEL, Rocky, Alma or Fedora
    ```

    On a Mac, install macFUSE and SSHFS. Both are at [macfuse.github.io](https://macfuse.github.io/).

2. Make an empty folder to mount into:

    ```
    mkdir ~/seawulf
    ```

3. Mount your home directory. To mount scratch or a project instead, put `/gpfs/scratch/<netid>` or `/gpfs/projects/<group>` after the colon.

    ```
    sshfs -o reconnect,auto_cache <netid>@milan.seawulf.stonybrook.edu:/gpfs/home/<netid> ~/seawulf
    ```

    Enter your NetID password and approve the Duo prompt. Your files now show up in `~/seawulf`.

4. Unmount when you're done:

    ```
    fusermount -u ~/seawulf  # Linux
    umount ~/seawulf         # macOS
    ```

If you see "Transport endpoint is not connected", unmount the folder and mount it again.

### Windows

1. Install [WinFsp](https://winfsp.dev/).
2. Install SSHFS-Win. Open PowerShell and run:

    ```
    winget install SSHFS-Win.SSHFS-Win
    ```

3. Install [SSHFS-Win Manager](https://github.com/evsar3/sshfs-win-manager) and open it.
4. Click **Add Connection**. Enter `milan.seawulf.stonybrook.edu` as the host, your NetID as the username, and a free drive letter. Leave **Remote Path** blank for your home directory, or enter `/gpfs/scratch/<netid>` or `/gpfs/projects/<group>`. Choose **Password** for authentication.
5. Click **Connect** and approve the Duo prompt. The folder appears as a drive in File Explorer. To unmount, select the connection and click **Disconnect**.

## When to use what

- RPX and SSHFS are best for small edits and moving a few files.
- For large data, use `scp`, `rsync` (see [CLI transfer](../shared/file-transfer-cli.md)) or [Globus](globus-file-transfer.md). They are much faster.

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/cifs-sshfs-access> (maintained by Research Computing and Informatics).
