#!/bin/bash
list=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/used_patchy.dat
mockdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/PATCHY_CMASS/box5
subsetdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/patchy_cmass_subset/box5/real
mkdir -p -v $subsetdir
echo "Found $(wc -l $list)"
for ran in $(cat $list)
do
filename=$(ls -d $mockdir/* | grep $ran)
echo $filename
cp $filename $subsetdir
fn_here=$subsetdir/$(basename $filename)
bunzip2 $fn_here
done
rm -v $subsetdir/*bz2*

