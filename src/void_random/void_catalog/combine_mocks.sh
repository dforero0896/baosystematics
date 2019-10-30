#!/bin/bash


countSGC=0
countNGC=0
path=/home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/mock_void_masked_catalogs/*.ascii
outfileSGC=/home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/void_catalog/mocksCombined100SGC.ascii
outfileNGC=/home/epfl/zhaoc/data/EZmock/eBOSS/ELG/obs/void/void_catalog/mocksCombined100NGC.ascii
if [[ -e $outfile ]]; then
    rm $outfile
fi
for filename in $path; do
    if [[ $filename == *"NGC"* && $countNGC != 100 ]]; then
        cat $filename >> $outfileNGC
	countNGC=$((countNGC+1))
        echo Added $countNGC files to NGC...
    fi
    if [[ $filename == *"SGC"* && $countSGC != 100 ]]; then
        cat $filename >> $outfileSGC
	countSGC=$((countSGC+1))
        echo Added $countSGC files to SGC...
    fi
done

#sort -k3n mocksCombined100.ascii > mocksCombined100SORT.ascii
#rm mocksCombined100.ascii

