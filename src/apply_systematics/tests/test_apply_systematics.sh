#!/usr/bin/bash
#test_apply_systematics.sh
module load python
WORKDIR=/global/cscratch1/sd/dforero/baosystematics/
COMMAND_A="python $WORKDIR/src/apply_systematics/apply_systematics.py $WORKDIR/data/init_test_v7/mock/EZ_ELG_clustering_NGC_v7.dat.541.fits $WORKDIR/results/init_test_v7/mocks_gal_rdz/EZ_ELG_clustering_NGC_v7.dat.126.ascii NOZ SYSTOT CP"
COMMAND_B="python $WORKDIR/src/apply_systematics/apply_systematics.py $WORKDIR/data/init_test_v7/mock/EZ_ELG_clustering_NGC_v7.dat.541.fits $WORKDIR/results/init_test_v7/mocks_gal_rdz/EZ_ELG_clustering_NGC_v7.dat.126.ascii SYSTOT"
$COMMAND_A
echo #######################################################################
echo $COMMAND_A
$COMMAND_B
echo #######################################################################
echo $COMMAND_B
