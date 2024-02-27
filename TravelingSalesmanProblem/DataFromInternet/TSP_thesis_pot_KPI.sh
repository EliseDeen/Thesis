#!/bin/bash
#
#SBATCH --job-name=Test
#SBATCH --output=Test.txt
#SBATCH --partition=compute (other options are memory and gpu)
#SBATCH --time=01:00:00
#SBATCH --ntasks=1 (number of python instances)
#SBATCH --cpus-per-task=48 (number of cores)
#SBATCH --mem=10GB (total memory)
#SBATCH --account=innovation
#
module load 2022r2
module load python
module load py-pip
(input your netid and Gurobi version below)
export
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/4896467/gurobi9.1.2
/linux64/lib
export
LIBRARY_PATH=$LIBRARY_PATH:/home/4896467/gurobi9.1.2/linux
64/lib
export PATH=$PATH:/home/4896467/gurobi9.1.2/linux64/bin
export
CPATH=$CPATH:/home/4896467/gurobi9.1.2/linux64/include
srun python main.py