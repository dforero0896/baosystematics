#!/usr/bin/bash
if [[ -e ./joblist/trim_joblist.sh ]]; then
rm -v ./joblist/trim_joblist.sh
fi
idir=$1
#idir=/global/cscratch1/sd/dforero/baosystematics/results/allsyst_v7/mocks_void_rdz_addmask/
odir=$2
#odir=/global/cscratch1/sd/dforero/baosystematics/results/allsyst_v7/mocks_void_rdz_finalmask
if [[ ! -e $odir ]]; then
mkdir -v -p $odir
fi
for fname in $(ls -d $idir/*); do
echo "python ../trim_masked_ascii.py $fname $odir 0" >> ./joblist/trim_joblist.sh
done
