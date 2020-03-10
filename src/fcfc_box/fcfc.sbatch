#!/bin/bash

RUNDIR=/hpcstorage/dforero/projects/baosystematics/src/fcfc_box
JOBLIST=${RUNDIR}/joblist/fcfc_gal_extra-r.sh
${RUNDIR}/fcfc_box.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/nosyst/mocks_gal_xyz_extra /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/nosyst/tpcf_gal_mock extra-r ${RUNDIR}/fcfc_box_count_real.conf /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/box_uniform_random_seed1_0-2500.dat 0
split -d -n 8 ${JOBLIST} realsp

