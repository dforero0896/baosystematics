#!/bin/bash

source ../.env
RUN=${WORKDIR}/bin/baorec/baorec.x
N=$SLURM_NTASKS
SEED=996166056
task(){
srun -n1 -c16 -N1 ${RUN} $1 $2 $3/
base=$(basename $1)
rm -v $2/psi*${base}*

}
for box in 1 #5
do

for space in redshift #real
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
echo "==> Be sure to change to rsd=true in input.par"
fi
IDIR=${WORKDIR}/patchy_results/box${box}/real/nosyst/mocks_gal_xyz
ODIR=${WORKDIR}/patchy_recon/box${box}/${space}/nosyst/mocks_gal_xyz
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*$SEED*); do
((i=i%N)); ((i++==0)) && wait
#if [[ -e ${ODIR}/CAT$(basename $file)rS5.0.dat ]]; then
#continue
#fi
task ${file} ${ODIR}/ ${redshift}&
#break
done
done
done
wait
