#!/bin/bash
if [[ $# -eq 3 ]];
then
	DEPENDENCYID=$3
	dependencycommand="--dependency=afterok:$DEPENDENCYID"
elif [[ $# -eq 2 ]];
then
	dependencycommand=''
else
	echo "ERROR: No job list provided."
	echo "USAGE: bash $0 JOB_LIST_ID N_JOBS DEPENDENCYID(optional)"
	echo "DIRECTION=rdz2xyz, xyz2rdz"
	exit 1
fi
this_dir="$(dirname $0)" #path from run dir to source dir
in_fn="$(filename $1)"
out_fn="${in_fn%%.*}"
DEPENDENCYID=$3
PWD=$(pwd)
abs_path=$(echo $pwd/$this_dir) #full path to source so it is reachable from everywhere
out_dir="$this_dir/../results/$out_fn/maskJob"
if [[ ! -e $out_dir ]]; then
	mkdir $out_dir
fi
n_files=$2
n_lines=$(wc -l < $this_dir/catalog_mask_$1.sh)
n_lines_per_file=$(($n_lines / $n_files))
if [[ $n_lines_per_file -eq 0 ]]; then
	n_lines_per_file=1
fi
if [[ $n_lines -eq 0 ]]; then
	maskJobid=$(sbatch -output=$out_dir/'maskJob_%x_%A_%a.out' --error=$out_dir/'maskJob_%x_%A_%a.err' --dependency=afterok:$DEPENDENCYID --wrap="echo No files writtten to job list")
	echo $maskJobid
else
	rm $this_dir/joblist_split/catalog_mask_$(echo $out_fn)_SLICE*
	split -dl $n_lines_per_file --additional-suffix=.sh $this_dir/catalog_mask_$1.sh $this_dir/joblist_split/catalog_mask_$(echo $out_fn)_SLICE
	n_files=$(ls $this_dir/joblist_split/catalog_mask_$(echo $out_fn)_SLICE* | wc -l)
	echo "Launching $n_files jobs with $n_lines_per_file lines each."
	maskJobid=$(sbatch $dependencycommand --array=0-$(($n_files-1)) --job-name=mask_$out_fn --output=$out_dir/'maskJob_%x_%A_%a.out' --error=$out_dir/'maskJob_%x_%A_%a.err' $this_dir/maskJob.sh $this_dir/joblist_split/catalog_mask_$(echo $out_fn)_SLICE)
	echo $maskJobid
fi
