#!/usr/bin/env python
import sys
import os
import subprocess
import numpy as np
from mpi4py import MPI
from params import *
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
# Paths
RUN = os.path.join(BIN, 'linhalo/linhalo')
OUTDIR = os.path.join(RESULTS, 'linhalo/box_size-{}'.format(box_size))
os.makedirs(OUTDIR, exist_ok=True)
INPUT = os.path.join(BIN, 'BAOfit_void/input/Albert_Pnw.dat')
i = INPUT
c = os.path.join(SRC, 'template_pkvoid/linhalo.conf')
b = box_size
n = n_halo
seeds = np.arange(N_in, N+1)
split_seeds = np.array_split(seeds, size)
for s in split_seeds[rank]:
    o = os.path.join(OUTDIR, 'NW_halo_seed-{}.ascii'.format(s))
    while not os.path.isfile(o) and s < 1000:
        o = os.path.join(OUTDIR, 'NW_halo_seed-{}.ascii'.format(s))
        command_catalog = [RUN, '-i', i, '-c', c, '-s', str(s), '-o', o, '-b', str(b), '-n', str(n)]
        compute = subprocess.Popen(command_catalog).wait()
        s+=100
MPI.Finalize()
