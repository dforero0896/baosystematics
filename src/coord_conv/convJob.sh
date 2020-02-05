#!/bin/bash
#SBATCH -n 1           # Number of tasks
#SBATCH -J xyz2rdz         # Name of the job
#SBATCH --output=convJob_%A_%a.out
#SBATCH --error=convJob_%A_%a.err
####SBATCH --output=./convJob/convJob_%A.out
####SBATCH --error=./convJob/convJob_%A.err
#SBATCH --array=0-10
#SBATCH -p s1           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module add python/2.7.15

PAD_TASK_ID=`printf %02d $SLURM_ARRAY_TASK_ID`


bash $1$PAD_TASK_ID.sh


