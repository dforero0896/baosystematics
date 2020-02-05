#!/usr/bin/bash
echo Void NOSYST
python chisq_bestfit.py /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_void_mock_R-15.5-50_cbz /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_void/BAOfit_TwoPCF_mockavg_nosyst_v7_void_R-15.5-50_cbz.ascii_best.dat void
echo Void ALLSYST
python chisq_bestfit.py /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_void_mock_R-15.5-50_cbz /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_void/BAOfit_TwoPCF_mockavg_allsyst_v7_void_R-15.5-50_cbz.ascii_best.dat void
echo Gal NOSYST
python chisq_bestfit.py /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_gal_mock_cbz /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_gal/ELG_ALL_bin8_mean_xi0_bestfit.txt gal
echo Gal ALLSYST
python chisq_bestfit.py /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_gal_mock_cbz /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_gal/ELG_ALL_bin8_mean_xi0_bestfit.txt gal
