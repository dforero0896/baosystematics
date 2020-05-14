#!/bin/bash

echo \#\# Radial

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*| sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*VOID/.VOID/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T* | sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*$/.VOID.R-2.2-5.dat/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/radialgauss/plots/snr_analysis.dat' | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*| sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*VOID/.VOID/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T* | sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*$/.VOID.R-2.2-5.dat/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/radialgauss/plots/snr_analysis.dat' | sed -e "s/redshift/real/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*| sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*VOID/.VOID/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T* | sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*$/.VOID.R-2.2-5.dat/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/radialgauss/plots/snr_analysis.dat' | sed -e "s/redshift/real/g; s/box1/box5/g ; s/15\.6/18.5/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*| sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*VOID/.VOID/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T* | sed -e "s/\/radialgauss\//\/nosyst\//g; s/\.radialgauss.*$/.VOID.R-2.2-5.dat/g") <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/radialgauss/plots/snr_analysis.dat' | sed -e "s/box1/box5/g ; s/15\.6/18.5/g" | bash

echo \#\# Angular

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-scaled2.2-50/T*)  <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/T*)| tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis.dat " | bash

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-scaled2.2-50/T*)  <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis.dat " | sed -e "s/redshift/real/g" | bash


echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-scaled2.2-50/T*)  <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis.dat " | sed -e "s/redshift/real/g; s/box1/box5/g; s/15\.6/18.5/g" | bash


echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-15.6-50/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-scaled2.2-50/T*)  <(ls box1/redshift/smooth/parabola_0.8/tpcf_void_mock_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis.dat " | sed -e "s/box1/box5/g; s/15\.6/18.5/g" | bash

echo \#\# Random

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis.dat " | bash

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis.dat " | sed -e "s/redshift/real/g" | bash

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis.dat "  | sed -e "s/redshift/real/g; s/box1/box5/g; s/15\.6/18.5/g" | bash

echo "../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/nosyst/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-15.6-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-scaled2.2-50/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis.dat "  | sed -e "s/box1/box5/g; s/15\.6/18.5/g" | bash

echo GALAXIES



echo \#\# Radial

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/radialgauss/tpcf_gal_mock_nowt/T*) | tee box1/redshift/radialgauss/plots/snr_analysis_gal.dat' | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/radialgauss/tpcf_gal_mock_nowt/T*) | tee box1/redshift/radialgauss/plots/snr_analysis_gal.dat' | sed -e "s/redshift/real/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/radialgauss/tpcf_gal_mock_nowt/T*) | tee box1/redshift/radialgauss/plots/snr_analysis_gal.dat' | sed -e "s/redshift/real/g; s/box1/box5/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/radialgauss/tpcf_gal_mock_nowt/T*) | tee box1/redshift/radialgauss/plots/snr_analysis_gal.dat' | sed -e "s/box1/box5/g" | bash

echo \#\# Angular

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis_gal.dat ' | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis_gal.dat ' | sed -e "s/redshift/real/g" | bash


echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis_gal.dat ' | sed -e "s/redshift/real/g; s/box1/box5/g" | bash


echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/smooth/parabola_0.8/tpcf_gal_mock_nowt/T*) | tee box1/redshift/smooth/parabola_0.8/plots/snr_analysis_gal.dat ' | sed -e "s/box1/box5/g" | bash

echo \#\# Random

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_gal_mock_nowt/T*)| tee box1/redshift/noise/flat_1.0/plots/snr_analysis_gal.dat ' | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_gal_mock_nowt/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis_gal.dat ' | sed -e "s/redshift/real/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_gal_mock_nowt/T*)| tee box1/redshift/noise/flat_1.0/plots/snr_analysis_gal.dat '  | sed -e "s/redshift/real/g; s/box1/box5/g" | bash

echo '../src/void_radius_cut/signal_to_noise.py <(ls box1/redshift/nosyst/tpcf_gal_mock/T*) <(ls box1/redshift/noise/flat_1.0/tpcf_gal_mock_nowt/T*) | tee box1/redshift/noise/flat_1.0/plots/snr_analysis_gal.dat '  | sed -e "s/box1/box5/g" | bash
