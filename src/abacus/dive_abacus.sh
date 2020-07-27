#!/bin/bash

source  ../.env
module load spack/default gcc/5.4.0 boost

RUN=${WORKDIR}/bin/DIVE_box/DIVE_box
ABACUS_DIR=${WORKDIR}/abacus_results
mkdir -v -p joblist
if [[ -e joblist/dive_jobs.sh ]]; then
	rm -v joblist/dive_jobs.sh
fi
for halo_file in $(ls ${ABACUS_DIR}/AbacusCosmos_1100box_products/AbacusCosmos_1100box_*_products/AbacusCosmos_1100box_*_rockstar_halos/*/halos.dat)
do
	ODIR=$(dirname ${halo_file})
	INAME=$(basename ${halo_file})
	ONAME=${ODIR}/halo_voids.dat
	echo "${RUN} ${halo_file} ${ONAME} 1100 0 999" >> joblist/dive_jobs.sh

done

