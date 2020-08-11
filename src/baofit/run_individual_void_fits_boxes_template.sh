#!/bin/bash
source ../.env

RUN=${SRC}/baofit/baofit_void_dir.py

for BOX in 5 #1
do
for SPACE in real #redshift
do
for SYST in radialgauss #smooth/parabola_0.8 #nosyst radialgauss
do
for CASE in 3 #2 #1
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
INPVOID=${WORKDIR}/patchy_linhalo/box${BOX}/real/${SYST}/void_template/PKvoid_template_case${CASE}.pspec
if [[ ! -e ${ODIR} ]]; then
mkdir -v ${ODIR}
fi

#readlink -f ${INPVOID}
cd $ODIR && ${RUN} ../../tpcf_void_mock_nowt_R-${SUFFIX}/ ./ void none --void-temp ${INPVOID}
wc -l ${ODIR}/void_dir_joblist.sh
echo "sbatch -p p4 -n1 -c16 -J baofit --chdir=${ODIR} --wrap='~/codes/jobfork_setup/jobfork_omp void_dir_joblist.sh'"
done
done
done
done
