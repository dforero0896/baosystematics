#!/usr/bin/env python
import numpy as np
import pandas as pd
from astropy.stats import jackknife_resampling
from astropy.stats import jackknife_stats
import sys
import os
#import matplotlib.pyplot as plt
def read_inlist(inlist_fn):
    inlist=[]
    with open(inlist_fn, 'r') as f:
        no_strip=f.readlines()
    [inlist.append(s.strip()) for s in no_strip]
    return inlist
def signal_to_noise_ratio(arr):
    return np.mean(arr)/np.std(arr)
def snr_constant_noise(arr, confidence_level=0.95):
    snr = arr/np.std(arr)
    mean_snr = np.mean(snr)
    std_err = np.std(snr)/np.sqrt(snr.shape[0])
    from scipy.special import erfinv
    estimate = mean_snr
    z_score = np.sqrt(2.0)*erfinv(confidence_level)
    conf_interval = estimate + z_score*np.array((-std_err, std_err))
    return estimate, 0, std_err, conf_interval
if __name__ == '__main__':
    if len(sys.argv)<2:
        sys.exit('ERROR: Unexpecte number of arguments.\nUSAGE: %s INPUT_FILE_LIST_1 [...INPUT_FILE_LIST_N]\n'%sys.argv[0])

    ilists_fn = sys.argv[1:]
    s_bao = 102.5
    s_dl_1 = 82.5
    s_dl_2 = 87.5
    s_dr_1 = 117.5
    s_dr_2 = 122.5
    s_vals = [s_bao, s_dl_1, s_dl_2, s_dr_1, s_dr_2]
    print(f"# SNR\tbias\tstderr\tconf_int_low\tconf_int_high\tsamples_dir\tn_samples")
    for ilist_fn in ilists_fn:
        ilist = read_inlist(ilist_fn)
        if len(ilist)<1: continue
        signal_arr=[]
        for ifile in ilist:
            ipath = ifile
            iarr = pd.read_csv(ipath, delim_whitespace=True, engine='c').values#np.loadtxt(ipath)
            if any((iarr[:,0]**2*iarr[:,1])[-2:]>5e2): continue
            s = iarr[:,0]
            xi = iarr[:,1]
            s_vals_id = np.array([np.where(s==val)[0] for val in s_vals])
            xi_vals = xi[s_vals_id]
            signal_arr.append(xi_vals[0] - np.mean(xi_vals[1:]))
        #signal_resamples = jackknife_resampling(signal_arr)
        signal_arr = np.array(signal_arr)
        SNR, bias, stderr, conf_interval = jackknife_stats(signal_arr, signal_to_noise_ratio, 0.95)
        #SNR, bias, stderr, conf_interval = snr_constant_noise(signal_arr, 0.95)
        print(f"{SNR}\t{bias}\t{stderr}\t{conf_interval[0]}\t{conf_interval[1]}\t{os.path.dirname(ilist[0])}\t{len(signal_arr)}")

