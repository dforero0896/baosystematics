#!/usr/bin/env bash
module load python/2.7.15
results_dir=$1
if [[ $# -ne 1 ]]; then
	echo ERROR: Directory not provided
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
bash /home/epfl/dforero/zhao/void/baosystematics/src/stack_random_catalogs.sh $results_dir/mock_void_masked_trimmed_catalogs/ $results_dir/void_ran/RAW_RAN_VOID_NGC.ascii NGC 100
python /home/epfl/dforero/zhao/void/baosystematics/src/shuffle_columns.py $results_dir/void_ran/RAW_RAN_VOID_NGC.ascii $results_dir/void_ran/BIG_RAN_VOID_NGC.ascii 1
shuf -n 2700000 $results_dir/void_ran/BIG_RAN_VOID_NGC.ascii> $results_dir/void_ran/EZ_ELG_RDZ_void_ran_NGC.ascii
bash /home/epfl/dforero/zhao/void/baosystematics/src/stack_random_catalogs.sh $results_dir/mock_void_masked_trimmed_catalogs/ $results_dir/void_ran/RAW_RAN_VOID_SGC.ascii SGC 100
python /home/epfl/dforero/zhao/void/baosystematics/src/shuffle_columns.py $results_dir/void_ran/RAW_RAN_VOID_SGC.ascii $results_dir/void_ran/BIG_RAN_VOID_SGC.ascii 1
shuf -n 2700000 $results_dir/void_ran/BIG_RAN_VOID_SGC.ascii> $results_dir/void_ran/EZ_ELG_RDZ_void_ran_SGC.ascii
