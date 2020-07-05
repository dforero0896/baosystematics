#!/bin/bash
source ../.env

BOX=1
SPACE=redshift

RR_FILE=${WORKDIR}/patchy_results/randoms/RR_2dbox_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat
IDIR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/radialgauss/tpcf2d_gal_mock_nowt
ODIR=${IDIR}_projected
if [[ ! -e $ODIR ]]; then
mkdir -v $ODIR
fi
for DR in $(ls ${IDIR}/DR_files/DR*)
do
DD=$(echo ${DR} | sed -e "s/DR_/DD_/g")
ONAME=${ODIR}/$(basename ${DD} | sed -e "s/DD_files\///g; s/DD_/TwoPCF_/g")
if [[ ! -e $ONAME ]]; then
python fcfc_2d_counts.py -dd ${DD} -dr ${DR} -rr ${RR_FILE} -o ${ONAME}
fi
done


RR_FILE=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/radialgauss/void_ran/RR_2dvoid_ranR-loc_scaled2.2-loc_scaled5.dat
IDIR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/radialgauss/tpcf2d_void_mock_nowt_R-loc_scaled2.2-loc_scaled5
ODIR=${IDIR}_projected
if [[ ! -e $ODIR ]]; then
mkdir -v $ODIR
fi
for DR in $(ls ${IDIR}/DR_files/DR*)
do
DD=$(echo ${DR} | sed -e "s/DR_/DD_/g")
ONAME=${ODIR}/$(basename ${DD} | sed -e "s/DD_files\///g; s/DD_/TwoPCF_/g")
if [[ ! -e $ONAME ]]; then
python fcfc_2d_counts.py -dd ${DD} -dr ${DR} -rr ${RR_FILE} -o ${ONAME}
fi
done


RR_FILE=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/radialgauss/void_ran/RR_2dvoid_ranR-15.6-50.dat
IDIR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/radialgauss/tpcf2d_void_mock_nowt_R-15.6-50.dat
ODIR=${IDIR}_projected
if [[ ! -e $ODIR ]]; then
mkdir -v $ODIR
fi
for DR in $(ls ${IDIR}/DR_files/DR*)
do
DD=$(echo ${DR} | sed -e "s/DR_/DD_/g")
ONAME=${ODIR}/$(basename ${DD} | sed -e "s/DD_files\///g; s/DD_/TwoPCF_/g")
if [[ ! -e $ONAME ]]; then
python fcfc_2d_counts.py -dd ${DD} -dr ${DR} -rr ${RR_FILE} -o ${ONAME}
fi
done
