#!/bin/bash
#SBATCH -n 5           # Number of tasks
#SBATCH -J combine         # Name of the job
#SBATCH -p p4          # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=ALL
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=1
#SBATCH --output=combine_%j_%x.out
module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module add python/2.7.15
module load mpi4py
srun -n $SLURM_NTASKS --mpi=pmi2 python /home/epfl/dforero/zhao/void/baosystematics/src/combine.py $1 $2 $3


