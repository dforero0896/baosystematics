/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.R-15.6-50.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/RR_void_ran_wt0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.R-15.6-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --rand-aux-col=4 --rand-aux-min=15.6 --rand-aux-max=50 --rand-select=23 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.R-15.6-50.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/RR_void_ran_wt0_wt1.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.R-15.6-50.dat --data-wt-col=5 --rand-wt-col=5 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --rand-aux-col=4 --rand-aux-min=15.6 --rand-aux-max=50 --rand-select=23 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --data-wt-col=5 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat --data-wt-col=5 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.0.CROSS.R_15.6-50.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat 2500 0 999
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.R-15.6-50.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/RR_void_ran_wt0_wt1_wt0.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.R-15.6-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --rand-aux-col=4 --rand-aux-min=15.6 --rand-aux-max=50 --rand-select=23 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/void_ran.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.R-15.6-50.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/void_ran/RR_void_ran_wt0_wt1_wt0_wt1.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.R-15.6-50.dat --data-wt-col=5 --rand-wt-col=5 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --rand-aux-col=4 --rand-aux-min=15.6 --rand-aux-max=50 --rand-select=23 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --data-wt-col=5 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz_wt_scaledR/CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat --data-wt-col=5 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=15.6 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py -dd /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/DD_files/DD_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat -o /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vw_gw_R-15.6-50/TwoPCF_CATALPTCICz0.466G960S231824037_zspace.parabola.sigma0.2.CROSS.R_15.6-50.dat
