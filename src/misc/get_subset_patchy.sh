#!/bin/bash
list=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/used_patchy.dat
N_mocks=500
BOX=5
mockdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/PATCHY_CMASS/box${BOX}
subsetdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/patchy_cmass_subset/box${BOX}/real
mkdir -p -v $subsetdir
echo "Found $(wc -l $list)"
for ran in $(cat $list | head -${N_mocks})
do
filename=$(ls -d $mockdir/* | grep $ran)
#echo $filename
fn_here=$subsetdir/$(basename $filename)
if [[ ! -e $(echo ${fn_here} | sed -e "s/\.bz2//g") ]]
then
echo ${fn_here} | sed -e "s/\.bz2//g"
cp $filename $subsetdir
bunzip2 -v $fn_here
fi
done
rm -v $subsetdir/*bz2*

