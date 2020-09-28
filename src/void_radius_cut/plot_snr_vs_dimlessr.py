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
load_dotenv()
WORKDIR = os.getenv("WORKDIR")
boxes = ['1']
spaces = ['redshift']
recon = ['patchy_recon', 'patchy_results']
dimless_r = [0.7, 0.75, 0.8,0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]

def call_proc(cmd):
    """ This runs in a separate thread. """
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.check_call(cmd, shell=True)
    #p.wait()
    #print(p.stdout.read())
    #out, err = p.communicate()
    #return (out, err)
    
if __name__ == '__main__':
  joblist = open("snr_joblist.sh", "w")
  for box in boxes:
    for space in spaces:
      for rec in recon:
        fig = plt.figure()
        main_path = f"{WORKDIR}/{rec}/box{box}/{space}/smooth/flat_*"
        dirlist = list(filter(os.path.isdir, glob.glob(main_path)))
        odir = f"{WORKDIR}/{rec}/box{box}/{space}/plots/"
        call_results = []
        for dir_ in dirlist:
           print(dir_)
           existing_dr = []; r_dirlist=[]
           for dr in dimless_r:
             d = f"{dir_}/tpcf_void_mock_nowt_R-scaled{dr}-50"
             if not os.path.isdir(d) or len(os.listdir(d)) < 2:print(f"Skipped {d}"); continue
             r_dirlist.append(d)
             existing_dr.append(dr)
           if len(r_dirlist)==0: continue
           snr_file = f"{odir}/snr_{os.path.basename(dir_)}.dat"
           if not os.path.exists(snr_file):
             command = ["./signal_to_noise.py"] + [f"<(ls {d}/T*)" for d in r_dirlist] + [">", f"{snr_file}"]
             joblist.write(" ".join(command)+"&\n")
           else:
             data = pd.read_csv(snr_file, delim_whitespace=True, usecols=[0,2,5], names=['snr', 'std', 'dir'], comment="#", dtype={'snr':float, 'std':float, 'dir':str})
             for i, d in enumerate(data['dir'].values): assert str(existing_dr[i]) in d
             plt.errorbar(existing_dr, data['snr'].values, yerr =data['std'].values, label = f"{os.path.basename(dir_)}")
           
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.gcf()
        #plt.tight_layout()
        ofig = f"{odir}/snr_vs_dimlessr.pdf"
        plt.savefig(f"{ofig}", bbox_inches="tight")
        print(f"Saved {ofig}")
joblist.close()
