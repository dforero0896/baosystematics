#!/bin/bash
rm -v joblistallcomps.sh
for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 #1.00
do

./dive_box.py /hpcstorage/dforero/projects/baosystematics/patchy_recon_nods/box1/redshift/smooth/flat_${comp}/mocks_gal_xyz /hpcstorage/dforero/projects/baosystematics/patchy_recon_nods/box1/redshift/smooth/flat_${comp}/mocks_void_xyz 2500 && cat joblist.sh >> joblistallcomps.sh

done
