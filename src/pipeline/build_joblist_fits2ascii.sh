#!/bin/bash
#build_joblist.sh
if [[ $# -eq 3 ]]; then
	raw_dir=$1
	[[ "${raw_dir}" == */ ]] && raw_dir="${raw_dir: : -1}"
	results_dir=$2
	[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}"
	overwrite=$3
elif [[ $# -eq 5 ]]; then
	raw_dir=$1
	[[ "${raw_dir}" == */ ]] && raw_dir="${raw_dir: : -1}"
	results_dir=$2
	[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}"
	splitmode=$4
	if [[ $splitmode -eq 1 ]]; then
		n_files=$5
		echo "Splitting in $n_files job lists"
	elif [[ $splitmode -eq 2 ]]; then
		n_lines_per_file=$5
		echo "Splitting in joblists with $n_lines_per_file lines per file"
	else
		echo "ERROR: Split mode not understood."
		echo "Choose SPLIT_MODE = 1 (split in N files)"
		echo "Choose SPLIT_MODE = 2 (split in files with N lines)"
	fi
	overwrite=$3
else
	echo "ERROR: Unxepected number of arguments."
	echo "USAGE: bash $0 RAW_DIR RESULTS_DIR OVERWRITE [SPLIT_MODE N]"
	exit 1
fi
id=$(basename $results_dir)
this_dir=$(dirname $0)
[[ "${this_dir}" == */ ]] && this_dir="${this_dir: : -1}"
if [[ ! -e $this_dir/joblists ]]; then
	mkdir $this_dir/joblists
fi
joblist_name=$this_dir/"joblists/premask_joblist_$(echo $id).sh"
if [[ ! -e $raw_dir ]]; then
	echo ERROR: Input directory not found.
	exit 1
fi

if [[ -e $joblist_name ]]; then
	rm $joblist_name
fi
echo Writing $joblist_name
echo Overwriting = $overwrite
for filename in $raw_dir/*NGC*.dat.*; do
	echo "bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/pipeline_file.sh $filename $results_dir $overwrite" >> $joblist_name
done
for filename in $raw_dir/*SGC*.dat.*; do
	echo "bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/pipeline_file.sh $filename $results_dir $overwrite" >> $joblist_name
done

if [[ $n_files != '' ]]; then
	n_lines=$(wc -l < $joblist_name)
	n_lines_per_file=$(($n_lines / $n_files))
	if [[ $n_lines_per_file -eq 0 ]]; then
		n_lines_per_file=1
	fi
	for filename in "${joblist_name%.*}"_SLICE*; do
		rm $filename
	done
        split -dl $n_lines_per_file --additional-suffix=.sh $joblist_name "${joblist_name%.*}"_SLICE
elif [[ $n_lines_per_file != '' ]]; then
	for filename in "${joblist_name%.*}"_SLICE*; do
		rm $filename
	done
        split -dl $n_lines_per_file --additional-suffix=.sh $joblist_name "${joblist_name%.*}"_SLICE
fi
echo Done 
