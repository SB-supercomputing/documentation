# Bowtie2

A fast, memory-efficient tool for aligning sequencing reads to long reference sequences.

Bowtie2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie2 supports gapped, local, and paired-end alignment modes and works with a variety of popular read formats including FASTQ, QSEQ, and FASTA.

**Module name:** `bowtie2`

## Loading Bowtie2

- module: `bowtie2 (default: 2.5.4)`

> [!TIP]
> Load modules inside your SLURM job script, not just on the login node, so compute nodes see the same environment. Verify with `which` after loading.

## Commands

- `-x` : Path to the index for the reference genome
- `-1` : File with mate 1 reads (paired-end)
- `-2` : File with mate 2 reads (paired-end)
- `-U` : File with unpaired reads (single-end)
- `-S` : Output SAM file (default: stdout)
- `-p/--threads` : Number of parallel search threads (default: 1)
- `--local`: Local alignment; ends might be soft clipped
- `--end-to-end`: End-to-end alignment (default)
- `-k` : Report up to  alignments per read

## Example usage

**Load Bowtie2**

```
module load bowtie2
```

**Load a specific version**

```
module load bowtie2/<version>
```

**Single-end alignment**

```
bowtie2 -p 8 -x /path/to/reference/genome -U sample.fastq -S output.sam
```

**SLURM job script (paired-end alignment)**

```
#!/bin/bash
#SBATCH --job-name=bowtie2_align
#SBATCH --output=bowtie2_align_%j.out
#SBATCH --error=bowtie2_align_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH -p short-40core
#SBATCH --ntasks=40

module load bowtie2

INDEX="/path/to/reference/genome"
READS1="/path/to/sample_1.fastq"
READS2="/path/to/sample_2.fastq"
OUTPUT="/path/to/output.sam"

bowtie2 -p $SLURM_CPUS_PER_TASK -x $INDEX -1 $READS1 -2 $READS2 -S $OUTPUT
```

## Availability

Bowtie2 is available on: SeaWulf, ClinWulf.

**Category:** Bioinformatics

**Applies to:** SeaWulf, ClinWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/hpc/software/bowtie2> (maintained by Research Computing and Informatics).
