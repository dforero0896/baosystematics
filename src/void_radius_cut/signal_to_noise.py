#!/usr/bin/env python
import numpy as np
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
        signal_arr=[]
        for ifile in ilist:
            ipath = ifile
            iarr = np.loadtxt(ipath)
            s = iarr[:,0]
            xi = iarr[:,1]
            s_vals_id = np.array([np.where(s==val)[0] for val in s_vals])
            xi_vals = xi[s_vals_id]
            signal_arr.append(xi_vals[0] - np.mean(xi_vals[1:]))
        #signal_resamples = jackknife_resampling(signal_arr)
        signal_arr = np.array(signal_arr)
        SNR, bias, stderr, conf_interval = jackknife_stats(signal_arr, signal_to_noise_ratio, 0.95)
        print(f"{SNR}\t{bias}\t{stderr}\t{conf_interval[0]}\t{conf_interval[1]}\t{os.path.dirname(ilist[0])}\t{len(ilist)}")
        resamples = jackknife_resampling(signal_arr)

        #jack_stat = np.apply_along_axis(signal_to_noise_ratio, 1, resamples)
        #import matplotlib.pyplot as plt
        #plt.hist(jack_stat, bins=100, label='%.1f +/- %.1f'%(SNR, stderr), histtype='step')
        #plt.legend()
        #SNR = signal_to_noise_ratio(signal_arr)
        #print(f"{SNR}\t{os.path.dirname(ilist[0])}\t{len(ilist)}")
    plt.show()
