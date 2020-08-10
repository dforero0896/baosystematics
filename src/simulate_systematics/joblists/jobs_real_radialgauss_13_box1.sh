module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_gal_xyz/halo_seed_1001300.radialgauss.sigma0.235.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_void_xyz/halo_seed_1001300.radialgauss.sigma0.235.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_gal_xyz/halo_seed_1001300.radialgauss.sigma0.235.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --count-mode=2 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/DD_files/DD_halo_seed_1001300.radialgauss.sigma0.235.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/DR_files/DR_halo_seed_1001300.radialgauss.sigma0.235.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/TwoPCF_halo_seed_1001300.radialgauss.sigma0.235.dat --data-wt-col=0 --cf-mode=1
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_void_xyz_scaledR/halo_seed_1001300.radialgauss.sigma0.235.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/void_ran/void_ran.dat --count-mode=5 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1001300.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DR_files/DR_halo_seed_1001300.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1001300.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --data-aux-col=5 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=5 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=1
module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_gal_xyz/halo_seed_1004500.radialgauss.sigma0.235.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_void_xyz/halo_seed_1004500.radialgauss.sigma0.235.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_gal_xyz/halo_seed_1004500.radialgauss.sigma0.235.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --count-mode=2 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/DD_files/DD_halo_seed_1004500.radialgauss.sigma0.235.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/DR_files/DR_halo_seed_1004500.radialgauss.sigma0.235.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_gal_mock_nowt/TwoPCF_halo_seed_1004500.radialgauss.sigma0.235.dat --data-wt-col=0 --cf-mode=1
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/mocks_void_xyz_scaledR/halo_seed_1004500.radialgauss.sigma0.235.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/void_ran/void_ran.dat --count-mode=2 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1004500.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DR_files/DR_halo_seed_1004500.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1004500.radialgauss.sigma0.235.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --data-aux-col=5 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=5 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=1
