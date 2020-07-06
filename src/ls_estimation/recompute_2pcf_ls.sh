#!/bin/bash

DR_file=$1
RR_file=$2 #/hpcstorage/dforero/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat
ODIR=$3
if [[ $# -ne 3 ]]; then
echo ERROR: use $0 DR_FILE RR_FILE ODIR
exit 1
fi
TPCF_file=$(echo ${DR_file} | sed -e "s/DR_file\///g; s/DR/TwoPCF/g")
DD_file=$(echo ${DR_file} | sed -e "s/DR_files/DD_files/g; s/DR/DD/g")
OFILE=${ODIR}/$(basename ${TPCF_file})
if [[ -e $OFILE ]]; then
echo "Exists"
#exit 0

fi
echo "~/codes/2pcf.py -dd ${DD_file} -dr ${DR_file} -rr ${RR_file} -o ${OFILE}"
