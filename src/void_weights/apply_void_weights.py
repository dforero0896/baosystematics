#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys
import os
WORKDIR = '/hpcstorage/dforero/projects/baosystematics'
sys.path.append(f"{WORKDIR}/src/simulate_systematics")
from params import *
from plot_void_catalog import get_histogram
import matplotlib.pyplot as plt

def add_void_weights(void_cat, comp_function):
    '''Apply void weights as a function of galaxy weights.

    void_cat (pandas DataFrame): Void catalog to add weights to. Columns x, y, z, r
    comp_function (callable): Void weight as a function of void radius and tracer position. w_v = function(y, x, r)'''
    
    void_cat['w'] = comp_function(void_cat['y'], void_cat['x'], void_cat['r'])
    return void_cat

def get_void_weights(void_cat, coeffs, comp_function):
    c0 = np.interp(void_cat['r'], coeffs[:,0], coeffs[:,1])
    c1 = np.interp(void_cat['r'], coeffs[:,0], coeffs[:,2])
    c2 = np.interp(void_cat['r'], coeffs[:,0], coeffs[:,3])
    gal_wt = (comp_function(void_cat['y'], void_cat['x']))**(-1)
    return c0 + c1 * gal_wt + c2 * gal_wt**2
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} VOID_WT_COEFF VOID_CAT OUT_VOID_CAT")
    void_wt_coeff_fn = sys.argv[1]
    void_cat_fn = sys.argv[2]
    out_cat_fn = sys.argv[3]
    os.makedirs(os.path.dirname(out_cat_fn), exist_ok=True)
    # Import data
    print(f"==> Reading {void_cat_fn}")
    void_cat = pd.read_csv(void_cat_fn, delim_whitespace = True, usecols=(0, 1, 2, 3), names = ['x', 'y', 'z', 'r'], dtype=np.float32)
    void_wt_coeff = np.loadtxt(void_wt_coeff_fn, dtype = np.float32) 
    print(f"==> Computing void weights")
    void_wt = get_void_weights(void_cat, void_wt_coeff, lambda y, x: flat(y, x, N_grid=2500, Cmin = 0.8))
    void_cat['w'] = void_wt
    print(f"==> Saving catalog to {out_cat_fn}")
    void_cat.to_csv(out_cat_fn, index=False, header = False, sep = ' ', float_format='%.5f')
    print("==> Done")

