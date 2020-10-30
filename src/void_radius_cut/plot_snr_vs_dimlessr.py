#!/usr/bin/env python

import glob
import os
import sys
import re
import numpy as np
import pandas as pd
import multiprocessing
from multiprocessing.pool import ThreadPool
import subprocess
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from scipy.optimize import minimize_scalar, curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create", action="store_true")
args = parser.parse_args()
create_jobs = args.create
load_dotenv()
WORKDIR = os.getenv("WORKDIR")
NGAL = {'1':3.976980e-4, '5':1.976125e-4}
boxes = ['1']
spaces = ['redshift']
recon = ['patchy_results']#,'patchy_recon', 'patchy_recon_nods']
dimless_r = [0.7, 0.75, 0.8,0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]

def call_proc(cmd):
    """ This runs in a separate thread. """
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.check_call(cmd, shell=True)
    #p.wait()
    #print(p.stdout.read())
    #out, err = p.communicate()
    #return (out, err)
    
def R_vs_ngal(ngal, a, b, c, d):
  return a * (ngal -b)**c + d
if __name__ == '__main__':
  joblist = open("snr_joblist.sh", "w")
  for box in boxes:
    for space in spaces:
      for rec in recon:
        fig = plt.figure()
        main_path = f"{WORKDIR}/{rec}/box{box}/{space}/smooth/flat_*"
        dirlist = list(filter(os.path.isdir, glob.glob(main_path)))
        odir = f"{WORKDIR}/{rec}/box{box}/{space}/plots/"
        optima = []
        ngal = []
        for dir_ in dirlist:
           #print(dir_)
           comp = float(re.findall("flat_[0-9].*$", dir_)[0].replace("flat_", ""))
           existing_dr = []; r_dirlist=[]
           for dr in dimless_r:
             d = f"{dir_}/tpcf_void_mock_nowt_R-scaled{dr}-50"
             if not os.path.isdir(d) or len(os.listdir(d)) < 2: continue
             r_dirlist.append(d)
             existing_dr.append(dr)
           if len(r_dirlist)==0: continue
           snr_file = f"{odir}/snr_{os.path.basename(dir_)}.dat"
           if not os.path.exists(snr_file) or create_jobs:
             print(f"Creating joblist to update SNR files.")
             command = ["./signal_to_noise.py"] + [f"<(ls {d}/T*)" for d in r_dirlist] + [">", f"{snr_file}"]
             joblist.write(" ".join(command)+"&\n")
           else:
             data = pd.read_csv(snr_file, delim_whitespace=True, usecols=[0,2,5], names=['snr', 'std', 'dir'], comment="#", dtype={'snr':float, 'std':float, 'dir':str})
             if data.shape[0] < 3: continue 
             print(data)
             dr = np.array([re.findall('R.scaled[0-9].*-50', data['dir'].iloc[i])[0].replace("R-scaled","").replace("-50", "") for i in range(data.shape[0])], dtype=float)
             snr_interp = interp1d(dr, data['snr'].values, kind="quadratic")
             res = minimize_scalar(lambda x: -snr_interp(x), method="Bounded", bounds = dr[[0, -1]])
             ngal.append(NGAL[box]*comp) 
             optima.append(res.x * (ngal[-1] ** (-1/3)))
             plt.scatter(res.x, snr_interp(res.x))
             p = plt.errorbar(dr, data['snr'].values, yerr =data['std'].values, label = f"{os.path.basename(dir_)}")
             color = p[0].get_color()
             dr_linsp = np.linspace(dr[0], dr[-1], 100)
             plt.plot(dr_linsp, snr_interp(dr_linsp), color=color, ls = "--")
        if os.path.exists(snr_file) and not create_jobs:
          optima = np.array(optima)
          ngal = np.array(ngal)
          plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
          plt.gcf()
          #plt.tight_layout()
          ofig = f"{odir}/snr_vs_dimlessr.pdf"
          plt.savefig(f"{ofig}", bbox_inches="tight")
          print(f"Saved {ofig}")

          fig = plt.figure()
          slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(ngal*1e4), np.log(optima))
          np.savetxt(f"{odir}/optimum_rescaled_radius_interp.dat", np.c_[optima, ngal], header=f"exp = -{slope}\nconst = {np.exp(intercept)*10**(4*slope)}\nRoptimum ngal")
          print(slope, intercept, r_value, std_err)
          line, = plt.plot(1e4 * ngal, optima*ngal**(-slope), marker=(5, 1, 180), lw=0, c = 'k')
          print("Mean value of R optima: ", np.mean(optima*ngal**(-slope)))
          plt.gca().axhline(np.exp(intercept)*10**(4*slope), c='k', ls='--', label=r'$\bar{n}_{\mathrm{gal}}^{%0.5f}~R^* = %+.2f$ (Mpc/$h$)$^{%.5f}$'%(-slope,np.exp(intercept)*10**(4*slope), -slope))
          plt.ylabel(r'$\bar{n}_{\mathrm{gal}}^{%.2f}~R^*$ [(Mpc/$h$)$^{%.2f}$]'%(-slope, -slope), fontsize=11) 
          plt.xlabel(r'$\bar{n}_{\mathrm{gal}}$ [$10^{-4}h^3$/Mpc$^3]$', fontsize=11)
          plt.ylim(1, 3)
          plt.legend(loc=0)
          ofig = f"{odir}/optimum_dimlessr_interp.pdf"

          fig.savefig(ofig, dpi=200)
          print(f"Saved {ofig}")

joblist.close()
