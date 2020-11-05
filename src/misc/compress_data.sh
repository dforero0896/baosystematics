#!/bin/bash

source ../.env
Nthreads=$(( 2 * ${SLURM_CPUS_PER_TASK:-1} ))
echo Using $Nthreads threads

for recon in patchy_results patchy_recon_nods # patchy_recon
do

for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do

DIR=${WORKDIR}/${recon}/box1/redshift/smooth/flat_${comp}/
GAL=${DIR}/mocks_gal_xyz
VOID=${DIR}/mocks_void_xyz

cd ${GAL} && ls | grep -v xz | parallel -j ${Nthreads} -I'{}' srun -n1 -c1 xz -9vf {}
cd ${VOID} && ls | grep -v xz | parallel -j ${Nthreads} -I'{}' srun -n1 -c1 xz -9vf {}

done
done
