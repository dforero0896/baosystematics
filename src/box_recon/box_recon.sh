#!/bin/bash

source ../.env
RUN=${WORKDIR}/src/box_recon/dorecon.py
PARAMS=${WORKDIR}/src/box_recon/params_ran_box_nopad.py
N=${SLURM_NTASKS:-1}
echo Using ${N} tasks
#SEED=996166056
#SEED=1005638091
task(){
srun -n1 -c16 -N1 ${RUN} --par=${PARAMS} --tracer-file=$1 --random-file=$2 --output-folder=$3
}
for box in 1 5
do

for space in redshift real
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
IDIR=${WORKDIR}/patchy_results/box${box}/${space}/nosyst/mocks_gal_xyz
ODIR=${WORKDIR}/patchy_recon/box${box}/${space}/nosyst/mocks_gal_xyz/
RAND=${WORKDIR}/patchy_results/randoms/box_uniform_random_seed1_0-2500.dat
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*$SEED*); do
((i=i%N)); ((i++==0)) && wait
srun -n1 -c32 -N1 python ${RUN} --par=${PARAMS} --tracer-file=${file} --random-file=${RAND} --output-folder=${ODIR} --f=${f} --bias=${bias} &
#if [[ -e ${ODIR}/CAT$(basename $file)rS5.0.dat ]]; then
#continue
#fi
#break
done
done
done
wait
