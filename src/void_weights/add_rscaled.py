#!/usr/bin/env python
import sys
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()
SRC = os.environ.get('SRC')
sys.path.append(f"{SRC}/void_weights")
from apply_void_weights import batch_add_scaled_void_radii, get_numdens_from_matrix, get_numdens_radial

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} NGAL VOID_CAT(S)")
    
    ngal_fn = sys.argv[1]
    void_cat_fn_list = sys.argv[2:]
    print(f"==> Loading galaxy number density from {ngal_fn}")
    ngal = np.load(ngal_fn)
    batch_add_scaled_void_radii(void_cat_fn_list,
				get_dens_func=get_numdens_radial,
				#get_dens_func=get_numdens_from_matrix,
				n_matrix=ngal,
				overwrite=True,
				exponent = 0.213) #0.213 for postrecon, 0.236 for prerecon
