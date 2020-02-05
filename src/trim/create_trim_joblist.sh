#!/usr/bin/bash
if [[ -e ./joblist/trim_joblist.sh ]]; then
rm -v ./joblist/trim_joblist.sh
fi

for fname in $(ls -d /global/cscratch1/sd/dforero/baosystematics/results/allsyst_v7/mocks_void_rdz_addmask/*); do
echo "python ../trim_masked_ascii.py $fname /global/cscratch1/sd/dforero/baosystematics/results/allsyst_v7/mocks_void_rdz_finalmask 0" >> ./joblist/trim_joblist.sh
done
