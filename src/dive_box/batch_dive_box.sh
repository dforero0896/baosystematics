#!/bin/bash

for comp in 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00
do

./dive_box.py /hpcstorage/dforero/projects/baosystematics/patchy_results/many_random/comp_${comp}_n3.97698e-04/discrete_tracers /hpcstorage/dforero/projects/baosystematics/patchy_results/many_random/comp_${comp}_n3.97698e-04/voids 2500 && mv -v joblist.sh joblist${comp}.sh

done
