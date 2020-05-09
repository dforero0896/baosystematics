#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import *
import numpy as np
if __name__ == '__main__':
    ODIR='/hpcstorage/dforero/projects/baosystematics/patchy_results/many_random'
    comp = np.arange(0.1, 1.05, 0.05)
    ngal=NGAL['1']*comp
    NFILES=100
    RUN="./uniform_random.o"
    joblist = open('joblist.sh', 'w')
    for i, n in enumerate(ngal):
        odir = f"{ODIR}/comp_{comp[i]:.2f}_n{NGAL['1']:.5e}/discrete_tracers"
        os.makedirs(odir, exist_ok=True)
        nobj = int(2500**3 * n)
        for k in range(NFILES):
            oname=f"{odir}/box_unif_2500_seed{k:03d}.dat"
            joblist.write(f"{RUN} {nobj} {k} {oname}\n")
    joblist.close()
