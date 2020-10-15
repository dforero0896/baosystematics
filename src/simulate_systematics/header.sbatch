#!/bin/bash
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -q regular
#SBATCH -J galdr
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=ALL
#SBATCH -t 04:00:00

#OpenMP settings:
export OMP_NUM_THREADS=64
export OMP_PLACES=threads
export OMP_PROC_BIND=spread


