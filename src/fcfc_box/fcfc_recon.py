#!usr/bin/env python

import numpy as np
import pandas as pd
import time
import os
import sys
import subprocess
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from Corrfunc.theory.xi import xi
import glob
from dotenv import load_dotenv
load_dotenv()
import argparse
from mpi4py import MPI

nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
inode = MPI.Get_processor_name()    # Node where this MPI process runs

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cpus", type=int, default=64)
parser.add_argument("-compid", "--compid", type=int, help="0-9 index to choose completeness to use")
args=parser.parse_args()

WORKDIR=os.getenv("WORKDIR")
NGAL_COMPLETE=3.977e-4
#comps = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
comps = [0.3, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
if args.compid is None:
    split_comps = np.array_split(comps, nproc)
    comps = split_comps[iproc]
else:
    comps = [comps[args.compid]]
r_dimless=[0.8, 0.87, 0.93, 1.0, 1.07, 1.13]
#r_dimless=[0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
bins = np.linspace(0.0001, 200, 41)
bin_centers = 0.5 * (bins[1:] + bins[:-1])
autocorr=1
nthreads=args.cpus
box_size=2500
for comp in comps:
    IDIR=f"{WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_{comp}/mocks_void_xyz"
    #ODIRS = [f"{WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_{comp}/tpcf_void_mock_nowt_R-scaled{sr}-50" for sr in r_dimless]

    for f in glob.glob(f"{IDIR}/*dat"):
        print(f"==> INPUT:\t{f}", flush=True)
        BASE=os.path.basename(f)
        #if all([os.path.isfile(f"{WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_{comp}/tpcf_void_mock_nowt_R-scaled{sr}-50/TwoPCF_{BASE.replace('.dat', f'.R-scaled{sr}-50.dat') }") for sr in r_dimless]):
        if all([os.path.isfile(f"{WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_{comp}/tpcf_void_mock_nowt_R-scaled{sr}-50/TwoPCF_{BASE}") for sr in r_dimless]):
            print(f"==> All 2PCF computed, skipping.")
            continue
        data = pd.read_csv(f, delim_whitespace=True, engine="c", names=['x', 'y', 'z', 'r'], usecols=[0, 1, 2, 3])
        data.set_index("r", inplace=True)
        data.sort_index(0, inplace=True)
        Ntot = data.shape[0]
        #mask = data.index <= 50
        #data = data.loc[mask]
        data = data.loc[:50]
        OLD_BASE=BASE
        for sr in r_dimless:

            RMIN=sr/((comp*NGAL_COMPLETE)**(1./3))
            ODIR=f"{WORKDIR}/patchy_recon_nods/box1/redshift/smooth/flat_{comp}/tpcf_void_mock_nowt_R-scaled{sr}-50"
            BASE = OLD_BASE#.replace(".dat", f".R-scaled{sr}-50.dat")
            DD=f"{ODIR}/DD_files/DD_{BASE}"
            TPCF=f"{ODIR}/TwoPCF_{BASE}"
            print(f"==> DD COUNTS:\t{DD}")
            print(f"==> OUTPUT:\t{TPCF}")
            if os.path.isfile(TPCF):
                print(f"==> 2PCF computed, skipping.")
                continue
            d_sel=data.loc[RMIN:].values
            print(f"==> Rmin = {RMIN}, Rmax =50")
            N = d_sel.shape[0]
            print(f"==> Using {N}/{Ntot} tracers")
            xi_counts = xi(box_size, nthreads, bins, d_sel[:,0], d_sel[:,1], d_sel[:,2], verbose=True) 
            out=np.c_[bin_centers, xi_counts['xi'], np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
            np.savetxt(TPCF, out, fmt="%.3f %.8e %.0f %.0f")
            print(f"==> The correlation function is saved.")
            out=np.c_[xi_counts['rmin'], xi_counts['rmax'], xi_counts['npairs'], xi_counts['npairs']/(N * N), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
            np.savetxt(DD, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
            print(f"==> The DD counts are saved.", flush=True)
            
