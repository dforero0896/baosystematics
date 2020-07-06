srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/mocks_gal_xyz/CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --count-mode=2 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_gal_mock_nowt/DD_files/DD_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_gal_mock_nowt/DR_files/DR_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_gal_mock_nowt/TwoPCF_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.dat --data-wt-col=0 --cf-mode=0
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/mocks_void_xyz/CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.VOID.dat --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/void_ran/void_ran.dat --count-mode=2 --dd=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/DD_files/DD_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.VOID.R-scaled2.2-50.dat --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/DR_files/DR_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.VOID.R-scaled2.2-50.dat --rr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/void_ran/RR_void_ranR-scaled2.2-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/TwoPCF_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.VOID.R-scaled2.2-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=17.93 --data-aux-max=50 --rand-aux-col=4 --rand-aux-min=17.93 --rand-aux-max=50 --rand-select=23 --cf-mode=0
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_redshift.conf --rand=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/mocks_gal_xyz/CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.dat --data=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/mocks_void_xyz/CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.VOID.dat --count-mode=2 --dr=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_xgv_mock_vnw_gnw_R-scaled2.2-50/DD_files/DD_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.CROSS.R_scaled2.2-50.dat --output=/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/redshift/radialgauss/tpcf_xgv_mock_vnw_gnw_R-scaled2.2-50/TwoPCF_CATALPTCICz0.466G960S494614559_zspace.radialgauss.sigma0.235.CROSS.R_scaled2.2-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=17.93 --data-aux-max=50 --cf-mode=0
