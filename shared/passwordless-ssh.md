# Passwordless SSH

An SSH key lets you log in without typing your NetID password each time. You make a pair of keys on your own computer: a private key that stays with you, and a public key you copy to the cluster. You may still be asked to approve Duo.

**On this page:** [macOS and Linux](#mac) · [Windows: MobaXterm](#moba) · [Windows: built-in terminal](#win) · [Windows: PuTTY](#putty) · [Other clusters](#other) · [Troubleshooting](#trouble)

> [!NOTE]
> **Keep your private key private.** Never copy it to the cluster or share it. Protect it with a passphrase; an SSH agent can remember the passphrase so you only type it once per session.

## macOS and Linux {#mac}

1. **Make a key pair** in Terminal. Press Enter to accept the default file name, then choose a passphrase:

    ```
    ssh-keygen -t ed25519 -C "<netid>@seawulf"
    ```

    If you need an RSA key for an older tool, use `ssh-keygen -t rsa -b 4096` instead.

2. **Add it to your SSH agent** so you don't retype the passphrase:

    ```
    ssh-add ~/.ssh/id_ed25519
    ```

3. **Copy the public key to SeaWulf** (you'll log in with your password and Duo this one time):

    ```
    ssh-copy-id -i ~/.ssh/id_ed25519.pub <netid>@milan.seawulf.stonybrook.edu
    ```

    No `ssh-copy-id` on your computer? Use this instead:

    ```
    cat ~/.ssh/id_ed25519.pub | ssh <netid>@milan.seawulf.stonybrook.edu 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
    ```

4. **Test it:**

    ```
    ssh <netid>@milan.seawulf.stonybrook.edu
    ```

    You should no longer be asked for your NetID password.

Your home folder is shared by all SeaWulf login nodes, so one copy of the key works for `milan`, `login`, and `xeonmax`.

## Windows: MobaXterm {#moba}

1. Install MobaXterm Home Edition and click **Start local terminal**.
2. Make a key pair:

    ```
    ssh-keygen -t ed25519
    ```

3. Copy the public key to SeaWulf:

    ```
    cat ~/.ssh/id_ed25519.pub | ssh <netid>@milan.seawulf.stonybrook.edu "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
    ```

4. Create a new SSH session to `milan.seawulf.stonybrook.edu`, tick **Specify username** and enter your NetID. Under **Advanced SSH settings**, tick **Use private key** and choose your key file. Click **OK**.

> [!NOTE]
> Older saved sessions that weren't set up with your private key will still ask for a password. Edit them to use the key.

## Windows: built-in terminal {#win}

Windows 10 and 11 include OpenSSH. In **PowerShell**:

```
ssh-keygen -t ed25519
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh <netid>@milan.seawulf.stonybrook.edu "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## Windows: PuTTY {#putty}

1. Open **PuTTYgen**, choose **EdDSA (Ed25519)** or **RSA 4096**, click **Generate**, and move the mouse to create randomness.
2. Set a passphrase and save both the public and private keys.
3. Copy the text in the "Public key for pasting" box and add it as a new line in `~/.ssh/authorized_keys` on SeaWulf.
4. In PuTTY, go to **Connection → SSH → Auth → Credentials**, browse to your private key, save the session, and connect.

## Other clusters {#other}

NVwulf has its own home folder, so copy your public key there too, using `login.nvwulf.stonybrook.edu` in place of the SeaWulf address.

## Troubleshooting {#trouble}

<details markdown="1">
<summary>It still asks for my password</summary>

The permissions on the cluster are probably too open. Log in and run:

```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Also check that the key you're offering is the one you copied, for example with `ssh -v`.

</details>

<details markdown="1">
<summary>"Permissions 0644 for '…id_ed25519' are too open"</summary>

That's your private key on your own computer. Fix it with `chmod 600 ~/.ssh/id_ed25519`.

</details>

<details markdown="1">
<summary>I lost my key or my computer</summary>

Log in with your password, edit `~/.ssh/authorized_keys` on the cluster to remove the old key's line, and make a new key pair.

</details>

More login help: [Connecting to the cluster](connecting-cluster.md) and [Duo authentication](duo-authentication.md).

**Applies to:** All clusters

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/passwordless-ssh> (maintained by Research Computing and Informatics).
