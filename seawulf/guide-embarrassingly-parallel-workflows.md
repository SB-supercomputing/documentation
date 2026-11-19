# Guide to embarrassingly parallel workflows

“Embarrassingly parallel” workflows are ones where each task runs independently: no communication between processes. This guide shows four ways to parallelize them on SeaWulf. For communication-dependent workloads, see the companion [guide to OpenMP and MPI](guide-using-openmp-and-mpi.md).

## The example task

A small Python script (`number_square.py`) that squares an integer: requires `module load anaconda/3`:

```
#!/usr/bin/env python
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Take in a number and print out its square")
parser.add_argument('integer', metavar='N', type=int,
                    help='an integer for the calculation')
args = parser.parse_args()
result = int(np.square(args.integer))
print(f'The square of {args.integer} is {result}')
```

Running `python number_square.py 8` prints `The square of 8 is 64`. The goal: compute this for many inputs at once.

## Approach 1: GNU Parallel

A command-line tool built exactly for this. Job script running 100 tasks, 40 at a time on one 40-core node:

```
#!/usr/bin/env bash
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=05:00
#SBATCH --partition=short-40core
#SBATCH --job-name=parallel_job
#SBATCH --output=squared_numbers.txt

module load anaconda/3
module load gnu-parallel/6.0

parallel --jobs 40 python number_square.py {} ::: {1..100}
```

- `--jobs 40`: run 40 processes simultaneously
- `{}`: placeholder for each input value
- `:::`: separates the command from its inputs; `{1..100}` is shell range syntax
- Add `--keep-order` if results must come out in input order

## Approach 2: Python multiprocessing

Parallelize inside Python itself with a worker pool (`number_square_mp.py`):

```
#!/usr/bin/env python
import numpy as np
import multiprocessing as mp

def square_me(num):
    result = int(np.square(num))
    return(result)

p = mp.Pool(processes=40)

for num in range(1,101):
    results = p.apply_async(square_me, [num])
    print(f'The square of {num} is {results.get()}')

p.close()
```

```
#!/usr/bin/env bash
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=05:00
#SBATCH --partition=short-40core
#SBATCH --job-name=parallel_job
#SBATCH --output=squared_numbers.txt

module load anaconda/3
python number_square_mp.py
```

A pool of 40 workers processes 40 calculations at a time, and results keep their input order naturally.

## Approach 3: Slurm job arrays

Spread independent tasks across many jobs (and nodes). Each array task reads one line from an input file (`100_numbers.txt`, one integer per line):

```
#!/usr/bin/env bash
#SBATCH --job-name=array_test
#SBATCH --output=array_test.%A_%a.log
#SBATCH --ntasks=1
#SBATCH -N 1
#SBATCH -p short-40core
#SBATCH -t 04:00:00
#SBATCH --array=1-100

module load anaconda/3

echo "Starting task $SLURM_ARRAY_TASK_ID"
INPUT=$(sed -n "${SLURM_ARRAY_TASK_ID}p" 100_numbers.txt)
python number_square.py $INPUT
```

Each task writes its own log (e.g. `array_test.816678_74.log`). Note there is no within-node parallelization here: this shape suits tasks that individually use a whole node.

## Approach 4: hybrid of job arrays + GNU Parallel

Combine both: 40 array tasks, each running 100 calculations with 40 parallel workers: 4,000 calculations in total:

```
#!/usr/bin/env bash
#SBATCH --job-name=array_test
#SBATCH --output=array_test.%A_%a.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH -N 1
#SBATCH -p short-40core
#SBATCH -t 04:00:00
#SBATCH --array=1-40

mkdir temp

module load anaconda/3
module load gnu-parallel/6.0

START=$SLURM_ARRAY_TASK_ID
NUMLINES=100
STOP=$((SLURM_ARRAY_TASK_ID*NUMLINES))
START="$(($STOP - $(($NUMLINES - 1))))"

echo "START=$START"
echo "STOP=$STOP"

for (( N = $START; N <= $STOP; N++ ))
do
    LINE=$(sed -n "$N"p 4k_numbers.txt)
    echo $LINE >> temp/tasks_${START}_${STOP}
done

cat temp/tasks_${START}_${STOP} | parallel --jobs 40 --verbose python number_square.py {}

rm temp/tasks_${START}_${STOP}
```

## Which approach when?

- **GNU Parallel**: simple standalone tasks; the fastest to set up
- **Python multiprocessing**: Python-native workflows needing fine-grained control
- **Job arrays**: distribute independent tasks across multiple nodes
- **Hybrid**: maximum scaling across nodes and cores at once

**Applies to:** SeaWulf

Ported from RCI's guide: <https://rci.stonybrook.edu/docs/guide-embarrassingly-parallel-workflows> (maintained by Research Computing and Informatics).
