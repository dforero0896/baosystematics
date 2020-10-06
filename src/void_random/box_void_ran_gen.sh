#!/usr/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics
NCORES=32
suffix=_scaledR
odir=void_ran${suffix}
results_dir=$1
if [[ $# -ne 3 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 RESULTS_DIR OVERWRITE KIND
	exit 1
fi
if [[ ! -e $results_dir ]]; then
	echo ERROR: Directory not found
	exit 1
fi
[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}" 
if [[ ! -e $results_dir/${odir} ]]; then
	mkdir -v $results_dir/${odir}
fi
#r_min=$2
#r_max=$3
overwrite=$2
kind=$3
nrandoms=240000000
if [[ ! -e $results_dir/${odir}/BIG_RAN_VOID.dat ]] || [[ $overwrite -eq 1 ]];then
rm -v -r $results_dir/${odir}/bins
srun -n $NCORES -c 1 --mpi=pmi2 python $WORKDIR/src/void_random/create_bins.py $results_dir/mocks_void_xyz${suffix}/ 1 --kind ${kind} --odir=${odir} || exit 1
echo Shuffling...
srun -n1 -c1 bash $WORKDIR/src/void_random/box_shuffle_columns.sh $results_dir/${odir}/bins ${kind} 0 || exit 1
fi
echo Selecting ${nrandoms} objects
srun -n1 -c1 shuf -n $nrandoms $results_dir/${odir}/BIG_RAN_VOID.dat> $results_dir/${odir}/${odir}.dat || exit 1
