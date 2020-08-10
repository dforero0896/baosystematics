module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1005400.parabola.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_halo_seed_1005400.parabola.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1005400.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=4 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5_wt0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=6 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=2
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1005400.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1005400.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock/TwoPCF_halo_seed_1005400.parabola.sigma0.0.dat --data-wt-col=4 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1005400.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=4 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5_wt0_wt1.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=5 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=6 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=2
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1005400.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1005400.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1005400.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=4 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1005400.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1008900.parabola.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_halo_seed_1008900.parabola.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1008900.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=0 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5_wt0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=6 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=2
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1008900.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz/halo_seed_1008900.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_gal_mock/TwoPCF_halo_seed_1008900.parabola.sigma0.0.dat --data-wt-col=4 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1008900.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=0 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5_wt0_wt1.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.VOID.R-loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=5 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --rand-aux-col=6 --rand-aux-min=2.2 --rand-aux-max=5 --rand-select=23 --cf-mode=2
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1008900.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=0 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_gal_xyz/halo_seed_1008900.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/halo_seed_1008900.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat --data-wt-col=5 --rand-wt-col=4 --data-aux-col=6 --data-aux-min=2.2 --data-aux-max=5 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/DD_files/DD_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_linhalo/box1/real/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-loc_scaled2.2-loc_scaled5/TwoPCF_halo_seed_1008900.parabola.sigma0.0.CROSS.R_loc_scaled2.2-loc_scaled5.dat
