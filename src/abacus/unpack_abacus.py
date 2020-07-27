#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import sys
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/AbacusCosmos")
from AbacusCosmos import Halos
import argparse
import glob
from tqdm import tqdm
from mpi4py import MPI

def bin_to_ascii(idir, odir):
    cat = Halos.make_catalog_from_dir(dirname=idir,
                                  load_subsamples=False, load_pids=False)
    halos = cat.halos
    data=pd.DataFrame(cat.halos['pos'])
    os.makedirs(odir, exist_ok=True)
    oname=f"{odir}/halos.dat"
    data.to_csv(oname, sep=" ", header=False, index=False)
    

if __name__=='__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--idir', required=False, help='Directory where Abacus catalogs are located.')
    parser.add_argument('-o', '--odir', required=True, help='Directory to save ASCII Abacus catalogs.')

    parsed = parser.parse_args()
    args = vars(parsed)
    abacus_idirs = glob.glob(f"{args['idir']}/*/*/*halos*/z*")
    abacus_odirs = [s.replace(args['idir'], args['odir']) for s in abacus_idirs]
    pairs=list(zip(abacus_idirs, abacus_odirs))
    comm=MPI.COMM_WORLD
    rank=comm.Get_rank()
    size=comm.Get_size()
    pairs_splits=np.array_split(pairs, size)
    for idir, odir in tqdm(pairs_splits[rank]):
        bin_to_ascii(idir, odir)
        sys.exit(0)

    MPI.Finalize()
