# How to Fix Common Login Issues

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

## "Connection reset by peer"

Sometimes Ookami users receive the following error message when attempting to login:

```
ssh_exchange_identification: read: Connection reset by peer
```

This typically indicates that the IP address the user is attempting to log in from has been blocked due to too many unsuccessful login attempts.

To rectify this situation, users should [submit a ticket](https://iacs.supportsystem.com/) and ask to have their IP address unblocked. When submitting the ticket it is helpful if you provide your public IP address. There are many websites that will provide this info (e.g., [here](https://www.whatismyip.com/what-is-my-public-ip-address/)). Likewise, this info can be determined at the command line by typing "ipconfig" (Windows users), "ifconfig" (Mac users), "ifconfig" or "curl ifconfig.me" (Linux users).

The most common cause of unsuccessful logins is password mistyping. To make things easier, users may wish to bypass the need for password entry to log into to Ookami by creating an RSA key. For more info, please see this [FAQ item on how to set up an RSA key for passwordless SSH](https://it.stonybrook.edu/help/kb/passwordless-ssh).

## "Your account has been locked out"

Sometimes Ookami users receive the following error message when attempting to login:

```
Your account has been locked out due to excessive authentication failures.
Please contact your administrator.
```

This occurs when you have failed to respond to 10 consecutive DUO authentication requests. You'll receive an email that will ask you to confirm the lockout. Once you respond to this email, the Computer Accounts Office will manually unlock your account. This probably happened either because your phone isn't properly configured with DUO so you never received any DUO pushes, or because you are using software or running a script that triggered a flood of DUO pushes.

If you have an iOS device, you can run a quick test to confirm that your phone is properly configured to receive DUO pushes. Open the DUO app and press "Edit" in the top left corner. Tap on your Stony Brook University account. Then click "Get Started" to perform a DUO test notificaton. If you're not using an iOS device, try logging in to the DUO Self Service Portal and make sure everything is configured properly. The HPC Support team does not provide support for DUO configuration issues, so if you run into any issues please check [DoIT's DUO FAQ Page](https://it.stonybrook.edu/services/duo-security-two-step-login) or submit a ticket to the [DoIT Service Portal](https://it.stonybrook.edu/services/itsm).

If your DUO lockout was caused by the software you're using or a script you ran, you will have to either change your workflow so that you do not get spammed with DUO pushes, or use Stony Brook's VPN when accessing Ookami. Information about requesting access and connecting to Stony Brook's VPN can be found [here](https://it.stonybrook.edu/services/vpn). You will need to authenticate once with DUO in order to get connected to the VPN, and then all connections made to Ookami through the VPN will not require DUO. We also have some recommendations for how to transfer files to and from Ookami with minimal DUO pushes on our [File Transferring FAQ Page](https://it.stonybrook.edu/help/kb/transferring-files-to-and-from-seawulf).

Please submit a ticket to the HPC Support team if you are having trouble adapting your workflow to avoid excessive DUO pushes and the VPN solution does not work for you.

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/fixing_common_login_issues.php`, retrieved November 5, 2026.
{: .archive-credit }
