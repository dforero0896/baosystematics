#!/bin/bash
rm -v joblistallcomps.sh
source ../.env
for comp in 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 #1.00
do

./dive_box.py ${WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_${comp}/mocks_gal_xyz ${WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_${comp}/mocks_void_xyz 2500 && cat joblist.sh >> joblistallcomps.sh

done
