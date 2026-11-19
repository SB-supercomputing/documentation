# Mathematica (Open OnDemand)

Mathematica combines symbolic mathematics, numerical computation, and interactive notebooks. Open its desktop interface through your browser and use SeaWulf resources for your calculations.

**On this page:** [Where it runs](#where) · [Start a session](#start) · [Launch settings](#settings) · [Troubleshooting](#trouble)

## Where it runs {#where}

| Cluster | Runs on |
| --- | --- |
| SeaWulf | Shared CPU queues on 40-core or 96-core nodes |

## Start a session {#start}

1. Sign in to the OnDemand portal for your cluster ([SeaWulf](https://sn-ood.seawulf.stonybrook.edu/)) with your NetID and Duo.
2. Open Interactive Apps and choose Mathematica.
3. Choose the launch settings below and click Launch.
4. After the session starts, Open OnDemand provides Compression and Image Quality controls for the remote desktop display (see the figure below). Compression controls how strongly the graphical display is compressed before being sent to the browser. Higher compression can improve responsiveness on slower network connections but may reduce visual quality. Image Quality controls the quality of the displayed image. Higher values provide a sharper display but may require more network bandwidth. For most sessions, the default settings are appropriate. Adjust them only if the desktop appears slow, blurry, or unresponsive.
5. Open or create a Mathematica notebook, and save it in your project folder before starting a long calculation.
6. Save your work or export the results, then click Delete on the session card when finished. Closing the browser tab does not stop the session.

![A running Mathematica session in Open OnDemand, with the Compression and Image Quality controls and the Launch Mathematica button](../assets/rci/seawulf-ondemand-mathematica/ood-mathematica-1.webp)

*A running Mathematica session in Open OnDemand, with the Compression and Image Quality controls and the Launch Mathematica button.*

## Launch settings {#settings}

Defaults below are starting points. Ask for resources your task needs, and keep the requested hours within the selected queue limit.

| Setting | What to choose |
| --- | --- |
| Mathematica version | Version 13.1.0. |
| Queue | Shared CPU queues on 40-core or 96-core nodes. Short up to 4 hours; long up to 24; extended up to 84. Start with `short-40core-shared` or `short-96core-shared`. |
| Working directory | Defaults to your home folder. Choose the folder containing your project or data. Enter a full path. |
| Hours | Default 1 hour. Choose enough time for your work, within the selected queue limit. |
| Cores | Default 1; form range 1 to 96. Use only as many cores as the task can use, within the selected node capacity. |
| Memory (GB) | Default 4 GB. Choices: 2, 4, 8, 16, 32, 64, 128, 164 GB. |

Email notifications are optional. Enter an email address and select Email when job starts if you want a start notification.

Choose an explicit memory size for routine work. All available can reserve node memory and increase waiting time; use it only when your task needs it.

## Troubleshooting {#trouble}

**A calculation uses too much memory.** Save what you can, then relaunch with more memory or reduce the size of the calculation.

**A license error appears.** Copy the exact error and contact HPC support. Include the app name and session job ID.

**The desktop opens but Mathematica does not.** Inspect the session output for module or startup errors and send it to support.

**My session stays Queued.** Try a shorter request, less memory, or fewer cores. Check the session output if the job fails instead of remaining queued.

If the problem continues, [contact HPC support](https://iacs.supportsystem.com) with the cluster, app name, job ID, and the error text.

## Related guides {#related}

- [Open OnDemand apps on SeaWulf](seawulf-ondemand-apps.md)
- [OnDemand overview](../shared/ondemand-overview.md)
- [Open OnDemand](https://rci.stonybrook.edu/hpc/ondemand)

**Applies to** <span class="rci-chip">SeaWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/ondemand-mathematica> (maintained by Research Computing and Informatics).
{: .rci-credit }
