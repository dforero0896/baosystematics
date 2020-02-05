#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH --ntasks-per-node=1           # Number of tasks
#SBATCH -J premask_all         # Name of the job
#SBATCH --output=/global/cscratch1/sd/dforero/baosystematics/results/jobout/%x_%a.out 
#SBATCH --error=/global/cscratch1/sd/dforero/baosystematics/results/jobout/%x_%a.err
#SBATCH -q regular           # Partition
#SBATCH -C haswell
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=50
#SBATCH --mem=48G

module add python
if [[ $# -ne 3 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 ID INITIAL_SLICE END_SLICE
	exit 1
fi
id=$1
init_slice=$2
end_slice=$3
joblist="/global/cscratch1/sd/dforero/baosystematics/src/pipeline/joblists/premask_joblist_$id.sh"
bash /global/cscratch1/sd/dforero/baosystematics/src/pipeline/omprun_slices.sh /global/cscratch1/sd/dforero/baosystematics/src/pipeline/joblists/premask_joblist_$id $init_slice $end_slice

