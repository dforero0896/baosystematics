#!/bin/bash

source ../.env
RUN=${WORKDIR}/src/box_recon/dorecon.py
PARAMS=${WORKDIR}/src/box_recon/params_ran_box_nopad.py
N=${SLURM_NTASKS:-1}
echo Using ${N} tasks
#SEED=1656249224
#SEED=824062495
#SEED=1005638091
for syst in smooth/parabola_0.8 #radialgauss nosyst
do
case ${syst} in
  smooth/parabola_0.8 |  nosyst)
    RAND=${WORKDIR}/patchy_results/randoms/box_uniform_random_seed1_0-2500.dat
  ;;
  radialgauss)
    RAND=${WORKDIR}/patchy_results/randoms/box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat
  ;;
  *)
    echo Systematics case ${syst} not recognized
  ;;
esac
for box in 1 5
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

for space in real #redshift
do
case ${space} in
    real)
      rsd_corr=0
    ;;
    redshift)
      rsd_corr=1
    ;;
    *)
    echo Space ${space} not understood.; exit 1
    ;;
esac
bias=1.92
IDIR=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/mocks_gal_xyz
ODIR=${WORKDIR}/patchy_recon/box${box}/${space}/${syst}/mocks_gal_xyz/
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*$SEED*); do
((i=i%N)); ((i++==0)) && wait
if [[ -e ${ODIR}/$(basename ${file} |  sed -e "s/.dat/.ran_pos_shift.dat/g") ]]; then
continue
fi
#if [[ -e ${ODIR}/$(basename ${file} |  sed -e "s/.dat/_pos_shift.dat/g") ]]; then
#continue
#fi
srun -n1 -c16 -N1 python ${RUN} --par=${PARAMS} --tracer-file=${file} --random-file=${RAND} --output-folder=${ODIR} --f=${f} --bias=${bias} --rsd-correct=${rsd_corr} &
#python ${RUN} --par=${PARAMS} --tracer-file=${file} --random-file=${RAND} --output-folder=${ODIR} --f=${f} --bias=${bias} --rsd-correct=${rsd_corr} 
#exit 0
done
done
done
done
wait
