# Start an OnDemand session

> **Status:** draft. Verified steps and screenshots to come.

Start a program on a compute node from your browser, check where it is running, and shut it down when you are done.
**Time:** 10 minutes, plus any wait in the queue · **Program:** the desktop app (<mark>Kitsune desktop app name</mark>)

> [!NOTE]
> Kitsune's OnDemand is planned but not confirmed yet. These steps use OnDemand as it works on any cluster; the specifics are checked and updated once ours is running.

| Before this | Data | You'll need |
|---|---|---|
| Nothing | None | An account on the cluster, and whatever second factor it asks for at sign-in: <mark>Kitsune account instructions, to come</mark> |

> [!NOTE]
> **Cluster details.** <mark>Highlighted</mark> values are placeholders. Kitsune's queue names, module versions, paths, and addresses go in when the cluster is deployed.

## Why this matters

The visualization lessons need a program running on a compute node, with a window you can use. [Open OnDemand](../../../reference/glossary.md#open-ondemand-ood) gives you both from a web browser. You request part of a node, and then ParaView or a Linux desktop opens in a browser tab. Your data stays on the cluster and you install nothing locally.

## Key idea

An OnDemand session is an ordinary Slurm job. Open OnDemand submits it for you, and the form is the job request: which [queue](../../../reference/glossary.md#queue-partition), how long, how many cores, how much memory. You keep the node until the time limit ends or you delete the session. Closing the browser tab only closes your view of it. The job carries on running and keeps using your allocation. → [Glossary: interactive session](../../../reference/glossary.md#interactive-session)

## Steps

### Step 1: Log in

Go to the cluster's OnDemand site, <mark>Kitsune OnDemand address</mark>, and sign in with <mark>Kitsune sign-in method</mark>.

**You should see:** the OnDemand dashboard, with a row of app icons (pinned apps) and a menu bar with **Files**, **Jobs**, **Clusters** and **Interactive Apps**.

<details>
<summary>Screenshot: the OnDemand dashboard</summary>

*Screenshot to come.*

</details>

### Step 2: Choose an app

Choose **Interactive Apps** and the desktop app (<mark>Kitsune desktop app name</mark>), or click its icon on the dashboard. The other interactive apps, including ParaView, use a similar form.

**You should see:** a form asking what the session needs.

<details>
<summary>Screenshot: the Interactive Apps menu</summary>

*Screenshot to come.*

</details>

### Step 3: Fill in the form

Each field is part of an ordinary [Slurm](../../../reference/glossary.md#slurm) job request. These values suit the visualization lessons in this set:

| Field | What it means | Slurm equivalent | Use for these lessons |
|---|---|---|---|
| **Queue** | Which group of nodes to run on, and its time limit | `--partition` | A queue for short work that shares nodes with other jobs: <mark>Kitsune queue name</mark> |
| **Number of hours** (or **Time Limit**) | How long the session may run | `--time` | `1`, the default. You can start another when it ends |
| **Number of cores** | How many cores the program gets | a core request | `4` |
| **Memory** | How much memory, written with a `G` | `--mem` | `16G` |
| **Desktop Environment** (Desktop only) | The look of the Linux desktop | none | <mark>Kitsune desktop environment</mark> |
| **Nodes** | How many nodes | `--nodes` | `1`. Leave it |
| **Account** | Which Slurm account to charge | `--account` | Leave blank unless your group told you otherwise |
| **Email Notification** | Email when the session starts | `--mail-type` | Optional, and useful when the queue is long |

> [!NOTE]
> Apps differ: not every one shows every field, and some name them differently. <mark>Kitsune's forms, to check</mark>.

**You should see:** your values in the form, and a **Launch** button at the bottom.

<details>
<summary>Screenshot: the filled-in form</summary>

*Screenshot to come.*

</details>

### Step 4: Launch and wait

Click **Launch**. The session card on **My Interactive Sessions** moves through **Queued**, then **Starting**, then **Running**.

**You should see:** a green **Running** card, after anything from seconds to a few minutes. It has a button that opens the desktop, and sliders for image quality.

<details>
<summary>Screenshot: the Running session card</summary>

*Screenshot to come.*

</details>

### Step 5: Connect

Click the card's launch button (<mark>Kitsune desktop app name</mark>). If it asks, sign in again.

**You should see:** a Linux desktop in a new browser tab. It's running on one of the cluster's compute nodes, not on your computer.

<details>
<summary>Screenshot: the desktop in the browser</summary>

*Screenshot to come.*

</details>

### Step 6: Check where you are

Open a terminal on the desktop: **Applications ▸ Terminal Emulator**.

**Run in:** the OnDemand desktop terminal

```bash
echo "Job $SLURM_JOB_ID on $(hostname) with $(nproc) cores"
```

**You should see:** a job number, a compute node's name and the number of cores you asked for, in this shape:

```text
Job 1234567 on <compute-node-name> with 4 cores
```

### Step 7: End the session

Close the desktop's browser tab. Then, on **My Interactive Sessions**, click **Delete** on the card and confirm.

**You should see:** the card disappears. The node goes back to the queue, and your allocation stops being charged.

<details>
<summary>Screenshot: the card's Delete button</summary>

*Screenshot to come.*

</details>

## Check your understanding

<details>
<summary>You close the browser tab of a running session and go to lunch. What happens, and what should you have done?</summary>

The session keeps running, and keeps using time, until its time limit ends. Closing the tab only closes your view of it. Delete the session on **My Interactive Sessions** when you're done.

</details>

<details>
<summary>Your session sits in "Queued" for twenty minutes. Name two changes to the form that would probably help.</summary>

Ask for less: fewer cores, less memory, or fewer hours make it easier to find room (see [backfill](../../../reference/glossary.md#backfill)). Or choose a queue that shares nodes, or one meant for short tests: <mark>Kitsune queue names and their limits</mark>.

</details>

## If something goes wrong

| What you see | Why | What to do |
|---|---|---|
| The card stays **Queued** for a long time | The queue is busy, or you asked for a lot | Delete it and relaunch with fewer cores, less memory, or fewer hours |
| The card jumps straight to **Completed** | The session failed to start | Click the **Session ID** link on the card and open `output.log`; the last lines say why |
| The desktop tab is blank or gray | The desktop is still starting | Wait 30 seconds, then reload the tab |
| Sign-in fails with "Disk quota exceeded" | Your home directory is full | Open a shell from the **Clusters** menu, check your usage (<mark>Kitsune quota command</mark>), and free some space |
| You can't find your data in the app | Apps start in your home directory | See [Get your data where the app can see it](your-data.md) |

## Next

- [Get your data where the app can see it](your-data.md): where to put your own files so an app can open them.
- [Start ParaView on OnDemand](../tools/paraview.md): opening a file, coloring it, saving a screenshot.
- [ParaView lessons](../maps/paraview.md): the full ParaView set.

