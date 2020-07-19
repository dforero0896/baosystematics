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
def bin_to_ascii(idir, odir):
    cat = Halos.make_catalog_from_dir(dirname=idir,
                                  load_subsamples=False, load_pids=False)
    halos = cat.halos
    data=pd.DataFrame(cat.halos['pos'])
    data.to_csv(odir, sep=" ", header=False, index=False)
    

if __name__=='__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--idir', required=False, help='Directory where Abacus catalogs are located.')
    parser.add_argument('-o', '--odir', required=True, help='Directory to save ASCII Abacus catalogs.')

    parsed = parser.parse_args()
    args = vars(parsed)
    print(glob.glob(f"{args['idir']}/*/*/*/*"))
