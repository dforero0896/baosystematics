#!/bin/bash
source ../.env
for recon in patchy_recon #patchy_results
do
for box in 1 5
do
for space in real redshift
do
IDIR=${WORKDIR}/patchy_results/box${box}/${space}/radialgauss/mocks_void_xyz
ODIR=${WORKDIR}/patchy_results/box${box}/${space}/radialgauss/plots
srun -n1 -c32 -p p5 python plot_radius_distribution.py ${IDIR} ${ODIR}
IDIR=${WORKDIR}/patchy_results/box${box}/${space}/smooth/parabola_0.8/mocks_void_xyz
ODIR=${WORKDIR}/patchy_results/box${box}/${space}/parabola_0.8/plots
srun -n1 -c32 -p p5 python plot_radius_distribution.py ${IDIR} ${ODIR}
done
done
done
