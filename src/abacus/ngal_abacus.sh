#!/bin/bash

source  ../.env
N=${1:-16}
task(){
wc -l $1 | awk '{print $1}' > $2
}

ABACUS_DIR=${WORKDIR}/abacus_results
for halo_file in $(ls ${ABACUS_DIR}/AbacusCosmos_1100box_products/AbacusCosmos_1100box_*_products/AbacusCosmos_1100box_*_rockstar_halos/*/halos.dat)
do
	((i=i%N)); ((i++==0)) && wait
	ODIR=$(dirname ${halo_file})
	INAME=$(basename ${halo_file})
	ONAME=${ODIR}/avg_gal_density.dat
	task ${halo_file} ${ONAME} &

done

