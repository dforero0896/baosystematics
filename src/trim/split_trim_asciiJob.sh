#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH -J mergeCats         # Name of the job
#SBATCH --output=split_trim_%j__%x.out
#SBATCH --error=split_trim_%j_%x.err
#SBATCH -p p4           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=60M #We expect each catalog to be about 24M

module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module load python/2.7.15
module load mpi4py
INPUT=$1
OUTPUT=$2
OVERWRITE=$3
srun -n $SLURM_NTASKS --mpi=pmi2 python /home/epfl/dforero/zhao/void/baosystematics/src/trim_masked_ascii.py $INPUT $OUTPUT $OVERWRITE

