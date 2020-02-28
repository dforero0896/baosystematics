#!/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics
indir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/patchy_cmass_subset/box5/real
outdir=/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/patchy_cmass_subset/box5/redshift
redshift=0.638
joblist=./joblist.sh
RUN=$WORKDIR/bin/convert_z/zcnvt
if [[ -e $joblist ]];
then
rm -v $joblist
fi
for iname in $(ls -p $indir/*)
do
bname=$(basename $iname)
oname=$outdir/"${bname%.*}"_zspace.dat
echo "$RUN $iname $oname $redshift" >> $joblist
done
