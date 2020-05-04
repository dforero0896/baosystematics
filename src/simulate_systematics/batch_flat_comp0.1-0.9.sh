#!/bin/bash
BOX=1
SPACE=redshift
for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do
#  echo "sbatch -p p4 -n 16 -c 1 --mem-per-cpu=8G -J rc${comp} --wrap='srun -n 32 -c 1 --mem-per-cpu=8G --mpi=pmi2 ./comp_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box${BOX}/${SPACE}/nosyst/mocks_gal_xyz ${comp}'"
  echo "sbatch -p p4 -n 16 -c 1 --mem-per-cpu=8G -J ${comp} --wrap='srun -n 16 -c 1 --mem-per-cpu=8G --mpi=pmi2 ./comp_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box${BOX}/${SPACE}/nosyst/mocks_gal_xyz -c ${comp} -b ${BOX} -s ${SPACE}'"
done

