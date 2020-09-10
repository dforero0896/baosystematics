#!/bin/bash

source ../.env
RUN=${WORKDIR}/bin/FCFC_box/2pcf
CONF=${WORKDIR}/src/box_recon/fcfc.conf
N=${SLURM_NTASKS:-1}
echo \#Using ${N} tasks
#SEED=996166056
#SEED=1005638091
for box in 1 #5
do

for space in redshift #real
do
case ${box} in
  1)
    redshift=0.466
    f=0.7432282059175079
  ;;
  5)
    redshift=0.638
    f=0.7967003161750181
  ;;
  *)
    exit 1
  ;;
esac
bias=1.92
IDIR=${WORKDIR}/patchy_recon/box${box}/${space}/nosyst/mocks_gal_xyz
ODIR=$(dirname ${IDIR})/tpcf_gal_mock_nowt
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
if [[ ! -e ${ODIR}/DD_files ]] ; then
mkdir -vp ${ODIR}/DD_files
mkdir -vp ${ODIR}/DS_files
mkdir -vp ${ODIR}/SS_files
fi
fi

for DAT in $(ls ${IDIR}/*$SEED* | grep -v ran_pos_shift.dat); do
((i=i%N)); ((i++==0)) && wait
RAN=$(echo ${DAT} | sed -e "s/_pos_shift.dat/.ran_pos_shift.dat/g")
BASE=$(basename ${DAT})
DD=${ODIR}/DD_files/DD_${BASE}
DR=${ODIR}/DS_files/DS_${BASE}
RR=${ODIR}/SS_files/SS_${BASE}
TPCF=${ODIR}/TwoPCF_${BASE}
if [[ -e ${TPCF} ]]; then
continue
fi
echo "srun -n1 -c16 -N1 ${RUN} --conf=${CONF} --data=${DAT} --rand=${RAN} --dd=${DD} --dr=${DR} --rr=${RR} --output=${TPCF} "
#break
done
done
done
wait
