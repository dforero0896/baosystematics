#!/usr/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics
results_dir=$1
if [[ $# -ne 5 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 RESULTS_DIR R_MIN R_MAX TRACER OVERWRITE
	exit 1
fi
if [[ ! -e $results_dir ]]; then
	echo ERROR: Directory not found
	exit 1
fi
[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}" 
if [[ ! -e $results_dir/void_ran ]]; then
	mkdir $results_dir/void_ran
fi
r_min=$2
r_max=$3
tracer=$4
overwrite=$5
nrandoms=15000000
if [[ $overwrite -eq 1 ]] || [[ ! -e $results_dir/void_ran/BIG_RAN_VOID_NGC.ascii ]];then
bash $WORKDIR/src/void_random/stack_random_catalogs.sh $results_dir/mocks_void_rdz_finalmask/ $results_dir/void_ran/RAW_RAN_VOID_NGC.ascii NGC 100
echo Shuffling...
python $WORKDIR/src/void_random/shuffle_columns.py $results_dir/void_ran/RAW_RAN_VOID_NGC.ascii $results_dir/void_ran/BIG_RAN_VOID_NGC.ascii $overwrite
fi
echo Selecting objects with R in \[$r_min, $r_max\] in NGC cap.
awk -v rmin="$r_min" -v rmax="$r_max" -F"\t" '($4*1) > rmin && ($4*1) < rmax' $results_dir/void_ran/BIG_RAN_VOID_NGC.ascii | shuf -n $nrandoms > $results_dir/void_ran/EZ_"$tracer"_RDZ_void_ran_NGC_R-$r_min-$r_max.ascii
if [[ $overwrite -eq 1 ]] || [[ ! -e $results_dir/void_ran/BIG_RAN_VOID_SGC.ascii ]];then
bash $WORKDIR/src/void_random/stack_random_catalogs.sh $results_dir/mocks_void_rdz_finalmask/ $results_dir/void_ran/RAW_RAN_VOID_SGC.ascii SGC 100
echo Shuffling...
python $WORKDIR/src/void_random/shuffle_columns.py $results_dir/void_ran/RAW_RAN_VOID_SGC.ascii $results_dir/void_ran/BIG_RAN_VOID_SGC.ascii $overwrite
fi
echo Selecting objects with R in \[$r_min, $r_max\] in SGC cap.
awk -v rmin="$r_min" -v rmax="$r_max" -F"\t" '($4*1) > rmin && ($4*1) < rmax' $results_dir/void_ran/BIG_RAN_VOID_SGC.ascii | shuf -n $nrandoms > $results_dir/void_ran/EZ_"$tracer"_RDZ_void_ran_SGC_R-$r_min-$r_max.ascii
