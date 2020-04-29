#!/usr/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics
NCORES=32
results_dir=$1
if [[ $# -ne 2 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 RESULTS_DIR OVERWRITE
	exit 1
fi
if [[ ! -e $results_dir ]]; then
	echo ERROR: Directory not found
	exit 1
fi
[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}" 
if [[ ! -e $results_dir/void_ran ]]; then
	mkdir -v $results_dir/void_ran
fi
#r_min=$2
#r_max=$3
overwrite=$2
nrandoms=240000000
if [[ ! -e $results_dir/void_ran/BIG_RAN_VOID.dat ]] || [[ $overwrite -eq 1 ]];then
srun -n 1 -c $NCORES python $WORKDIR/src/void_random/create_bins.py $results_dir/mocks_void_xyz_wt_scaledR/ 0 || exit 1
echo Shuffling...
bash $WORKDIR/src/void_random/box_shuffle_columns.sh $results_dir/void_ran/bins 0 || exit 1
fi
echo Selecting ${nrandoms} objects
shuf -n $nrandoms $results_dir/void_ran/BIG_RAN_VOID.dat> $results_dir/void_ran/void_ran.dat || exit 1
