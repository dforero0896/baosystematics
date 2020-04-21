#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import sys
import dask.dataframe as dd
import dask.array  as da
from dotenv import load_dotenv
load_dotenv()
SRC = os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import *
def dask_save_radial_density(files, box_size=box_size, N_grid=NGRID):
    fnlist = os.listdir(files)
    nmocks = len(fnlist)
    zedges = np.linspace(0, box_size, N_grid + 1)
    data = dd.read_csv(f"{files}/*", delim_whitespace=True, usecols=[2],\
		 names = ['z'], dtype=np.float32)
    hist, _ = da.histogram(data['z'].values, bins = zedges)
    histcomp = hist.compute()
    histcomp = histcomp/(nmocks)# * box_size * box_size * (zedges[1:] - zedges[:-1]))
    odir = os.path.abspath(f"{files}/../plots")
    os.makedirs(odir, exist_ok=True)
    oname = f"{odir}/ngal_radial.dask.npy"
    np.save(oname, histcomp)    
    print(f"==> Saved {oname}")

def radial_n_worker(fname, box_size=box_size, N_grid=NGRID):
    zedges = np.linspace(0, box_size, N_grid + 1)
    data = pd.read_csv(f"{fname}", delim_whitespace=True, usecols=[2],\
			names = ['z'], dtype=np.float32)
    hist, _ = np.histogram(data['z'].values, bins = zedges)
    #hist = hist/(box_size * box_size * (zedges[1:] - zedges[:-1]))
    return hist
def ang_n_worker(fname, box_size=box_size, N_grid=NGRID):
    xedges = np.linspace(0, box_size, N_grid + 1)
    yedges = xedges
    data = pd.read_csv(f"{fname}", delim_whitespace=True, usecols=[0,1],\
			names = ['x', 'y'], dtype=np.float32)
    hist, _, _ = np.histogram2d(data['x'].values, data['y'].values, 
				bins =(xedges, yedges))
    #hist = hist/(box_size * (xedges[1:] - xedges[:-1]) * (yedges[1:] - yedges[:-1]))
    return hist
def mp_save_radial_density(files, box_size=box_size, N_grid=NGRID, out='ngal_radial.npy'):

    import multiprocessing as mp
    size = mp.cpu_count()
    fnlist = [os.path.join(files, f) for f in os.listdir(files)]
    with mp.Pool(processes=size) as pool:
        result=pool.map(radial_n_worker, fnlist)
    histcomp = np.array(result).mean(axis=0)
    odir = os.path.abspath(f"{files}/../plots")
    os.makedirs(odir, exist_ok=True)
    oname = f"{odir}/{out}"
    np.save(oname, histcomp)    
    print(f"==> Saved {oname}")
def mp_save_ang_density(files, box_size=box_size, N_grid=NGRID, out="ngal_ang.npy"):
    import multiprocessing as mp
    size = mp.cpu_count()
    fnlist = [os.path.join(files, f) for f in os.listdir(files)]
    with mp.Pool(processes=size) as pool:
        result=pool.map(ang_n_worker, fnlist)
    histcomp = np.array(result).mean(axis=0)
    odir = os.path.abspath(f"{files}/../plots")
    os.makedirs(odir, exist_ok=True)
    oname = f"{odir}/{out}"
    np.save(oname, histcomp)    
    print(f"==> Saved {oname}")

        
def iter_save_radial_density(files, box_size=box_size, N_grid=NGRID):
    # Very slow
    fnlist = [os.path.join(files, f) for f in os.listdir(files)]
    result = []
    for f in fnlist:
        result.append(radial_n_worker(f))
    histcomp = np.array(result).mean(axis=0)
    odir = os.path.abspath(f"{files}/../plots")
    os.makedirs(odir, exist_ok=True)
    oname = f"{odir}/ngal_radial.mp.npy"
    np.save(oname, histcomp)    
    print(f"==> Saved {oname}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} CATALOG_DIR OUT_BASE")
    filedir = sys.argv[1]
    out = sys.argv[2]
    mp_save_radial_density(filedir, out=out+'_radial.npy')
    mp_save_ang_density(filedir, out=out+'_ang.npy')
