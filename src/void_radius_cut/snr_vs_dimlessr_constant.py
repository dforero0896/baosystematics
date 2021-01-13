#!/usr/bin/env python

import glob
import os
import sys
import re
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from scipy.optimize import minimize_scalar, curve_fit
from scipy.interpolate import interp1d, UnivariateSpline
from scipy import stats
from astropy.stats import jackknife_stats
from signal_to_noise import read_inlist, signal_to_noise_ratio
from multiprocessing import Pool
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
def count_lines(m):
    return pd.read_csv(m, delim_whitespace=True, engine='c', usecols=(0,)).shape[0]
def compute_snr(args):
    base, dr, s_vals = args
    dir = f"{base}/tpcf_void_mock_nowt_R-dl{dr}-50"
    ilist = glob.glob(f"{dir}/T*")[:185]
    print(f"==> Found {len(ilist)} correlations.")
    signal_arr=[]
    for ifile in ilist:
        iarr = pd.read_csv(ifile, delim_whitespace=True, engine='c', usecols=(0,1)).values
        s = iarr[:,0]
        xi = iarr[:,1]
        s_vals_id = np.array([np.where(s==val)[0] for val in s_vals])
        xi_vals = xi[s_vals_id]
        signal_arr.append(xi_vals[0] - np.mean(xi_vals[1:]))
    signal_arr = np.array(signal_arr)
    SNR, bias, stderr, conf_interval = jackknife_stats(signal_arr, signal_to_noise_ratio, 0.95)
    return SNR, bias, stderr, conf_interval[0], conf_interval[1], len(ilist)

load_dotenv()
WORKDIR = os.getenv("WORKDIR")
box_size=2500
s_bao = 102.5
s_dl_1 = 82.5
s_dl_2 = 87.5
s_dr_1 = 117.5
s_dr_2 = 122.5
s_vals = [s_bao, s_dl_1, s_dl_2, s_dr_1, s_dr_2]
names = ["SNR","bias","stderr","conf_int_low","conf_int_high","samples_dir","n_samples"]
dimless_r = np.array([0.87, 0.93, 1.0, 1.13, 1.19, 1.25, 1.33])
dr = np.linspace(dimless_r[0], dimless_r[-1], 100)
ls = ['-', '--']
markers = ['o', 's']
if __name__=="__main__":
    for box in ['1', '5']:
        for j, space in enumerate(['redshift', 'real']):
            for i, syst in enumerate(['radialgauss', 'smooth/parabola_0.8']):
                print(f"{box}, {space}, {syst}")
                dir=f"{WORKDIR}/patchy_results/box{box}/{space}/{syst}*"
                mocks = glob.glob(f"{dir}/mocks_gal_xyz/*")[:20]
                pool = Pool(len(mocks))
                Ngal = np.array(pool.map(count_lines, mocks))
                ngal=(Ngal/(box_size**3)).mean()
                R = np.array(dimless_r) / (ngal**(1./3))
                #print(R)
                pool = Pool(len(dimless_r))
                args = zip([dir]*len(dimless_r), dimless_r, [s_vals]*len(dimless_r))
                results = pool.map(compute_snr, args)
                results = np.array(results)
                mask = results[:,0] == max(results[:,0])
                print("Discrete: ", "R ", dimless_r[mask]/ngal**(1/3), "snr ", results[mask,0], "rescaled ", ngal**(0.238)*dimless_r[mask]/ngal**(1/3))
                print(dimless_r[mask], results[mask,0])
                #snr_interp = interp1d(dimless_r, results[:,0], kind='quadratic')
                snr_interp = UnivariateSpline(dimless_r, results[:,0], k=4)#, w=results[:,-1]/results[:,-1].sum())
                res = minimize_scalar(lambda x: -snr_interp(x), method='Bounded', bounds = dimless_r[[0,-1]])
                print("Interp: ", "R ", (res.x/ngal**(1./3)), "snr ", snr_interp(res.x), "rescaled ", ngal**(0.238)*res.x/ngal**(1./3))
                plt.errorbar(dimless_r/ngal**(1./3), results[:,0], yerr=results[:,1], marker=markers[i], lw=1,label=f"{box}, {space}, {syst}", markersize=0)
                plt.plot(dr/ngal**(1./3), snr_interp(dr), ls=ls[j])
                plt.scatter(res.x/ngal**(1./3), snr_interp(res.x), marker="^")

    plt.gcf()
    plt.legend()
    oname=f"constant.pdf"
    plt.savefig(oname, dpi=300)
    print(f"Saved {os.path.abspath(oname)}")



