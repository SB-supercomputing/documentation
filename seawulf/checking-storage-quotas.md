# Checking storage quotas

## The myquota command

`myquota` displays storage space and file usage in your directories. The clusters enforce limits on both storage size *and* file count: this command helps identify issues behind quota or disk errors.

## Basic usage

```
[NetID@milan1 ~]$ myquota
== NetID-home ==
Filesystem     GB      quota      limit |       files      quota      limit
mmfs1           6         20         20 |       61172     204800     204800

== NetID-scratch ==
Filesystem     GB      quota      limit |       files      quota      limit
mmfs1           1      20480      20480 |         204   10000000   10000000

== DoeGroup ==
Filesystem     GB      quota      limit |       files      quota      limit
mmfs1        3957       5120       5120 |     2038373   10485760   10485760
```

In this example the home directory uses 6 GB of 20 GB and 61,172 of 204,800 permitted files.

## Checking a specific directory

```
myquota <netid>-home      # your home directory
myquota <netid>-scratch   # your scratch directory
myquota ProjectName       # a shared project space
```

## Reading the output

- **GB / quota / limit**: storage consumed and maximum permitted
- **files / quota / limit**: file count and maximum allowed

Most directories have identical soft and hard limits, functioning as a single boundary.

## When to run it

- On "disk quota exceeded" or "no space left on device" errors
- Before transferring or creating large datasets
- When resolving shared project-space concerns with collaborators

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/checking-storage-quotas> (maintained by Research Computing and Informatics).
