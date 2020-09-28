#!/bin/bash

source ../.env

DIR=${WORKDIR}/patchy_recon

for box in 1
do
for space in redshift
do
COMPDIR=${DIR}/box${box}/${space}/smooth/flat_*
for comp in $(ls -d ${COMPDIR})
do
echo ${comp}
ls ${comp}/mocks_void_xyz | wc -l
for rsc in $(ls -d ${comp}/tpcf_void_mock_nowt_R-scaled*)
do
echo ${rsc}
ls ${rsc} | wc -l
done
done
done
done

