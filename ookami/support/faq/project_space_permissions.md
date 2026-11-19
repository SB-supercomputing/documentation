# Setting Permissions in Project Spaces

!!! note archive "Archived page"
    Ookami reached end of life at the end of 2025. This is a copy of its website, kept for reference; some original material is not included.

All files in UNIX are owned by both a group and a user. There exist different sets of permissions for the group and user owner of every file. Each project folder on Ookami is associated with a group that all users in the research team belong to. If group members aren't careful, files they place there may not be accessible to other group members because the group owner or group permissions are not correct. You can use the command ls -l to check if files in your project folder have the right group owner and permissions. For example, if John Smith has access to a project folder called SmithGroup, he should see this:

```
[jsmith@login2 SmithGroup]$ ls -l
total 0
-rw-rw---- 1 jsmith SmithGroup 0 Sep 16 15:27 file.txt
```

The group owner is SmithGroup and characters 5 through 7 in the ouput are rw-, meaning members of SmithGroup have read and write permissions for the file. Here are two examples of incorrect permissions:

```
[jsmith@login2 SmithGroup]$ ls -l
total 0
-rw-rw---- 1 jsmith jsmith 0 Sep 16 15:27 file.txt

[jsmith@login2 SmithGroup]$ ls -l
total 0
-rw------- 1 jsmith SmithGroup 0 Sep 16 15:27 file.txt
```

In the first example, the group permissions are set correctly but the group owner is jsmith, so members of SmithGroup don't have read and write permissions. In the second example, the group owner is SmithGroup, but SmithGroup is not provided the proper read and write permissions.

When creating new files and directories in the root directory of your project space, they should default to the correct group owner and permissions. Problems can occcur when copying or moving files into your project space from other locations, depending on what method you use. We recommend using rsync with the proper flags whenever copying files into a project space.

## rsync command

By default, rsync will **not** use the correct permissions when copying files into your project space. However, it offers multiple flags that will allow you to set them properly. Instead of running this command to quickly copy a file into your project folder:

```
rsync -avz file.txt /gpfs/projects/SmithGroup
```

Use this command:

```
rsync -avz --no-g --no-p --chmod=ugo=rwX file.txt /gpfs/projects/SmithGroup
```

This will ensure that the group owner is SmithGroup and other members of SmithGroup have the correct read, write, and execute permissions on the file.

## scp and cp command

The scp and cp command will set the correct group owner, but not the right permissions. If you used one of these commands to copy your files into your project space, you should also run the following command to correct group permissions:

```
find <DIRECTORY> -user $USER -exec chmod g=u {} \;
```

This will update group permissions to reflect your own user permissions for all the files you own in the given &lt;DIRECTORY>.

## mv command

The mv command is the fastest way to get files into your project space since it's not actually copying the contents of the file, but instead just changing its location in the file system. However, it has **no support** for updating permissions. You must manually set correct permissions after the files have been moved to allow your group members access. This can be done like so:

```
find <DIRECTORY> -user $USER -exec chgrp <GROUPNAME> {} \; -exec chmod g=u {} \;
```

If you are copying any folders using the move command, you must also update the special [setgid bit](https://linuxconfig.org/how-to-use-special-permissions-the-setuid-setgid-and-sticky-bits) (see below for explanation).

## Subdirectories

Sometimes, even when using the rsync command with the flags we recommended above, you may find group ownership is still set incorrectly. This is probably because you are copying files into a subdirectory of your project space that does not have the special setgid bit enabled. It should be enabled by default when creating subdirectories in your project space, but the mv command, for example, will not enable the setgid bit if moving directories into your project space. The [setgid bit](https://linuxconfig.org/how-to-use-special-permissions-the-setuid-setgid-and-sticky-bits) of a directory controls the default group of files and subdirectories created within that directory. Earlier, we mentioned that permissions for newly created files will always be set correctly in the **root directory** of your project space because all project directories have the setgid bit enabled. You can confirm this with ls -l:

```
[jsmith@login2 SmithGroup]$ ls -la
total 0
drwxrws---+ 1 jsmith jsmith 0 Sep 16 15:27 .
```

Notice the 7th character of the output for the current directory (signified by ".") is the letter s. This is what causes all files and subdirectories created in the SmithGroup project folder to be owned by the SmithGroup by default (subdirectories also inherit the setgid bit by default). If you have a folder within your project space without an s as the 7th character of the permissions list, you can set the setgid bit like so:

```
chmod -R g+s <DIRECTORY>
```

You'll also probably need to update group ownership and permissions for everything in that directory like so:

```
find <DIRECTORY> -user $USER -exec chgrp <GROUPNAME> {} \; -exec chmod g=u {} \;
```

[SUBMIT A TICKET](https://iacs.supportsystem.com)

Archived from `https://www.stonybrook.edu/commcms/ookami/support/faq/project_space_permissions.php`, retrieved November 5, 2026.
{: .archive-credit }
