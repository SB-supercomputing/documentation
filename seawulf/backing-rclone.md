# Backing up with rclone

## Why back up

Scratch files are deleted after 45 days. Project spaces are not backed up. So back up anything important on a regular schedule. We recommend Stony Brook Box: storage is unlimited, it can hold sensitive data, and you can reach it from any device.

## Setup

1. **Load the module.**

    ```
    module load rclone/1.74.4
    ```

2. **Configure a Box remote.**

    ```
    rclone config
    ```

    Pick Box from the list. Leave the ID and secret fields blank. Choose *No* for auto config, because SeaWulf has no web browser.

3. **Authorize from your own computer.** Install rclone locally, run `rclone authorize "box"`, sign in, and paste the generated token back into the SeaWulf config prompt.

Google Drive works the same way: pick Drive in `rclone config` and authorize with `rclone authorize "drive"`.

## Transfer commands

```
rclone copy ./myfile.txt my_box:seawulf_backup          # single file
rclone copy ./mydir/ my_box:seawulf_backup/mydir        # directory
rclone sync ./mydir/ my_box:seawulf_backup/mydir        # mirror (deletes extras!)
```

## Performance

- Single files usually move at 350 to 450 Mbps.
- Folders with many small files are slow, so pack them into one archive first: `tar -zcvf mydir.tar.gz ./mydir`
- If Box slows your transfers down, add a rate limit, for example `--tpslimit`.

!!! note ""
    **Related:** Migrating a whole Google Drive into BOX? The step-by-step [Google Drive → BOX rclone guide](https://rci.stonybrook.edu/box/migrate-gdrive-rclone) covers the full cloud-to-cloud workflow.

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/backing-rclone> (maintained by Research Computing and Informatics).
{: .rci-credit }
