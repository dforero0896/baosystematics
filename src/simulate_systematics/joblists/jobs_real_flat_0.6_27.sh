module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.0.dat --data-wt-col=4 --cf-mode=3
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S824062495.flat.sigma0.2.dat --data-wt-col=4 --cf-mode=3
module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.0.dat --data-wt-col=4 --cf-mode=3
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S1790390939.flat.sigma0.2.dat --data-wt-col=4 --cf-mode=3
module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/smooth/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.0.dat --data-wt-col=4 --cf-mode=3
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.R-16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_void_mock_nowt_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gnw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_void_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_xgv_mock_vnw_gw_R-16-50/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/mocks_gal_xyz/CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box5/real/noise/flat_0.6/tpcf_gal_mock/TwoPCF_CATALPTCICz0.638G960S542715479.flat.sigma0.2.dat --data-wt-col=4 --cf-mode=3
