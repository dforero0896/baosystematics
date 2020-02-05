#!/bin/bash
#SBATCH --ntasks=1 #tasks are mpi ranks
#SBATCH --ntasks-per-node=1           # Number of tasks
#SBATCH -J diveMock         # Name of the job
#SBATCH --output=/home/epfl/dforero/zhao/void/baosystematics/results/full_v4/diveJob/dive_%j_%x.out 
#SBATCH --error=/home/epfl/dforero/zhao/void/baosystematics/results/full_v4/diveJob/dive_%j_%x.err
####SBATCH --array=0-4
#SBATCH -p p4           # Partition
#SBATCH --mail-user=daniel.forerosanchez@epfl.ch
#SBATCH --mail-type=BEGIN,END,FAIL,ARRAY_TASKS
#SBATCH --cpus-per-task=16
#SBATCH --mem=2G
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
module use /astro/soft/modulefiles/
module unuse /etc/modulefiles
module add astro
module add python/3.7.1
module load spack/default  gcc/5.4.0 boost

srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.126.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.126.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.252.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.252.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.74.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.74.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.213.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.213.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.234.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.234.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.195.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.195.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.468.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.468.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.65.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.65.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.213.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.213.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.252.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.252.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossSGC_v4.dat.234.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossSGC_v4.VOID.dat.234.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.468.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.468.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.126.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.126.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.65.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.65.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.195.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.195.ascii
srun /home/epfl/dforero/zhao/void/baosystematics/bin/DIVE /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mocks_xyz_combined/EZ_ELG_XYZ_clustering_ebossNGC_v4.dat.74.ascii /home/epfl/dforero/zhao/void/baosystematics/results/test_v4/mock_void_catalogs/EZ_ELG_XYZ_clustering_ebossNGC_v4.VOID.dat.74.ascii
