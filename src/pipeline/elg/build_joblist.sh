#!/bin/bash
#build_joblist.sh
if [[ $# -gt 5 ]] && [[ $# -lt 9 ]]; then
	raw_dir=$1
	[[ "${raw_dir}" == */ ]] && raw_dir="${raw_dir: : -1}"
	results_dir=$2
	[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}"
	overwrite=$3
	splitmode=$4
	if [[ $splitmode -eq 1 ]]; then
		n_files=$5
		echo "Splitting in $n_files job lists"
	elif [[ $splitmode -eq 2 ]]; then
		n_lines_per_file=$5
		echo "Splitting in joblists with $n_lines_per_file lines per file"
	elif [[ $splitmode -eq 0 ]]; then
		echo "Not splitting."
	else
		echo "ERROR: Split mode not understood."
		echo "Choose SPLIT_MODE = 0 (no splitting)"
		echo "Choose SPLIT_MODE = 1 (split in N files)"
		echo "Choose SPLIT_MODE = 2 (split in files with N lines)"
	fi
	sys_effect_1=$6
	sys_effect_2=$7
	sys_effect_3=$8
	sys_effects="SYSTOT NOZ CP NONE"
	for sys_input in $sys_effect_1 $sys_effect_2 $sys_effect_3; do
		counter=0
		for seffect in $sys_effects; do
			if [[ "${sys_input}" == "${seffect}" ]]; then
				break
			elif [[ "${sys_input}" != '' ]]; then
				counter=$(( $counter + 1 ))
			fi
		done
		if [[ $counter -gt 3 ]]; then
			echo "ERROR: Unvalid systematic effects: $sys_input."
			echo "Choose SYS_EFFECT = SYSTOT, NOZ, CP, NONE."
			exit 1
		fi
	done
else
	echo "ERROR: Unxepected number of arguments."
	echo "USAGE: bash $0 RAW_DIR RESULTS_DIR OVERWRITE SPLIT_MODE N SYS_EFFECT [SYS_EFFECT SYS_EFFECT]"
	exit 1
fi
id=$(basename $results_dir)
this_dir=$(dirname $0)
[[ "${this_dir}" == */ ]] && this_dir="${this_dir: : -1}"
if [[ ! -e $this_dir/joblists ]]; then
	mkdir -p -v $this_dir/joblists
fi
joblist_name=$this_dir/"joblists/premask_joblist_$(echo $id).sh"
if [[ ! -e $raw_dir ]]; then
	echo ERROR: Input directory not found.
	exit 1
fi

if [[ -e $joblist_name ]]; then
	rm -v $joblist_name
fi
echo Writing $joblist_name
echo Overwriting = $overwrite
for filename in $raw_dir/*NGC*.dat.*; do
	echo "bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/pipeline_file.sh $filename $results_dir $overwrite $sys_effect_1 $sys_effect_2 $sys_effect_3" >> $joblist_name
done
for filename in $raw_dir/*SGC*.dat.*; do
	echo "bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/pipeline_file.sh $filename $results_dir $overwrite $sys_effect_1 $sys_effect_2 $sys_effect_3" >> $joblist_name
done

if [[ $n_files != '' ]]; then
	n_lines=$(wc -l < $joblist_name)
	n_lines_per_file=$(($n_lines / $n_files))
	if [[ $n_lines_per_file -eq 0 ]]; then
		n_lines_per_file=1
	fi
	for filename in "${joblist_name%.*}"_SLICE*; do
		rm -v $filename
	done
        split -dl $n_lines_per_file --additional-suffix=.sh $joblist_name "${joblist_name%.*}"_SLICE
elif [[ $n_lines_per_file != '' ]]; then
	for filename in "${joblist_name%.*}"_SLICE*; do
		rm -v $filename
	done
        split -dl $n_lines_per_file --additional-suffix=.sh $joblist_name "${joblist_name%.*}"_SLICE
fi
echo Done 
