#!/bin/bash
ls ../../patchy_results/box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/DR_files/* | xargs -I'{}' bash recompute_2pcf_ls.sh {} ../../patchy_results/box1/redshift/radialgauss/void_ran/RR_void_ranR-loc_scaled2.2-loc_scaled5.dat ../../patchy_results/box1/redshift/radialgauss/tpcf_void_mock_nowt_R-loc_scaled2.2-loc_scaled5/ | bash
