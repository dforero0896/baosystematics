#!/bin/bash
source ../.env

RUN=${SRC}/baofit/baofit_void_dir.py

for BOX in 1 #5
do
for SPACE in real redshift
do
for SYST in radialgauss #smooth/parabola_0.8 #nosyst radialgauss
do
for CASE in 1 #2 3
do
case ${CASE} in
1)
	case ${BOX} in
	1)
	SUFFIX=15.6-50
	;;
	5)
	SUFFIX=18.5-50
	;;
	esac
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
echo "sbatch -p p4 -n1 -c16 --chdir=${ODIR} --wrap='~/codes/jobfork_setup/jobfork_omp void_dir_joblist.sh'"
done
done
done
done
