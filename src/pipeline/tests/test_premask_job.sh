#!/usr/bin/bash
bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/build_joblist.sh /global/cscratch1/sd/dforero/baosystematics/data/init_test_v7/mock/ /global/cscratch1/sd/dforero/baosystematics/results/init_test_v7/ 1 2 50 SYSTOT
#sbatch -C haswell --array=0-2 --time=3:00:00 --job-name=t_premask /global/cscratch1/sd/dforero/baosystematics/src/pipeline/pipeline_premask_job.sbatch init_test_v7
