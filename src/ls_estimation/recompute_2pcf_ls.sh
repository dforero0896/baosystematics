#!/bin/bash

DR_file=$1
RR_file=/hpcstorage/dforero/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat
ODIR=$2
TPCF_file=$(echo ${DR_file} | sed -e "s/DR_file\///g; s/DR/TwoPCF/g")
DD_file=$(echo ${DR_file} | sed -e "s/DR_files/DD_files/g; s/DR/DD/g")

echo "~/codes/2pcf.py -dd ${DD_file} -dr ${DR_file} -rr ${RR_file} -o ${ODIR}/$(basename ${TPCF_file})"
