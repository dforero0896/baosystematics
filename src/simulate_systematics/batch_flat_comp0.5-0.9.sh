#!/bin/bash

for comp in 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do
  #echo "sbatch -p p4 -n 32 -c 1 --mem-per-cpu=30G -J rc${comp} --wrap='srun -n 32 -c 1 --mem-per-cpu=30G --mpi=pmi2 ./comp_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/nosyst/mocks_gal_xyz ${comp}'"
  echo "sbatch -p p4 -n 32 -c 1 --mem-per-cpu=30G -J zc${comp} --wrap='srun -n 32 -c 1 --mem-per-cpu=30G --mpi=pmi2 ./comp_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/redshift/nosyst/mocks_gal_xyz ${comp}'"
done
