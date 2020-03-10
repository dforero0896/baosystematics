#!/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics
indir=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/nosyst/mocks_gal_xyz
outdir=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/redshift/nosyst/mocks_gal_xyz
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
if [[ -f $oname ]];
then
continue
fi
echo "$RUN $iname $oname $redshift" >> $joblist
done
