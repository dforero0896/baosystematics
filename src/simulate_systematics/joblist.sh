/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.R-18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.R-18-20.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=3
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_mock/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.R-18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.R-18-20.dat --data-wt-col=5 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=3
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --data-wt-col=5 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/mocks_void_xyz_wt/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat --data-wt-col=5 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_mock_vw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.0.CROSS.R_18-20.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.VOID.dat --count-mode=1 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_nowt_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.VOID.R-18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_mock_nowt_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.VOID.R-18-20.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=3
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gnw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat
srun -n 1 -c 32 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_gal_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/mocks_void_xyz/CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=18 --data-aux-max=20 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_mock_vnw_gw_R-18-20/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.CROSS.R_18-20.dat
/home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock/DD_files/DD_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat /home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_mock/TwoPCF_CATALPTCICz0.466G960S378695801_zspace.parabola.sigma0.2.dat
ICz0.466G960S1484324254_zspace.parabola.sigma0.2.dat
