#!/usr/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics #/global/cscratch1/sd/dforero/baosystematics
if [[ $# -ne 6 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 IN_FILE OUT_DIR R_MIN R_MAX DELIMITER OVERWRITE
	exit 1
fi
infile=$1
outdir=$2
infn=$(basename -- "$infile")
inext="${infn##*.}"
inbase="${infn%.*}"
if [[ ! -e $outdir ]]; then
	mkdir -v -p $outdir
fi
r_min=$3
r_max=$4
delimiter=$5
overwrite=$6
outname=$outdir/"$inbase"_R-$r_min-$r_max"."$inext
if [[ $overwrite -eq 1 ]] || [[ ! -e $outname ]]; then
echo Selecting objects with R in \[$r_min, $r_max\].
echo $outname
awk -v rmin="$r_min" -v rmax="$r_max" -F"$delimiter" '($4*1) > rmin && ($4*1) < rmax' $infile | shuf > $outname
fi
