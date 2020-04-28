#!/bin/bash
NCORES=1
partition=${1:-p5}
for box in 1 5
do
for space in real redshift
do
echo "sbatch -p ${partition} -n ${NCORES} -c 1 -J ${box}${space} --mem-per-cpu=8G --wrap='srun -n ${NCORES} -c 1 --mpi=pmi2 --mem-per-cpu=8G python radial_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box${box}/${space}/nosyst/mocks_gal_xyz/ ${box} ${space}'"
done
done
