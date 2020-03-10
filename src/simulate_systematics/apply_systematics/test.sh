#!/bin/bash
WORKDIR=/hpcstorage/dforero/projects/baosystematics/src/simulate_systematics
RUN=$WORKDIR/apply_systematics/apply_systematics
CATALOG=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091.dat
SEED=1
OUTPUT_BASE=$(basename ${CATALOG} | sed -e "s/\.dat//g")
VETO_MASK=$WORKDIR/masks/vetomask_s42_nbar3.9770e-04.dat
ANG_MASK=$WORKDIR/masks/angmask_half_s2_nbar3.9770e-04.dat
SAVE=2
SUFFIX="test"
#time $(dirname $RUN)/../mask_comp_func.py $CATALOG $OUTPUT_BASE
time $RUN $CATALOG $SEED $OUTPUT_BASE $VETO_MASK $ANG_MASK $SAVE $SUFFIX
