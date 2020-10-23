#!/bin/bash
source ../.env
N=${SLURM_N_TASKS:-1}
echo Using ${N} tasks
RUN=${WORKDIR}/bin/DIVE_box/DIVE_box
for comp in 0.85
do
IDIR=${WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_${comp}/
ls -d ${IDIR}
GALDIR=${IDIR}/mocks_gal_xyz
VOIDDIR=${IDIR}/mocks_void_xyz
for cat in $(ls ${GALDIR}/* | grep -v ran)
do
((i=i%N)); ((i++==0)) && wait
ocat=${VOIDDIR}/$(basename ${cat} | sed -e "s/.dat/.VOID.dat/g")
ocat_t=${ocat}.TMP
if [[ -e ${ocat} ]] ;then
echo Skipping, ${ocat} exists
continue
fi
${RUN} ${cat} ${ocat_t} 2500 0 999 && mv -v ${ocat_t} ${ocat} & 
done
done
wait
