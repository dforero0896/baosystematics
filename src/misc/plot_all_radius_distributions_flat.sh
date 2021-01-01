#!/bin/bash
source ../.env
for recon in patchy_recon_nods #patchy_results
do
for box in 1 #5
do
for space in redshift #real
do
for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do
IDIR=${WORKDIR}/${recon}/box${box}/${space}/smooth/flat_${comp}/mocks_void_xyz
if [[ ! -e ${IDIR} ]]; then
    continue
fi
ODIR=${WORKDIR}/${recon}/box${box}/${space}/smooth/flat_${comp}/plots
mkdir ${ODIR}
srun -n1 -c32 -p p5 python plot_radius_distribution.py ${IDIR} ${ODIR} &
done
done
done
done
