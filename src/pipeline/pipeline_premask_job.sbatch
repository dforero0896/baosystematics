#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH --ntasks-per-node=1           # Number of tasks
#SBATCH -J premask_all         # Name of the job
#SBATCH --output=/global/cscratch1/sd/dforero/baosystematics/results/jobout/%x_%a.out 
#SBATCH --error=/global/cscratch1/sd/dforero/baosystematics/results/jobout/%x_%a.err
#SBATCH --array=0-2
#SBATCH -p regular           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G

module add python
if [[ $# -ne 1 ]]; then
	echo ERROR: No ID provided.
	echo USAGE: $0 ID
	exit 1
fi
id=$1
joblist="/global/cscratch1/sd/dforero/baosystematics/src/pipeline/joblists/premask_joblist_$id.sh"
joblist_len=$(wc -l < $joblist)
lines_per_task=$(( $joblist_len / $SLURM_ARRAY_TASK_COUNT ))
start=$(( $SLURM_ARRAY_TASK_ID * $lines_per_task + 1 ))
end=$(( ( $SLURM_ARRAY_TASK_ID + 1 ) * $lines_per_task ))
while read -r comm ; do
	echo Task $SLURM_ARRAY_TASK_ID handling lines $start to $end.
	$comm
done <<< "$(tail -$joblist_len $joblist | head -$end | tail -$lines_per_task)"
