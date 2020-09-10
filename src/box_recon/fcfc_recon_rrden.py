#!/usr/bin/env python

import pandas as pd
import os
import sys
from dotenv import load_dotenv
load_dotenv()
WORKDIR = os.environ.get("WORKDIR")
from mpi4py import MPI
import glob
from tqdm import tqdm
import numpy as np
from scipy.special import legendre
spaces=['redshift', 'real']
boxes= ['1', '5']
def rr_analytic2d(bin_low_bound, bin_high_bound, box_size, nmu_bins=80):
    volume = 4 * np.pi * (bin_high_bound**3 - bin_low_bound**3) / 3
    normed_volume = volume / box_size **3
    mu_edges = np.linspace(0,1,nmu_bins+1)
    mu = 0.5 * (mu_edges[:-1] + mu_edges[1:])
    mono = normed_volume[:,None] / (nmu_bins*np.ones(nmu_bins)[None,:])
    quad = mono*(2*2+1) * legendre(2)(mu)[None, :]
    #hexa = mono*(4*2+1) * legendre(4)(mu)[None, :]

    RR0 = np.sum(mono, axis=1)
    RR2 = np.sum(quad, axis=1)
    #RR4 = np.sum(hexa, axis=1)
    return pd.DataFrame(dict(zip(['mono', 'quad'], [RR0, RR2])))

def main():
    use_rr_num=False
    for box in boxes:

        for space in spaces:

           IDIR=f"{WORKDIR}/patchy_recon/box{box}/{space}/nosyst/mocks_gal_xyz"
           TPCFDIR=f"{WORKDIR}/patchy_recon/box{box}/{space}/nosyst/tpcf_gal_mock_nowt"
           if use_rr_num:
               ODIR=f"{os.path.dirname(IDIR)}/tpcf_gal_mock_nowt_rrnum/"
           else:
               ODIR=f"{os.path.dirname(IDIR)}/tpcf_gal_mock_nowt_rrden/"
           os.makedirs(ODIR, exist_ok=True)
           
           tpcf_in=glob.glob(f"{TPCFDIR}/Two*")
           for i, tpcf_fn in tqdm(enumerate(tpcf_in)):
               DD = tpcf_fn.replace("TwoPCF_", "DD_files/DD_")
               DS = tpcf_fn.replace("TwoPCF_", "DS_files/DS_")
               SS = tpcf_fn.replace("TwoPCF_", "SS_files/SS_")
               if not (os.path.isfile(DD) and os.path.isfile(DS) and os.path.isfile(SS)): continue
               dd = pd.read_csv(DD, delim_whitespace=True, engine='c', names = ['s_low', 's_high', 'mono', 'quad'], usecols=[0,1,3,5]) 
               ds = pd.read_csv(DS, delim_whitespace=True, engine='c', names = ['mono', 'quad'], usecols=[3,5]) 
               ss = pd.read_csv(SS, delim_whitespace=True, engine='c', names = ['mono', 'quad'], usecols=[3,5]) 
               if i==0: rr = rr_analytic2d(dd['s_low'], dd['s_high'], 2500)

               if use_rr_num:
                   tpcf = (dd - 2 * ds + rr) / rr['mono'].values[:,None]
               else:
                   tpcf = (dd - 2 * ds + ss) / rr['mono'].values[:,None]
                   
               tpcf['s'] = 0.5 * (dd['s_low'] + dd['s_high'])
               tpcf_out=f"{ODIR}/{os.path.basename(tpcf_fn)}"
          
               tpcf[['s', 'mono', 'quad']].to_csv(tpcf_out, header=False, index=False, sep=" ")
               print(f"==> Saved {tpcf_out}", flush=True)


if __name__=='__main__': 
    main()       
