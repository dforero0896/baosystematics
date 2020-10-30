#!/bin/bash
BOX=1
SPACE=redshift
NCORES=1
source ../.env
DIR=${WORKDIR}/patchy_results
NU=$(python -c 'print(1./3)')
#for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
for comp in 0.65
do
for scaled_rmin in 0.8 #0.75 0.7 #1.13 1 0.87 1.25 1.33 1.07 1.19 1.18 0.93
do 
#  echo "sbatch -p p4 -n 16 -c 1 --mem-per-cpu=8G -J rc${comp} --wrap='srun -n 32 -c 1 --mem-per-cpu=8G --mpi=pmi2 ./comp_mask_catalog.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box${BOX}/${SPACE}/nosyst/mocks_gal_xyz ${comp}'"
  echo "sbatch -p p4 -n ${NCORES} -c 1 --mem-per-cpu=12G -J ${comp} --wrap='srun -n ${NCORES} -c 1 --mem-per-cpu=8G --mpi=pmi2 ./comp_mask_catalog.py ${DIR}/box${BOX}/${SPACE}/nosyst/mocks_gal_xyz -c ${comp} -b ${BOX} -s ${SPACE} -r ${scaled_rmin} -nu ${NU}'"
done
done
