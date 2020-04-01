==> Using completeness from command line.
==> Using function parabola
==> Using min. completeness 0.8
module load spack/default  gcc/5.4.0 boost
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_gal_obs_nowt/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_gal_obs_nowt/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.VOID.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_void_obs_nowt_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.VOID.R-16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_void_obs_nowt_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_gal_obs/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/smooth/parabola_0.8/tpcf_gal_obs/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.0.dat --data-wt-col=4 --cf-mode=3
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_gal_obs_nowt/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_gal_obs_nowt/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_void_obs_nowt_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.R-16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_void_obs_nowt_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_gal_obs/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/noise/parabola_0.8/tpcf_gal_obs/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384.parabola.sigma0.2.dat --data-wt-col=4 --cf-mode=3

==> Using completeness from command line.
==> Using function parabola
==> Using min. completeness 0.8
module load spack/default  gcc/5.4.0 boost
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_obs_nowt/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_obs_nowt/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_obs_nowt_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.R-16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_void_obs_nowt_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_obs/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/smooth/parabola_0.8/tpcf_gal_obs/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.0.dat --data-wt-col=4 --cf-mode=3
/home/epfl/dforero/scratch/projects/baosystematics/bin/DIVE_box/DIVE_box /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.dat 2500 0 999
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_obs_nowt/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_obs_nowt/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --data-wt-col=0 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_obs_nowt_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.R-16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_void_obs_nowt_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.R-16-50.dat --data-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=3
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=0 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gnw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_void_count_real.conf --rand=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/{cat_type}s_void_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.VOID.dat --count-mode=2 --dr=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat --data-wt-col=0 --rand-wt-col=4 --data-aux-col=4 --data-aux-min=16 --data-aux-max=50 --cf-mode=0 && /home/epfl/dforero/scratch/projects/baosystematics/bin/2pcf.py /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat /hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_xgv_obs_vnw_gw_R-16-50/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.CROSS.R_16-50.dat
srun -n 1 -c 16 /home/epfl/dforero/scratch/projects/baosystematics/bin/FCFC_box/2pcf --conf=/home/epfl/dforero/scratch/projects/baosystematics/src/fcfc_box/fcfc_box_count_real.conf --data=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/obss_gal_xyz/Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --count-mode=1 --dd=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_obs/DD_files/DD_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --output=/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/redshift/noise/parabola_0.8/tpcf_gal_obs/TwoPCF_Box_HAM_z0.465600_nbar3.976980e-04_scat0.2384_zspace.parabola.sigma0.2.dat --data-wt-col=4 --cf-mode=3

