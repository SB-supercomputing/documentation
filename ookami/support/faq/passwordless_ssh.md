# Setting Up Passwordless SSH

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

RSA keys allow users to SSH into a system without having to enter a password. Instead, a locally stored key file is authenticated using the RSA cryptosystem (read more [here](https://en.wikipedia.org/wiki/RSA_(cryptosystem))). This practically allows users to write automated scripts utilizing SSH login without having to compromise password security.

## For MacOS and Linux

If you want to set up passwordless SSH from a Mac/Linux machine into either Ookami, you must first generate a public/private key pair from the terminal **on your local machine**. This would be:

```
ssh-keygen -t rsa -b 4096 -C "<your_netid>@login.ookami.stonybrook.edu"
```

The keygen program will prompt you to name the file. Give it whatever name you'd like:

```
Enter file in which to save the key (/home/<your_username>/.ssh/id_rsa): <filename>
```

The absolute path in the parentheses is the default location where the file will be saved if no filename is provided. If you provide a plain filename without an absolute path, it will save the key pair in the directory where you are running the keygen program, or whatever relative path you provide. We recommend putting your key in the .ssh folder in your home directory.

You will be prompted to create a passphrase for the key:

```
Enter passphrase (empty for no passphrase): <passphrase>
Enter same passphrase again: <same passphrase>
```

You will only need to enter this passphrase once, but it is still advisable to remember it or write it down somewhere.

Finally, add your key to your machine's list of keys:

```
ssh-add <private key>
```

You will then enter the passphrase that you created earlier. Your private key is the file without the .pub extension added to the end.

Your public key is the one with the .pub extension at the end. The next step is to upload this key to the login node:

```
ssh-copy-id -i <mykey> <your_netid>@login.ookami.stonybrook.edu
```

This will place the public key in the authorized_keys file in your .ssh directory. If the ssh-copy-id command is not available on your system, you can use the following command to upload your public key to Ookami:

```
cat ~/.ssh/id_rsa.pub | ssh <netid>@login.ookami.stonybrook.edu
     'cat >> .ssh/authorized_keys && echo "Key copied"'
```

It is best to limit permissions on your Ookami authorized_keys file. We recommend doing the following:

```
chmod 600 .ssh/authorized_keys
```

You should now be able to ssh into Ookami without entering a password.

## For Windows Users

### MobaXTerm

- Download [MobaXterm Home Edition](http://download.mobatek.net/1092018073012523/MobaXterm_Installer_v10.9.zip).
- Open up a local terminal by clicking "Start local terminal"
- Then Run the command below:

```
ssh-keygen -t rsa
```

- A prompt will come up, proceed to hit enter (unless you want to add a passphrase to your private key on the second prompt)
- The output should look similar:

```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/mobaxterm/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/mobaxterm/.ssh/id_rsa.
Your public key has been saved in /home/mobaxterm/.ssh/id_rsa.pub.
The key fingerprint is:
<YOUR FINGERPRINT> hpc@login.ookami.stonybrook.edu
The key's randomart image is:
<YOUR RANDOM ART IMAGE>
```

- To export this key to the Ookami server, use this command below (replace &lt;your_netid> with your NetID):

```
cat ~/.ssh/id_rsa.pub | ssh <your_netid>@login.ookami.stonybrook.edu
     "cat - >> ~/.ssh/authorized_keys
```

- Logout and close all active shells
- Open a new MobaXterm Window and click on Session on the top left corner of the screen
    - Select "SSH"
    - Input the remote host (login.ookami.stonybrook.edu), check the "Specify username" checkbox and input username (NetID) in the input field
- Click on "Advanced SSH Settings" and check the "Use private key" checkbox and the path should default to your saved key directory
- Select "OK" and your session should have automatically authenticated using RSA keys leaving you in your Ookami home directory.

Note: If you click to connect to a recent session of Ookami on MobaXterm, and that session wasn't configured to use your private key, it will ask for your password. Make sure you click on the most recent session for passwordless ssh or Start a new session, checking the "using your private key" box in order for passwordless SSH to work properly.

### PUTTYgen and PUTTY

1. Download [PUTTYgen](https://the.earth.li/~sgtatham/putty/latest/x86/puttygen.exe).
2. Open the PUTTYgen application.
    - Select SSH-2 RSA and 2048 bits and click the "Generate" button.
    - Move your mouse randomly in the blank area until the key generator has finished.
    - If you would like to use an additional passphrase enter and confirm this on the following window.
    - Save the public key and private key to a known location on your local machine.
    - Copy the text from the public key to your clipboard.
3. SSH into your account using PUTTY as normal (see [logging in](logging-into-ookami.md)).
4. From your home directory change to the .ssh directory and use your favorite editor to open the authorized_keys file and paste the key you copied into a new line
5. Logout and close all active shells
6. Open a new PUTTY session
    - enter in the information required to login as normal
    - In Connection/SSH/Auth click the "Browse" button and select the path to the private key that you saved earlier.
    - Save this configuration in the Session tab and click the "Open" button
7. Your session should have automatically authenticated using RSA keys leaving you in your Ookami home directory.

[SUBMIT A TICKET](https://iacs.stonybrook.edu)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/passwordless_ssh.php`, retrieved November 5, 2026.
{: .archive-credit }
