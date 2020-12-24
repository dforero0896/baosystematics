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
from tqdm import tqdm

names = ['x', 'y', 'z', 'r', 'w', 'scaled_r']
zedges = np.linspace(0, box_size, NGRID//100 + 1)
def worker(filename):
    id_, fn, odir, kind = filename
    print(f"==> Reading {fn}", flush=True)
    data = pd.read_csv(fn, delim_whitespace=True, 
			names=['x', 'y', 'z', 'r', 'w', 'scaled_r'],
			dtype=np.float32)
    data.dropna(how='any', axis=1, inplace=True)
    names=data.columns.tolist()
    data['zid'] = np.searchsorted(zedges, data.z, side='right')
    data['rid'] = np.searchsorted(radius_bins, data.r, side='right')
    lens = []
    #if data.shape[1] <= 4: kind='radial'
    if kind=='ang':
        cols = [[names[0], names[1], names[-1]], names[2:-1]]
    elif kind=='radial':
        cols=  [names[:2],names[2:]]
    else : raise NotImplementedError
    for key, df in tqdm(data.groupby(['zid', 'rid'])):
        #sys.stdout.flush()
        oname_left=f"{odir}/{id_:0>3}_zmax{key[0]}_rmax{key[1]}.left"
        oname_right=f"{odir}/{id_:0>3}_zmax{key[0]}_rmax{key[1]}.right"
        if np.any(df[names[-1]].values==0): sys.exit("Found zero values in last column")
        #if not os.path.exists(oname_left) or overwrite:
        df[cols[0]].sample(frac=1).to_csv(oname_left, header=False, index=False, sep=" ")
        #if not os.path.exists(oname_right):
        df[cols[1]].to_csv(oname_right, header=False, index=False, sep=" ")
        lens.append(len(df))
    print(f"==> Split {fn} saved {oname_left}") 
    return sum(lens)
if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT_DIR', help="Directory containing void catalogs to shuffle into a random catalog.")
    parser.add_argument('OVERWRITE', help="Overwrite bin files.")
    parser.add_argument('-o', '--odir', required=False, help="Output directory name (Default: void_ran)")
    parser.add_argument('-k', '--kind', required=False, help="Coordinate to shuffle scaled_R with. 'radial' or 'ang' (Default: radial)")
    parsed=parser.parse_args()
    args=vars(parsed)
    indir = args['INPUT_DIR']
    overwrite = bool(int(args['OVERWRITE']))
    odirname = args['odir'] or 'void_ran'
    kind = args['kind'] or 'radial'
    odir = os.path.abspath(os.path.join(indir,f"../{odirname}/bins"))
    os.makedirs(odir, exist_ok=True)
    fnames = [os.path.join(indir,f) for f in os.listdir(indir)][:32]
    args = list(zip(range(len(fnames)), fnames, [odir]*len(fnames), [kind]*len(fnames)))
    print(f"==> Saving binned chunks in {odir}")
    nproc = MPI.COMM_WORLD.Get_size()
    iproc = MPI.COMM_WORLD.Get_rank()
    inode = MPI.Get_processor_name()
    args_split = np.array_split(args, nproc)
    for arg in args_split[iproc]:
        worker(arg)
 
    size=mp.cpu_count()
    #with mp.Pool(processes=size) as pool:
    #    result=pool.map(worker, args)
    #print(sum(result))
    if iproc==0:
        np.savetxt(f"{odir}/zedges.dat", zedges) 
        np.savetxt(f"{odir}/redges.dat", radius_bins) 
    MPI.Finalize()
