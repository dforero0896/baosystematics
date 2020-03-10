#!/bin/bash
WORKDIR=/home/epfl/dforero/scratch/projects/baosystematics
RESULTS=$WORKDIR/patchy_results
SPACE=redshift
BOX=box1
SEED=1
ANG_MASK=$WORKDIR/src/simulate_systematics/masks/angmask_half_s2_nbar3.9770e-04.dat
ANG_MASK_RANDOM=$WORKDIR/src/simulate_systematics/masks/angmask_half_s2_nbar3.9770e-04.dat # w/o random noise
VETO_MASK=$WORKDIR/src/simulate_systematics/masks/vetomask_s42_nbar3.9770e-04.dat
catalog=$1
mocks_gal_xyz=$(dirname $catalog)

# Mask
SUFFIX="egg_cart_noise"
GAL_MASK_DIR=$RESULTS/$BOX/$SPACE/masked/mocks_gal_xyz
VETO_DIR=$RESULTS/$BOX/$SPACE/veto
mkdir -v -p $VETO_DIR
ANG_DIR=$RESULTS/$BOX/$SPACE/ang
mkdir -v -p $ANG_DIR
VETOANG_DIR=$RESULTS/$BOX/$SPACE/vetoang
mkdir -v -p $VETOANG_DIR

#MASK_RUN=$WORKDIR/bin/apply_systematics
MASK_RUN=$WORKDIR/src/simulate_systematics/mask_comp_func.py
GAL_OMASK=$GAL_MASK_DIR/$(basename $catalog | sed -e "s/\.dat//g")
VETO_GAL=$VETO_DIR/mocks_gal_xyz/$(basename ${GAL_OMASK}).VETO.${SUFFIX}.dat
ANG_GAL=$ANG_DIR/mocks_gal_xyz/$(basename ${GAL_OMASK}).ANG.${SUFFIX}.dat
VETOANG_GAL=$VETOANG_DIR/mocks_gal_xyz/$(basename ${GAL_OMASK}).VETO_ANG.${SUFFIX}.dat

if [[ ! -f ${GAL_OMASK}.VETO.${SUFFIX}.dat || ! -f ${GAL_OMASK}.ANG.${SUFFIX}.dat || ! -f ${GAL_OMASK}.VETO_ANG.${SUFFIX}.dat ]] & [[ ! -f $VETO_GAL || ! -f $ANG_GAL || ! -f $VETOANG_GAL ]]; then
#$MASK_RUN $catalog $SEED $GAL_OMASK $VETO_MASK $ANG_MASK 4 ${SUFFIX}
time $MASK_RUN $catalog $GAL_OMASK ${SUFFIX} 1
fi
mkdir -v -p $VETO_DIR/mocks_gal_xyz
mkdir -v -p $ANG_DIR/mocks_gal_xyz
mkdir -v -p $VETOANG_DIR/mocks_gal_xyz

mv -v ${GAL_OMASK}.VETO.${SUFFIX}.dat $VETO_DIR/mocks_gal_xyz
mv -v ${GAL_OMASK}.ANG.${SUFFIX}.dat $ANG_DIR/mocks_gal_xyz
mv -v ${GAL_OMASK}.VETO_ANG.${SUFFIX}.dat $VETOANG_DIR/mocks_gal_xyz
RAN_CAT=$WORKDIR/patchy_results/randoms/box_uniform_random_seed1_0-2500_SMALL
if [[ ! -e ${RAN_CAT}.VETO.${SUFFIX}.dat || ! -e ${RAN_CAT}.ANG.${SUFFIX}.dat || ! -e ${RAN_CAT}.VETO_ANG.${SUFFIX}.dat ]];then
#$MASK_RUN ${RAN_CAT}.dat $SEED $RAN_CAT $VETO_MASK $ANG_MASK_RANDOM 4 ${SUFFIX}
time $MASK_RUN ${RAN_CAT}.dat ${RAN_CAT} ${SUFFIX} 0
fi

#FCFC Gal
FCFC_LIST_RUN=$WORKDIR/src/fcfc_box
export OMP_NUM_THREADS=32
$FCFC_LIST_RUN/fcfc_box.py ${ANG_DIR}/mocks_gal_xyz ${ANG_DIR}/tpcf_gal_mock_nowt ang  $FCFC_LIST_RUN/fcfc_box_count_${SPACE}.conf ${RAN_CAT}.ANG.${SUFFIX}.dat 0
FCFC_CMD=$(grep $(basename $ANG_GAL) $FCFC_LIST_RUN/joblist/fcfc_gal_ang.sh)
$FCFC_CMD

#$FCFC_LIST_RUN/fcfc_box.py ${VETO_DIR}/mocks_gal_xyz ${VETO_DIR}/tpcf_gal_mock_nowt veto  $FCFC_LIST_RUN/fcfc_box_count_${SPACE}.conf ${RAN_CAT}.VETO.${SUFFIX}.dat 0
#FCFC_CMD=$(grep $(basename $VETO_GAL) $FCFC_LIST_RUN/joblist/fcfc_gal_veto.sh)
#$FCFC_CMD

#$FCFC_LIST_RUN/fcfc_box.py ${VETOANG_DIR}/mocks_gal_xyz ${VETOANG_DIR}/tpcf_gal_mock_nowt vetoang  $FCFC_LIST_RUN/fcfc_box_count_${SPACE}.conf ${RAN_CAT}.VETO_ANG.${SUFFIX}.dat 0
#FCFC_CMD=$(grep $(basename $VETOANG_GAL) $FCFC_LIST_RUN/joblist/fcfc_gal_vetoang.sh)
#$FCFC_CMD

