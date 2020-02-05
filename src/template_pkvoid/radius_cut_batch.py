#!/usr/bin/env python
import sys
import os
import subprocess
import numpy as np
from mpi4py import MPI
from params import *
def main():
    size = MPI.COMM_WORLD.Get_size()   # Size of communicator
    rank = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
    #size, rank = 1, 0
    # Paths
    RUN = os.path.join(SRC, 'template_pkvoid/radius_cut.sh')
    OUTDIR = os.path.join(RESULTS, 'linvoid/box_size-{}_R-{}-{}'.format(box_size, R_min, R_max))
    INDIR = os.path.join(RESULTS, 'linvoid/box_size-{}'.format(box_size))
    os.makedirs(OUTDIR, exist_ok=True)
    delimiter = " "
    input_catalogs = os.listdir(INDIR) # Get filenames of inputs
    split_input_catalogs = np.array_split(input_catalogs, size)
    for input_catalog in split_input_catalogs[rank]:
        ifile = os.path.join(INDIR, input_catalog)
        command = [RUN, ifile, OUTDIR, str(R_min), str(R_max), delimiter, '0']
        compute = subprocess.Popen(command).wait()
    MPI.Finalize()
def radius_cut_single(ifile):
    RUN = os.path.join(SRC, 'template_pkvoid/radius_cut.sh')
    OUTDIR = os.path.join(RESULTS, 'linvoid/box_size-{}_R-{}-{}'.format(box_size, R_min, R_max))
    INDIR = os.path.join(RESULTS, 'linvoid/box_size-{}'.format(box_size))
    os.makedirs(OUTDIR, exist_ok=True)
    delimiter = " "
    command = [RUN, ifile, OUTDIR, str(R_min), str(R_max), delimiter, '0']
    compute = subprocess.Popen(command).wait()
if __name__ == '__main__':
    main()
