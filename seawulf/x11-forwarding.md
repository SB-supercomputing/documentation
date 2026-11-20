# X11 forwarding

## Overview

X11 forwarding lets you run GUI applications on SeaWulf while displaying them on your local computer: useful for visualization tools and interactive applications with graphical interfaces.

## Setting up an X server

### Windows (MobaXterm)

MobaXterm includes a built-in X server with SSH integration. Create an SSH session to `login.seawulf.stonybrook.edu`, enable X11-Forwarding in Advanced SSH Settings, then test with `glxgears`.

### macOS (XQuartz)

Install XQuartz (the standard X11 implementation for macOS; version 2.7.9+ users should enable indirect GLX), then connect with:

```
ssh -X <your_netid>@login.seawulf.stonybrook.edu
```

### Linux

Most distributions include X11 by default:

```
ssh -X <your_netid>@login.seawulf.stonybrook.edu
```

## X11 with SLURM jobs

For interactive jobs, request resources with `salloc`, then SSH into the allocated node with X11 forwarding enabled. For some GUI applications, particularly tools like RStudio, the SeaWulf Desktop app in [Open OnDemand](../shared/ondemand-overview.md) delivers better performance.

!!! note ""
    **Note:** X11 forwarding operates per SSH connection: switching nodes requires reconnecting with the `-X` flag.

## Troubleshooting

- Verify your local X server is running
- Confirm the display variable is set: `echo $DISPLAY`
- Test with `glxgears` or a GUI app like Matplotlib or MATLAB

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/x11-forwarding> (maintained by Research Computing and Informatics).
{: .rci-credit }
