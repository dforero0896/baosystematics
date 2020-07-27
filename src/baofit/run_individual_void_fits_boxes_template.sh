#!/bin/bash
source ../.env

RUN=${SRC}/baofit/baofit_void_dir.py

for BOX in 1 #5
do
for SPACE in real redshift
do
for SYST in nosyst #smooth/parabola_0.8 radialgauss
do
for CASE in 1 #2 3
do
case ${CASE} in
1)
SUFFIX=15.6-50
;;
2)
SUFFIX=scaled2.2-50
;;
3)
SUFFIX=loc_scaled2.2-loc_scaled5
;;
*)
exit 1
;;
esac

ODIR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/${SYST}/baofit/individual_void_nowt_case${CASE}_template
if [[ ! -e ${ODIR} ]]; then
mkdir -v ${ODIR}
fi
cd $ODIR && ${RUN} ../../tpcf_void_mock_nowt_R-${SUFFIX}/ ./ void none
wc -l ${ODIR}/void_dir_joblist.sh
echo "sbatch -p p5 -n1 -c1 --chdir=${ODIR} --wrap='bash void_dir_joblist.sh'"
done
done
done
done
