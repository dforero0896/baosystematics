#!/bin/bash

DD_file=$1
#RR_file=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/radialgauss/void_ran/RR_void_ranR-15.6-50.dat 
RR_file=/hpcstorage/dforero/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat
#RR_file=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/radialgauss/void_ran/RR_void_ranR-scaled2.2-50.dat 
ODIR=$2
TPCF_file=$(echo ${DD_file} | sed -e "s/DD_file\///g; s/DD/TwoPCF/g")
#DD_file=$(echo ${DR_file} | sed -e "s/DR_files/DD_files/g; s/DR/DD/g")

echo "~/codes/2pcf.py -dd ${DD_file} -rr ${RR_file} -o ${ODIR}/$(basename ${TPCF_file})"
