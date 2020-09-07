#!/bin/bash

source ../.env
RUN="mv -v"
N=16
for box in 1 5 
do

for space in real redshift
do

IDIR=${WORKDIR}/patchy_recon/box${box}/${space}/nosyst/mocks_gal_xyz
ODIR=$(echo ${IDIR} | sed -e "s/mocks_gal_xyz/baorec_pspec/g")
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/pow*); do
((i=i%N)); ((i++==0)) && wait
${RUN} ${file} ${ODIR}/ &
done
done
done
