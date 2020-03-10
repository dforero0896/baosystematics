#!/bin/bash
RUN=./run_box.sh
#catalog=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091.dat
catalog=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091_zspace.dat
$RUN $catalog
