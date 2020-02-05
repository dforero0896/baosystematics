#!/usr/bin/bash
if [[ $# -ne 2 ]]; then
echo $0 OVERWRITE_GAL OVERWRITE_VOID
exit 1
fi
overwrite_gal=$1
overwrite_void=$2
if [[ $overwrite_gal -eq 1 ]]; then
rm -v /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_gal/*
fi
echo Gal NOSYST
python baofit.py /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_gal_mock_cbz/ /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_gal_mock_avg/ELG_ALL_bin8_mean_xi0.dat /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_gal/ gal


if [[ $overwrite_gal -eq 1 ]]; then
rm -v /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_gal/*
fi
echo Gal ALLSYST
python baofit.py /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_gal_mock_cbz/ /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_gal_mock_avg/ELG_ALL_bin8_mean_xi0.dat /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_gal/ gal


if [[ $overwrite_void -eq 1 ]]; then
rm -v /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_void/*
fi
echo Void ALLSYST
python baofit_void.py /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_void_mock_R-15.5-50 /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/tpcf_void_mock_R-15.5-50_avg/TwoPCF_mockavg_allsyst_v7_void_R-15.5-50_cbz.ascii /hpcstorage/dforero/projects/baosystematics/results/allsyst_v7/baofit/avg_combined_void/ void


if [[ $overwrite_void -eq 1 ]]; then
rm -v /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_void/*
fi
echo Void NOSYST
python baofit_void.py /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_void_mock_R-15.5-50 /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/tpcf_void_mock_R-15.5-50_avg/TwoPCF_mockavg_nosyst_v7_void_R-15.5-50_cbz.ascii /hpcstorage/dforero/projects/baosystematics/results/nosyst_v7/baofit/avg_combined_void/ void

