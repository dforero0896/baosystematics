#!/usr/bin/bash
#omprun_slices.sh
joblist_basename=$1
id_init=$2
id_end=$3
for i in $(seq -f "%02g" $id_init $id_end)
do
	echo "Processing job list $joblist_basename""_SLICE$i.sh"
	/global/cscratch1/sd/dforero/baosystematics/bin/OMPrun $(echo $joblist_basename)_SLICE$i.sh	
done
