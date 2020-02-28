#!/bin/bash
#build_joblist.sh
WORKDIR=/hpcstorage/dforero/projects/baosystematics
if [[ $# -eq 4 ]]; then
	raw_dir=$1
	[[ "${raw_dir}" == */ ]] && raw_dir="${raw_dir: : -1}"
	results_dir=$2
	[[ "${results_dir}" == */ ]] && results_dir="${results_dir: : -1}"
	tracer=$3
	overwrite=$4
else
	echo "ERROR: Unxepected number of arguments."
	echo "USAGE: bash $0 RAW_DIR RESULTS_DIR TRACER OVERWRITE"
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
	#exit 1
fi

if [[ -e $joblist_name ]]; then
	rm -v $joblist_name
fi
echo Writing $joblist_name
echo Overwriting = $overwrite
for filename in $raw_dir/*NGC*.dat.*; do
	echo "bash ${WORKDIR}/src/pipeline/pipeline_file_wsys.sh $filename $results_dir $tracer $overwrite " >> $joblist_name
	sgc_comp=$raw_dir/$(basename $filename | sed -e "s/NGC/SGC/g")
	echo "bash ${WORKDIR}/src/pipeline/pipeline_file_wsys.sh $sgc_comp $results_dir $tracer $overwrite " >> $joblist_name
done
echo Done 
