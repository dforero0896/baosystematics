#!/usr/bin/bash
TESTFILEFITS=/global/cscratch1/sd/dforero/baosystematics/results/nosyst_v7/mocks_void_rdz_vetomask/superCatalog.MASKED9.fits
TESTFILEASCII=/global/cscratch1/sd/dforero/baosystematics/results/init_test_v7/mocks_gal_rdz/EZ_ELG_clustering_NGC_v7.dat.256.ascii
TESTOUT=/global/cscratch1/sd/dforero/baosystematics/results/init_test_v7/add_mask_test
source activate myenv
/global/cscratch1/sd/dforero/baosystematics/src/mask/additional_mask.py $TESTFILEFITS $TESTOUT
#/global/cscratch1/sd/dforero/baosystematics/src/mask/additional_mask.py $TESTFILEASCII $TESTOUT
