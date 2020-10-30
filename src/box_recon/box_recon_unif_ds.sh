#!/bin/bash

source ../.env
RUN=${WORKDIR}/src/box_recon/dorecon.py
PARAMS=${WORKDIR}/src/box_recon/params_ran_box_noran.py
N=${SLURM_NTASKS:-1}
echo Using ${N} tasks
#SEED=1876527057
#SEED=1942922759
for SEED in 1248755586 114530336 
do
#SEED=1005638091
#for syst in smooth/flat_0.1  smooth/flat_0.15  smooth/flat_0.2  smooth/flat_0.25  smooth/flat_0.3  smooth/flat_0.35  smooth/flat_0.4  smooth/flat_0.45  smooth/flat_0.5  smooth/flat_0.55  smooth/flat_0.6  smooth/flat_0.65  smooth/flat_0.7  smooth/flat_0.75 smooth/flat_0.8  smooth/flat_0.85 smooth/flat_0.9 smooth/flat_0.95   
for syst in smooth/flat_0.3
do
for box in 1 #5 
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

for space in redshift #real
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
ODIR=${WORKDIR}/patchy_recon_nods/box${box}/${space}/${syst}/mocks_gal_xyz/
if [[ ! -e ${ODIR} ]] ; then
mkdir -vp ${ODIR}
fi

for file in $(ls ${IDIR}/*$SEED*); do
((i=i%N)); ((i++==0)) && wait
#if [[ -e ${ODIR}/$(basename ${file} |  sed -e "s/.dat/.ran_pos_shift.dat/g") ]]; then
#continue
#fi
if [[ -e ${ODIR}/$(basename ${file} |  sed -e "s/.dat/_pos_shift.dat/g") ]]; then
continue
fi
#srun -n1 -c16 -N1 python ${RUN} --par=${PARAMS} --tracer-file=${file} --output-folder=${ODIR} --f=${f} --bias=${bias} --rsd-correct=${rsd_corr} &
python ${RUN} --par=${PARAMS} --tracer-file=${file} --output-folder=${ODIR} --f=${f} --bias=${bias} --rsd-correct=${rsd_corr} 
#exit 0
done
done
done
done
done
wait
