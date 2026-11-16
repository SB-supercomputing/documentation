# Get your data where the app can see it

> **Status:** draft. Verified steps and screenshots to come.

Link your scratch space into your home directory so the OnDemand apps can see it, then put a dataset there.
**Time:** 10 minutes · **Program:** the OnDemand Files app and a terminal

| Before this | Data | You'll need |
|---|---|---|
| Nothing | Your own files. Step 3 downloads a public dataset as an example | Your account on the cluster |

> [!NOTE]
> **Cluster details.** <mark>Highlighted</mark> values are placeholders. Kitsune's queue names, module versions, paths, and addresses go in when the cluster is deployed.

## Why this matters

OnDemand apps open in your home directory, which is small. Work usually belongs in scratch or project space, and an app can only browse there if a path leads to it from your home directory. A symlink solves that. Knowing which space to use also keeps your files from being deleted by the [purge](../../../reference/glossary.md#purge).

## Key idea

The cluster has three kinds of storage, and each one trades something away. Home is small but backed up; keep code and notes there. Scratch is large and fast, and nothing in it is backed up: files older than a set age are deleted automatically, which is the [purge](../../../reference/glossary.md#purge). Project space is shared with your group, and its size is set on request. Work in scratch, and copy anything you want to keep somewhere else before the purge takes it. → [Glossary: scratch](../../../reference/glossary.md#scratch)

## Steps

### Step 1: Know the three places

| Place | Path | Size | Backed up? | Use it for |
|---|---|---|---|---|
| Home | <mark>Kitsune home path</mark> | <mark>Kitsune home quota</mark> | Yes | Scripts, notes, small results you must not lose |
| Scratch | <mark>Kitsune scratch path</mark> | <mark>Kitsune scratch quota</mark> | No, and old files are deleted | Data you're working on right now |
| Project | <mark>Kitsune project path</mark> | Set per group | No | Data your group shares |

Working data goes in scratch.

### Step 2: Make scratch visible from home

Open a terminal: the shell on the dashboard's **Clusters** menu, or the terminal in a desktop session.

**Run on:** a login node, or the OnDemand desktop terminal. <mark>Put Kitsune's scratch path in place of /path/to/scratch.</mark>

```bash
ln -s /path/to/scratch/$USER ~/scratch
```

**You should see:** no output. In the **Files** app, your home directory now has a `scratch` folder that leads to your scratch space. An app that opens in your home directory can now reach scratch through it.

<details>
<summary>Screenshot: the Files app, with the scratch folder in your home</summary>

*Screenshot to come.*

</details>

### Step 3: Download a dataset

Compute nodes may not be able to reach the internet, but login nodes can. Run the download on a login node, into scratch. The example here is ParaView's tutorial data.

**Run on:** a login node

```bash
cd ~/scratch
curl -LO https://www.paraview.org/files/data/ParaViewTutorialData-20220629.tar.gz
tar -xzf ParaViewTutorialData-20220629.tar.gz
ls ParaViewTutorialData-20220629
```

**You should see:** a folder of example datasets, `disk_out_ref.ex2`, `can.ex2`, and `headsq.vti` among them. Your own data gets there the same way: by download or upload.

### Step 4: Upload a file of your own

In the **Files** app, open `scratch`, click **Upload** and choose a small file from your computer.

**You should see:** your file listed in `scratch`. For anything over a few gigabytes, use Globus instead of the browser (see module [B3](../../../modules/B3-data-transfer.md)).

<details>
<summary>Screenshot: the Files app's Upload button</summary>

*Screenshot to come.*

</details>

### Step 5: Check how much space you have

**Run on:** a login node. <mark>Put Kitsune's quota command in place of quota-command.</mark>

```bash
quota-command
quota-command $USER-scratch
```

**You should see:** your usage and limit for home, and then for scratch.

## Check your understanding

<details>
<summary>Your simulation writes 5 GB of results you'll visualize next week and want to keep for a paper. Where should they live?</summary>

Write them to scratch, which is fast and large, and visualize them from there. Then copy the results you need to keep to project space, or somewhere backed up, before the purge can delete them.

</details>

## If something goes wrong

| What you see | Why | What to do |
|---|---|---|
| `ln: failed to create symbolic link … File exists` | You already made the link | Nothing to do: open `~/scratch` |
| `curl: (6) Could not resolve host` | You're on a compute node without internet | Run the download on a login node instead |
| `Permission denied` in a project folder | Your group hasn't given you write access | Ask your group's owner (see module [B2](../../../modules/B2-data-management.md)) |

## Next

- [Start ParaView on OnDemand](../tools/paraview.md): the program most of these lessons use.
- [ParaView lessons](../maps/paraview.md): what else ParaView can do here.

## Credits

ParaView example data: Kitware, BSD-3-Clause.
