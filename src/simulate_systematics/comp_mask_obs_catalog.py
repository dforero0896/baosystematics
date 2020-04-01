#!/usr/bin/env python
import sys
import os
from comp_mask_catalog import comp_mask_catalog
from params import *
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(f"ERROR: Unexpected number of arguments\nUSAGE: {sys.argv[0]} INDIR MIN_COMP")
    filenames = sys.argv[1:-1]
    try:
        print(f"==> Using completeness from command line.")
        cmin_map = float(sys.argv[-1])
    except:
        sys.exit("ERROR: Please provide a completeness lower bound.")
    for f in filenames:
        odir = os.path.abspath(os.path.dirname(f)+'/../..')
        command=comp_mask_catalog(f, odir, noise_sampler=noise_sampler, function = parabola, cmin = cmin_map, N_grid = 2500, rmin = 16, rmax = 50, sigma_noise=0.2, cat_type='obs')
        print(command)
