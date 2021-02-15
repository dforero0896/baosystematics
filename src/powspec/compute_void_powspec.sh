#!/bin/bash

source ../.env
RUN="srun -p p4 -n1 -c 16 --mem-per-cpu=64G ${WORKDIR}/bin/powspec/POWSPEC"
SEED=1005638091
BOX_SIZE=2500
VOLUME=$(( ${BOX_SIZE} * ${BOX_SIZE} * ${BOX_SIZE} ))
for box in 1 #5
do
case $box in
  1)
   RMIN_C1=15.6
  ;;
  5)
   RMIN_C1=18.5
  ;;
  *)
   exit 1
  ;;
esac 

for space in redshift #real
do

for syst in nosyst #radialgauss smooth/parabola_0.8 
do

for case_ in 2 #3
do



if [[ "$syst" == "smooth/parabola_0.8" ]];then
SUFFIX=_wt_scaledR
FORMAT='"%f %f %f %f %*s %f"'
else
SUFFIX=_scaledR
FORMAT='"%f %f %f %f %*f"'
fi
if [[ "$syst" == "nosyst" ]]; then
CUBIC_SIM=1
else
CUBIC_SIM=0
fi

IDIR=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/mocks_void_xyz${SUFFIX}
RAN=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/void_ran/void_ran.dat
for DAT in $(ls ${IDIR}/*${SEED}*);do
NELEM=$(wc -l ${DAT} | awk '{print $1}')
DATA_NZ=$(echo "${NELEM}/${VOLUME}" | bc -l)

case ${case_} in

  1)
   SEL_COL=4
   SEL_MIN=${RMIN_C1}
   OSUFFIX=${RMIN_C1}-inf
  ;;
  2)
   SEL_COL=4
   MATTERDAT=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/mocks_gal_xyz/$(echo $(basename $DAT) | sed -e "s/\.VOID//g")
   NMATTERELEM=$(wc -l ${MATTERDAT} | awk '{print $1}')
   echo ${NMATTERELEM}
   NGAL=$(python -c "print(${NMATTERELEM}./${VOLUME})")
   echo ${NGAL}
   SEL_MIN=$(python -c "print(2.37/(${NGAL})**(0.238))")
   OSUFFIX=scaled2.37-inf
  ;;
  3)
   SEL_COL=5
   SEL_MIN=2.37
   OSUFFIX=loc-scaled2.37-inf
  ;;
  *)
   exit 1
  ;;
esac

ODIR=${WORKDIR}/patchy_results/box${box}/${space}/${syst}/powspec_void_mock_nowt_R-${OSUFFIX}
if [[ ! -e ${ODIR} ]]; then
mkdir -v ${ODIR}
fi

ONAME=${ODIR}/powspec_$(basename ${DAT})
SELECTION="\"\\\$${SEL_COL} > ${SEL_MIN} && \\\$1 < 2500 && \\\$1 > 0 && \\\$2 < 2500 && \\\$2 > 0 && \\\$3 < 2500 && \\\$3 > 0\""
COMMAND="${RUN} --data=${DAT} --rand=${RAN} --data-formatter=${FORMAT} --rand-formatter=${FORMAT} --data-nz=${DATA_NZ} --data-select=${SELECTION} --rand-select=${SELECTION} --auto=${ONAME} --sim=${CUBIC_SIM} --conf=$(readlink -f ${WORKDIR}/src/powspec/powspec.conf)"

echo "sbatch -J powspec -p p4 --mem-per-cpu=64G -n1 -c16 --wrap='${COMMAND}'"
done
done
done
done
done

