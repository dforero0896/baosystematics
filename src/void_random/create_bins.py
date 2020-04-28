#!/us/bin/env python
import numpy as np
import pandas as pd
import multiprocessing as mp
from mpi4py import MPI
import os
import sys
from dotenv import load_dotenv
load_dotenv()
SRC = os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import *

names = ['x', 'y', 'z', 'r', 'scaled_r']
zedges = np.linspace(0, box_size, NGRID//100 + 1)
def worker(filename):
    id_, fn, odir = filename
    #print(f"==> Reading {fn}")
    data = pd.read_csv(fn, delim_whitespace=True, 
			names=names,
			dtype=np.float32)
    data.dropna(how='any', axis=1)
    data['zid'] = np.searchsorted(zedges, data.z, side='right')
    data['rid'] = np.searchsorted(radius_bins, data.r, side='right')
    lens = []
    for key, df in data.groupby(['zid', 'rid']):
        oname_left=f"{odir}/{id_:0>3}_zmax{key[0]}_rmax{key[1]}.left"
        oname_right=f"{odir}/{id_:0>3}_zmax{key[0]}_rmax{key[1]}.right"
        if not os.path.exists(oname_left) or overwrite:
            df[names[:2]].to_csv(oname_left, header=False, index=False, sep=" ")
        if not os.path.exists(oname_right):
            df[names[2:]].to_csv(oname_right, header=False, index=False, sep=" ")
        lens.append(len(df))
    print(f"==> Split {fn} saved {oname_left}") 
    return sum(lens)
if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.exit(f"USAGE: {sys.argv[0]} INPUT_DIR OVERWRITE")

    indir = sys.argv[1]
    overwrite = bool(int(sys.argv[2]))
    odir = os.path.abspath(os.path.join(indir,'../void_ran/bins'))
    os.makedirs(odir, exist_ok=True)
    fnames = [os.path.join(indir,f) for f in os.listdir(indir)][:100]
    args = list(zip(range(len(fnames)), fnames, [odir]*len(fnames)))
    print(f"==> Saving binned chunks in {odir}")
    nproc = MPI.COMM_WORLD.Get_size()
    iproc = MPI.COMM_WORLD.Get_rank()
    inode = MPI.Get_processor_name()
    args_split = np.array_split(args, nproc)
    for arg in args_split[iproc]:
        worker(arg)
 
    #size=mp.cpu_count()
    #with mp.Pool(processes=size) as pool:
    #    result=pool.map(worker, args)
    #print(sum(result))
    MPI.Finalize()
