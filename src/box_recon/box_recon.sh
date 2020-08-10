#!/bin/bash

source ../.env
RUN=${WORKDIR}/src/baorec/compcorr.x

for box in 1 5; do

for space in real redshift; do 


IDIR=${WORKDIR}/patchy_results/box${box}/${space}/nosyst/mocks_gal_xyz
ODIR=$(echo ${IDIR} | sed -e "s/patchy_results/patchy_recon/g")
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*); do


break
done
done
done
