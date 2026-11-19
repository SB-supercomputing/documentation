# genome_assembly

Software tools for assembling genomes from short sequencing reads.

The genome_assembly module provides various software and tools for genome assembly, facilitating the reconstruction of complete genomes from sequencing data.

**Module name** `genome_assembly`

## Loading genome_assembly

- module `genome_assembly/1.0`

!!! tip ""
    **Tip:** load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `Abyss`
- `BUSCO`
- `Canu`
- `Falcon`
- `Flye`
- `Hifiasm`
- `Medaka`
- `Miniasm`
- `QUAST`
- `Racon`

## Example usage

**Load genome_assembly**

```
module load genome_assembly/1.0
```

## Availability

genome_assembly is available on: SeaWulf, ClinWulf.

**Applies to** <span class="rci-chip">SeaWulf</span> <span class="rci-chip">ClinWulf</span>

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/genomeassembly> (maintained by Research Computing and Informatics).
{: .rci-credit }
