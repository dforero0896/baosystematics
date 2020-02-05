#!/usr/bin/bash
#test_fcfc.py
module load python
WORKDIR=/global/cscratch1/sd/dforero/baosystematics
python $WORKDIR/src/fcfc/fcfc.py $WORKDIR/results/init_test_v7/mocks_gal_rdz $WORKDIR/results/init_test_v7/tpcf_gal_mock/ init_test_v7 $WORKDIR/src/fcfc/fcfc_mock_gal.conf 1
echo python $WORKDIR/src/fcfc/fcfc.py $WORKDIR/results/$1/mocks_gal_rdz $WORKDIR/results/$1/tpcf_gal_mock/ $1 $WORKDIR/src/fcfc/fcfc_mock_gal.conf 1
