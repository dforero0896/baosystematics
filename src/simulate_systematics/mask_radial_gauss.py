#!/usr/bin/env python
from mask_comp_func import mask_radial_gauss
import pandas as pd
import numpy as np
import os
import sys
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get('WORKDIR')

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        sys.exit(f"USAGE: {sys.argv[0]} IN_CATALOG OUT_CATALOG")
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    data = pd.read_csv(ifile, delim_whitespace=True, usecols=(0,1,2), 
			names=['x', 'y', 'z'], dtype=np.float32)
    masked=mask_radial_gauss(data)
    masked.to_csv(ofile, header=False, index=False, sep=" ")


