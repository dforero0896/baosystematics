#!/bin/bash
rm -v recon_joblist.sh
source ../.env
RUN=${WORKDIR}/bin/FCFC_box/2pcf
CONF=${WORKDIR}/src/fcfc_box/fcfc_box_void_count_redshift.conf
N=${SLURM_NTASKS:-1}
echo \#Using ${N} tasks
#SEED=996166056
#SEED=1005638091
NGAL_COMPLETE=3.977e-4
for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do
NGAL=$(python -c "print(${comp}*${NGAL_COMPLETE})")
for box in 1 #5
do

for space in redshift #real
do
IDIR=${WORKDIR}/patchy_recon_nods/box${box}/${space}/smooth/flat_${comp}/mocks_void_xyz
for sr in 0.8 0.87 0.93 1.0 1.07 1.13 #1.19 1.25 1.33 0.7 0.75
do
#if (( $(echo "${comp} > 0.35" | bc -l) )) && (( $(echo "${sr} < 0.85" | bc -l) )); then
#continue
#fi

RMIN=$(python -c "print(${sr}/(${NGAL})**(1/3))")
ODIR=$(dirname ${IDIR})/tpcf_void_mock_nowt_R-scaled${sr}-50
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
if [[ ! -e ${ODIR}/DD_files ]] ; then
mkdir -vp ${ODIR}/DD_files
mkdir -vp ${ODIR}/DS_files
mkdir -vp ${ODIR}/SS_files
fi
fi

for DAT in $(ls ${IDIR}/*$SEED*dat ); do
((i=i%N)); ((i++==0)) && wait
BASE=$(basename ${DAT})
DD=${ODIR}/DD_files/DD_${BASE}
DR=${ODIR}/DS_files/DS_${BASE}
RR=${ODIR}/SS_files/SS_${BASE}
TPCF=${ODIR}/TwoPCF_${BASE}
if [[ -e ${TPCF} ]]; then
echo Skipping, ${TPCF} exists.
continue
fi
srun -n1 -c16 ${RUN} --conf=${CONF} --data=${DAT} --dd=${DD} --output=${TPCF} --data-aux-min=${RMIN} --data-aux-max=50 --count-mode=1 --cf-mode=3 &
#echo "srun -n1 -c64 ${RUN} --conf=${CONF} --data=${DAT} --dd=${DD} --output=${TPCF} --data-aux-min=${RMIN} --data-aux-max=50 --count-mode=1 --cf-mode=3" >> recon_joblist.sh
done
done
done
done
done
wait
