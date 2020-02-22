#!/bin/bash

WORKDIR=/hpcstorage/dforero/projects/baosystematics
ALLSYST=$WORKDIR/lrg_results/allsyst_v7/mocks_gal_rdz
NOSYST=$WORKDIR/lrg_results/nosyst_v7/mocks_gal_rdz
if [[ ! -e $NOSYST ]];then
mkdir -p -v $NOSYST
fi
if [[ -e joblist.sh ]];then
rm -v joblist.sh
fi
for catalog in $(ls -d $ALLSYST/* | grep "\.dat\.")
do
catname=$(basename $catalog)
echo "python shuffle_comp_weights.py $catalog $NOSYST/$catname" >> joblist.sh
done
