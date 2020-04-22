#!/bin/bash

partition=${1:-p5}
ncores=16
for box in 1 5
do
for space in real redshift
do
echo sbatch -J ${box}${space} -p ${partition} -n 1 -c ${ncores} --array=0-31 --wrap=\'bash joblists/jobs_${space}_radialgauss_'${SLURM_ARRAY_TASK_ID}'_box${box}.sh\'
done
done
