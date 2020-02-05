#!/usr/bin/env python
import sys
import os
import subprocess
from mpi4py import MPI
import numpy as np
from params import *
from radius_cut_batch import radius_cut_single
size = MPI.COMM_WORLD.Get_size()   # Size of communicator
rank = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator


# Paths
RUN = os.path.join(BIN, 'DIVE_box/DIVE_box')
OUTDIR = os.path.join(RESULTS, 'linvoid/box_size-{}'.format(box_size))
INDIR = os.path.join(RESULTS, 'linhalo/box_size-{}'.format(box_size))
os.makedirs(OUTDIR, exist_ok=True)
input_catalogs = os.listdir(INDIR)
split_input_catalogs = np.array_split(input_catalogs, size)
for i in split_input_catalogs[rank]:
    input_catalog = os.path.join(INDIR, i) 
    output_catalog = os.path.join(OUTDIR, i.replace('halo', 'void'))
    if os.path.isfile(output_catalog):
        continue
    command = [RUN, input_catalog, output_catalog, str(box_size), '0', '999']
    print(command)
    compute = subprocess.Popen(command).wait()
    radius_cut_single(output_catalog)
MPI.Finalize()

