# Start ParaView on OnDemand

> **Status:** draft. Verified steps and screenshots to come.

Open a dataset in ParaView on a compute node, color it by one of its variables, and save a picture.
**Time:** 10 minutes · **Program:** ParaView 6 (<mark>Kitsune ParaView module</mark>)

> [!NOTE]
> Kitsune's OnDemand is planned but not confirmed yet. These steps use OnDemand as it works on any cluster; the specifics are checked and updated once ours is running.

| Before this | Data | You'll need |
|---|---|---|
| [Start an OnDemand session](../start/ondemand-session.md) | `disk_out_ref.ex2`: air flowing around a heated, spinning disk. It comes with ParaView (BSD-3) | Nothing else |

> [!NOTE]
> **Cluster details.** <mark>Highlighted</mark> values are placeholders. Kitsune's queue names, module versions, paths, and addresses go in when the cluster is deployed.

## Why this matters

ParaView reads the formats simulation codes usually write: Exodus, VTK, NetCDF, OpenFOAM, CSV, and image stacks. It can handle datasets too big for a laptop's memory. Running it on the cluster means the data does not move: the compute node reads it and renders the image, and only the image is sent to your browser.

## Key idea

ParaView builds a picture as a chain of steps, the pipeline. A reader opens the file, filters transform what it produced, and the render view draws whatever is switched on. The **Pipeline Browser** on the left shows that chain, and changes take effect only when you click **Apply**. Each filter produces new output rather than editing its input, so the file on disk is unchanged and you can go back and edit an earlier step. → [Glossary: visualization pipeline](../../../reference/glossary.md#visualization-pipeline)

## Steps

### Step 1: Start ParaView

On the OnDemand dashboard, choose **Interactive Apps ▸ ParaView**. The form takes the values from [the start lesson](../start/ondemand-session.md): <mark>Kitsune queue name</mark>, 1 hour, 4 cores. Launch, then connect.

**You should see:** the ParaView window in your browser, with the Pipeline Browser on the left and an empty render view in the middle.

<details>
<summary>Screenshot: the Pipeline Browser and render view, marked</summary>

*Screenshot to come.*

</details>

> [!TIP]
> If your dashboard has no ParaView app, start the desktop app (<mark>Kitsune desktop app name</mark>) instead. Open **Applications ▸ Terminal Emulator**, load ParaView (<mark>Kitsune ParaView module</mark>), and run `paraview &`.

### Step 2: Open the example data

Choose **File ▸ Open…**, click **Examples** in the left-hand list, select `disk_out_ref.ex2` and click **OK**. In the **Properties** panel, make sure every variable is ticked, then click **Apply**.

**You should see:** a gray, roughly cylindrical shape in the render view, and `disk_out_ref.ex2` in the Pipeline Browser.

<details>
<summary>Screenshot: the Open File dialog, with Examples marked</summary>

*Screenshot to come.*

</details>

> [!NOTE]
> If the dialog has no **Examples** entry, download the same files into scratch with Step 3 of [Get your data where the app can see it](../start/your-data.md), then open `~/scratch/ParaViewTutorialData-20220629/disk_out_ref.ex2`.

### Step 3: Move around

In the render view:
- drag with the left mouse button to rotate;
- scroll, or drag with the right button, to zoom;
- drag with the middle button (or <kbd>Shift</kbd> + left) to move sideways.

The **Reset Camera** button on the camera toolbar brings the whole object back into view.

**You should see:** the shape turn and move as you drag.

<details>
<summary>Screenshot: the Reset Camera button</summary>

*Screenshot to come.*

</details>

### Step 4: Color by temperature

With `disk_out_ref.ex2` selected, open the coloring drop-down on the toolbar (it says **Solid Color**) and choose **Temp**. Then click **Rescale to Data Range** on the same toolbar.

**You should see:** the surface colored from cool to hot, with a color legend labeled `Temp`.

<details>
<summary>Screenshot: the coloring drop-down and the legend</summary>

*Screenshot to come.*

</details>

> [!NOTE]
> Some ParaView versions show the variable names in lower case (`temp`, `pres`, `v`). Pick whichever your list shows.

### Step 5: Use a color map that doesn't mislead

In the **Properties** panel, find **Coloring** and click **Choose Preset** (the icon beside **Edit**). Search for **Viridis**, choose it, click **Apply**, then **Close**.

**You should see:** colors running from dark purple (cool) to yellow (hot). Viridis stays in order in grayscale and for red-green color blindness. A rainbow [color map](../../../reference/glossary.md#color-map) does not.

<details>
<summary>What you should see</summary>

*Picture to come: the practice data colored by temperature with Viridis.*

</details>

<details>
<summary>Screenshot: the Choose Preset dialog</summary>

*Screenshot to come.*

</details>

### Step 6: Save a picture

Choose **File ▸ Save Screenshot…**. Set the file name to `~/scratch/paraview-first.png` and the size to 1600 by 1200, then click **OK**.

**You should see:** `paraview-first.png` in the **Files** app, in your `scratch` folder.

<details>
<summary>Screenshot: the Save Screenshot dialog</summary>

*Screenshot to come.*

</details>

### Step 7: Finish

Choose **File ▸ Exit** to close ParaView. Then **delete the session** on **My Interactive Sessions**, as in the start lesson.

**You should see:** the session card gone.

## Check your understanding

<details>
<summary>After choosing a new variable, the whole object is one flat color. What single click usually fixes it?</summary>

**Rescale to Data Range.** The color scale was still set for the previous variable's values, so every value in the new one fell at one end of it.

</details>

<details>
<summary>Where did ParaView actually run, and why does that matter for a 200 GB dataset?</summary>

On one of the cluster's compute nodes. The data is read on the node, and only the rendered image crosses the network, so the size of the file makes little difference to your connection.

</details>

## If something goes wrong

| What you see | Why | What to do |
|---|---|---|
| **Apply** stays highlighted and nothing appears | The change hasn't been applied | Click **Apply** |
| The render view stays black | ParaView draws with the node's processors and is still working | Give it a few seconds, or click inside the view |
| Rotating is slow and jerky | The picture is large, or the image quality is set high | Make the window smaller, or lower **Image Quality** on the session card |
| `Temp` isn't in the list | Not all variables were loaded | Select the reader, tick every variable in **Properties**, click **Apply** |

## The ParaView family

ParaView ships as several programs built on the same core. The lessons use:

| Tool | What it's for | Taught in |
|---|---|---|
| `paraview` | This window: interactive exploration | this lesson; the density and vector-field lessons |
| **View ▸ Python Shell**, **Tools ▸ Start Trace** | Turning clicks into Python | *From clicks to a script* |
| Python Calculator | Computing new fields, NumPy-style (`curl`, `gradient`, `mag`) | *Derived fields: vorticity* |
| Programmable Filter | Any Python inside the pipeline | *Derived fields* (going further) |
| [`pvbatch` and `pvpython`](../../../reference/glossary.md#the-paraview-family) | Running ParaView Python scripts with or without a window | *From clicks to a script*, *Batch rendering* |
| `pvserver` | The server side of client-server mode | module B5, "Where next" |

## Next

- [Draw streamlines in ParaView](../vectors/streamlines/paraview.md): follow the flow through this same dataset.
- [Orbitals and electron density in ParaView](../densities/orbitals-and-density/paraview.md): ParaView for chemistry data.
- [ParaView lessons](../maps/paraview.md): the rest of the ParaView set.


## Credits

Data: `disk_out_ref.ex2`, ParaView example data (Kitware/Sandia), BSD-3-Clause. ParaView is BSD-3-Clause.
