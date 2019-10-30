#!/usr/bin/env bash
this_dir=$(dirname $0)"/../"
res_orig=$this_dir"results/full_v4/"
#find $res_orig -type d | sed -e "s/full_v4/$1/g"
for d in $(find $res_orig -type d | sed -e "s/full_v4/$1/g"); do
	if [[ ! -e $d ]]; then
		mkdir $d
	fi
done

