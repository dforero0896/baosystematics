#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH -J split_trim         # Name of the job
#SBATCH --output=%x_%a.out
#SBATCH --error=%x_%a.err
#SBATCH --array=0-9
#SBATCH -p s1           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G #We expect each big fits file will be around 3G

module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module load python/2.7.15
INPUT=$1
OUTPUT=$2
OVERWRITE=$3
if [[ ! -e $OUTPUT ]]; then
	mkdir $OUTPUT
fi
python /home/epfl/dforero/zhao/void/baosystematics/src/trim_masked_fits.py $INPUT $OUTPUT $SLURM_ARRAY_TASK_COUNT $SLURM_ARRAY_TASK_ID $OVERWRITE
