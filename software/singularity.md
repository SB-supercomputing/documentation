# Singularity

An open-source container platform for executing applications in isolated environments.

Singularity is a containerization platform that allows users to run applications in isolated environments, ensuring reproducibility across different computing systems. By encapsulating your entire environment in a container, you can ensure that your research code runs the same way on different systems. Note: the singularity build command with definition files is not supported on SeaWulf due to privilege requirements. Docker and Apptainer: Docker itself can't run on the clusters because it needs administrator (root) rights, but Singularity runs Docker images without them. Apptainer is the newer name for the same project, and the commands work the same way. Pull a Docker image with singularity pull docker://python:3.11 , then run it with singularity exec . For GPU jobs, add --nv .

**Module name:** `singularity`

## Loading Singularity

Load the default module, or run `module avail singularity` to list every installed version on your cluster:

> [!NOTE]
> `module load singularity`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Pull container images from Docker Hub**

```
singularity pull docker://ubuntu:20.04
singularity pull docker://python:3.9
singularity pull docker://tensorflow/tensorflow:latest-gpu
```

**Pull a container image from the Singularity Library**

```
singularity pull library://alpine:latest
```

**Build a container locally (not supported on SeaWulf)**

```
sudo singularity build my_container.sif my_definition.def
```

**Transfer a container to SeaWulf**

```
scp my_container.sif username@seawulf.stonybrook.edu:~/path/to/directory/
```

**Run or execute commands in a container**

```
singularity run my_container.sif
singularity exec my_container.sif my_custom_command
singularity exec my_container.sif python3 my_script.py
```

## Can I use Docker? {#docker}

Not directly. Docker needs administrator (root) rights, which aren't available on a shared cluster. Singularity runs Docker images without them. Apptainer is the newer name for the same project, and its commands work the same way.

1. Load it: `module load singularity`
2. Turn a Docker image into a Singularity image file (`.sif`):

    ```
    singularity pull docker://python:3.11
    ```
3. Run it in your job script:

    ```
    singularity exec python_3.11.sif python3 my_script.py
    ```
4. For GPU jobs, add `--nv` so the container can use the node's NVIDIA GPUs:

    ```
    singularity exec --nv my_image.sif python3 train.py
    ```

Images are large, so pull them into scratch or project space rather than your home folder. Images that need root to build can't be built on the clusters: build them on your own computer and copy the `.sif` file over.

## Availability

Singularity is available on: SeaWulf, NVwulf, ClinWulf.

**Category:** Development

**Applies to:** SeaWulf, NVwulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/singularity> (maintained by Research Computing and Informatics).
