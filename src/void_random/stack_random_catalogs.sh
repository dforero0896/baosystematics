#!/bin/bash
if [[ $# -ne 4 ]];
then
	echo "ERROR: Unexpected number of arguments."
	echo "USAGE: bash $0 IN_DIR OUT_FILE KEY N_FILES" 
	echo "KEY=NGC, SGC, ..."
	echo "    Only files with filename containing KEY will be combined"
	exit 1
fi
this_dir="$(dirname $0)" #path from run dir to source dir
in_dir=$1
out_fn=$2
key=$3
PWD=$(pwd)
abs_path=$(echo $pwd/$this_dir) #full path to source so it is reachable from everywhere
[[ "${in_dir}" != */ ]] && in_dir="${in_dir}/"
if [[ -e $out_fn ]];
then
	rm $out_fn
fi
for filename in $(ls $in_dir | grep $key | shuf -n $4); do
	echo $filename
	cat $in_dir$filename >> $out_fn
done
echo "Done, file $out_fn saved"

