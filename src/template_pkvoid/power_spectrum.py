#!/usr/bin/env python
import sys
import os
import subprocess
import numpy as np
from mpi4py import MPI
from params import *
size = MPI.COMM_WORLD.Get_size()   # Size of communicator
rank = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
#size, rank = 1, 0
# Paths
RUN = os.path.join(BIN, 'powspec_cross/powspec')
OUTDIR = os.path.join(RESULTS, 'linvoid_powspec/box_size-{}_R-{}-{}'.format(box_size, R_min, R_max))
INDIR = os.path.join(RESULTS, 'linvoid/box_size-{}_R-{}-{}'.format(box_size, R_min, R_max))
os.makedirs(OUTDIR, exist_ok=True)
p = box_size
c = os.path.join(SRC, 'template_pkvoid/powspec.conf')
input_catalogs = os.listdir(INDIR) # Get filenames of inputs
split_input_catalogs = np.array_split(input_catalogs, size)
for input_catalog in split_input_catalogs[rank]:
    a = os.path.join(INDIR, input_catalog)
    b = 'NONE' # Input tracer B
    i,j = '0', '0' # File types (ascii)
    o = os.path.join(OUTDIR, 'Pk_'+input_catalog) # Output filename
    if os.path.isfile(o):
        continue
    command = [RUN, '-c', c, '-a', a, '-b', b, '-i', i, '-j', j, '-o', o, '-p', str(p)]
    compute = subprocess.Popen(command).wait()
MPI.Finalize()
