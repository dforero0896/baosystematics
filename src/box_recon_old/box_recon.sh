#!/bin/bash

source ../.env
RUN=${WORKDIR}/bin/baorec/compcorr.x
N=${SLURM_NTASKS:-1}
echo Using ${N} tasks
#SEED=996166056
SEED=1005638091
task(){
srun -n1 -c16 -N1 ${RUN} $1 $2 $3/ $4 $5 $6
base=$(basename $1)
rm -v $2/psi*${base}*
rm -v $2/v*${base}*
rm -v $2/delta*${base}*

}
for box in 1 5
do

for space in redshift real
do
case ${box} in
  1)
    redshift=0.466
  ;;
  5)
    redshift=0.638
  ;;
  *)
    exit 1
  ;;
esac

if [[ "$space" == "redshift" ]];then
rsd_apply=0
rsd_correct=1
input_format=4
elif [[ "$space" == "real" ]]; then
rsd_apply=0
rsd_correct=0
input_format=1
else
echo Space not recognized.
exit 1
fi
IDIR=${WORKDIR}/patchy_results/box${box}/${space}/nosyst/mocks_gal_xyz
ODIR=${WORKDIR}/patchy_recon/box${box}/${space}/nosyst/mocks_gal_xyz
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*$SEED*); do
((i=i%N)); ((i++==0)) && wait
#if [[ -e ${ODIR}/CAT$(basename $file)rS5.0.dat ]]; then
#continue
#fi
task ${file} ${ODIR}/ ${redshift} ${rsd_apply} ${rsd_correct} ${input_format}&
#break
done
done
done
wait
