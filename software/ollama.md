# Ollama

An AI tool for building and deploying natural language processing models.

Ollama is a tool that facilitates the interaction with LLMs (Large Language Models) across different environments and hardware. It provides configurations for both AMD and NVIDIA systems, enabling accessible AI applications for natural language processing. SeaWulf offers multiple Ollama versions across different hardware environments for flexibility in various use cases.

**Module name:** `ollama`

## Loading Ollama

- module: `ollama/0.1.44-amd`
- module: `ollama/0.1.44-nvidia`
- module: `ollama/0.3.10-amd`
- module: `ollama/0.5.7-amd`
- module: `ollama/0.5.4`
- module: `ollama-py/0.3.3`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Example usage

**Load an Ollama module**

```
module load ollama/0.5.7-amd
```

## Availability

Ollama is available on: SeaWulf, NVwulf.

**Category:** Machine learning & AI

**Applies to:** SeaWulf, NVwulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/ollama> (maintained by Research Computing and Informatics).
