#!/bin/bash
SYSTCASE=allsyst_v7
WORKDIR=/home/epfl/dforero/scratch/projects/baosystematics
INDIR=$WORKDIR/lrg_results/$SYSTCASE/mocks_void_rdz
OUTDIR=$WORKDIR/lrg_results/$SYSTCASE/mocks_void_rdz_finalmask
RUN=$PWD/catalog_mask_lrg_single.sh
JOBLIST=joblist/lrg_joblist.sh
if [[ ! -e $OUTDIR ]];then
mkdir -p -v $OUTDIR
fi
if [[ -e $JOBLIST ]];then
rm -v $JOBLIST
fi
for in_catalog in $(ls -p $INDIR/*)
do
echo "$RUN $in_catalog" >> $JOBLIST
done
