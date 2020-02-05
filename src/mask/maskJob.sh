#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH -J mask     # Name of the job
#SBATCH --output=mask_%A_%x.out
#SBATCH --error=mask_%A_%x.err
#SBATCH --array=0-10
#SBATCH -p s1           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module load python/2.7.15
module load cfitsio
PAD_TASK_ID=`printf %02d $SLURM_ARRAY_TASK_ID`


bash $1$PAD_TASK_ID.sh
