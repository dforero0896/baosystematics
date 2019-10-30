#!/bin/bash

count=0
path=/home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/void_catalog/binned_catalogs_R/*.ascii
outfile=/home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/void_catalog/binned_catalogs_L/
if [ -e BIG_VOID_RAN_CATALOG.ascii ]; then
    rm BIG_VOID_RAN_CATALOG.ascii
fi
for filename in $path; do
    shuf -o $filename $filename
    paste $outfile$(basename $filename) $filename >> BIG_VOID_RAN_CATALOG.ascii
    
done

#sort -k3n mocksCombined100.ascii > mocksCombined100SORT.ascii
#rm mocksCombined100.ascii

