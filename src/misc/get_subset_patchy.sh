#!/bin/bash
list=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/used_patchy.dat
N_mocks=100
BOX=2
mockdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/PATCHY_CMASS/box${BOX}
subsetdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/patchy_cmass_subset/box${BOX}/real
mkdir -p -v $subsetdir
echo "Found $(wc -l $list)"
for ran in $(cat $list | head -${N_mocks})
do
filename=$(ls -d $mockdir/* | grep $ran)
echo $filename
cp $filename $subsetdir
fn_here=$subsetdir/$(basename $filename)
bunzip2 $fn_here
done
rm -v $subsetdir/*bz2*

