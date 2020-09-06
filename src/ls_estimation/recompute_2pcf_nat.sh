#!/bin/bash
source ../.env
NTASKS=${SLURM_NTASKS:-16}
NNODES=${SLURM_JOB_NUM_NODES:-1}
N=$(( ${NTASKS}*${NNODES} ))
echo Using $N tasks
task(){
TPCF_file=$(echo $1 | sed -e "s/DD_files\///g; s/DD/TwoPCF/g")
~/codes/2pcf.py -dd $1 -rr $2 -o ${TPCF_file} &
}
for BOX in 1 5 
do
for SPACE in real redshift
do
for wtflag in 0 1
do
case ${wtflag} in

	0)
	FOLDER=tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5
	RAN_SUFFIX=
	;;
	1)
	FOLDER=tpcf_void_mock_R-loc_scaled2.2-loc_scaled5
	RAN_SUFFIX=_wt1
	;;
	*)
	echo Weight flag not understood
	exit 1
	;;
esac

OUT=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/smooth/parabola_0.8/${FOLDER}
RR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/smooth/parabola_0.8/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5_wt0${RAN_SUFFIX}.dat
for DD in $(ls ${OUT}/DD_files/DD*)
do
((i=i%N)); ((i++==0)) && wait
task $DD $RR

done
done
done
done

