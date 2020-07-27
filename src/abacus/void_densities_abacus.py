#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import sys
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
WORKDIR=os.environ.get('WORKDIR')
sys.path.append(f"{SRC}/AbacusCosmos")
from AbacusCosmos import Halos
import argparse
import glob
from tqdm import tqdm
from mpi4py import MPI

def void_density(ifile):

    obase = os.path.dirname(ifile)
    ofile = f"{obase}/void_number_density.npy"
    data = pd.read_csv(ifile, delim_whitespace=True, names=['r'], usecols=[3], engine='c')
    edges = np.linspace(0, 60, 100)
    hist, _ = np.histogram(data.values, bins=edges, density=True)
    tosave = np.c_[edges[:-1], edges[1:], hist]
    np.save(ofile, tosave)    

if __name__=='__main__':

    parser=argparse.ArgumentParser()
#    parser.add_argument('-i', '--idir', required=False, help='Directory where Abacus catalogs are located.')
#    parser.add_argument('-o', '--odir', required=True, help='Directory to save ASCII Abacus catalogs.')

#    parsed = parser.parse_args()
#    args = vars(parsed)
    ifiles = glob.glob(f"{WORKDIR}/abacus_results/*/*/*halos*/z*/halo_voids.dat")
    comm=MPI.COMM_WORLD
    rank=comm.Get_rank()
    size=comm.Get_size()
    ifile_splits=np.array_split(ifiles, size)
    for ifile in tqdm(ifile_splits[rank]):
        void_density(ifile)
        sys.exit(0)

    MPI.Finalize()
