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
from scipy.interpolate import NearestNDInterpolator, RegularGridInterpolator

def add_void_weights_interp(void_cat_fn, void_wt_coeff_fn, comp_function, 
			out_cat_fn = None,
			save=True):
    """Apply void weights as a function of galaxy weights.
   """ 
    if out_cat_fn is None: out_cat_fn = os.path.dirname(void_cat_fn)+\
					"_wt/"+os.path.basename(void_cat_fn)
    # Import data
    print(f"==> Reading {void_cat_fn}")
    void_cat = pd.read_csv(void_cat_fn, delim_whitespace = True,\
			 usecols=(0, 1, 2, 3), names = ['x', 'y', 'z', 'r'],\
			 dtype=np.float32)
    void_wt_coeff = np.loadtxt(void_wt_coeff_fn, dtype = np.float32) 
    print(f"==> Computing void weights")
    void_wt = get_void_weights_interp(void_cat, void_wt_coeff, comp_function)
    void_cat['w'] = void_wt
    if save:
        print(f"==> Saving catalog to {out_cat_fn}")
        os.makedirs(os.path.dirname(out_cat_fn), exist_ok=True)
        void_cat.to_csv(out_cat_fn, index=False, header = False, sep = ' ',\
			 float_format='%.5f')
        print("==> Done")
    return void_cat

def add_void_weights(void_cat_fn, get_weights_func, out_cat_fn = None,
			 out_dir_suffix='_wt', save=True, **kwargs):
    """Apply void weights as a function of galaxy weights.
   """ 
    
    if out_cat_fn is None: out_cat_fn = os.path.dirname(void_cat_fn)+\
				out_dir_suffix+"/"+os.path.basename(void_cat_fn)
    # Import data
    print(f"==> Reading {void_cat_fn}")
    void_cat = pd.read_csv(void_cat_fn, delim_whitespace = True,\
			 usecols=(0, 1, 2, 3), names = ['x', 'y', 'z', 'r'],\
			 dtype=np.float32)
    print(f"==> Computing void weights with {get_weights_func.__name__}")
    void_wt = get_weights_func(void_cat['r'], void_cat['x'], void_cat['y'], 
				**kwargs)
    void_cat['w'] = void_wt
    if save:
        print(f"==> Saving catalog to {out_cat_fn}")
        os.makedirs(os.path.dirname(out_cat_fn), exist_ok=True)
        void_cat.to_csv(out_cat_fn, index=False, header = False, sep = ' ',\
			 float_format='%.5f')
        print("==> Done")
    return void_cat

def batch_add_void_weights(void_cat_fn_list, get_weights_func, 
				out_dir_suffix = '_wt', **kwargs):
    

    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    if rank ==0 : print(f"==> Using {size} processes.")
    void_cat_chunk_fn = np.array_split(void_cat_fn_list, size)[rank]
    print(f"==> MPI process {rank} has {len(void_cat_chunk_fn)} jobs allocated.")
    for void_cat_fn in void_cat_chunk_fn:
        add_void_weights(void_cat_fn, get_weights_func, 
			out_dir_suffix = out_dir_suffix,
			out_cat_fn = None, save=True, **kwargs)
    print(f"==> MPI process {rank} finished.")
    MPI.Finalize()

def get_void_weights_interp(r, x, y, coeffs, comp_function):
    """Compute void weights from galaxy completeness(= 1/galaxy_weight)

    """

    c0 = np.interp(r, coeffs[:,0], coeffs[:,1])
    c1 = np.interp(r, coeffs[:,0], coeffs[:,2])
    c2 = np.interp(r, coeffs[:,0], coeffs[:,3])
    gal_wt = (comp_function(y, x))**(-1)
    return c0 + c1 * gal_wt + c2 * gal_wt**2

def edges_to_centers(edges):
    widths = edges[1:] - edges[:-1]
    centers = edges[:-1] + 0.5 * widths
    return centers, widths
def get_known_void_weight_matrix(raw_void_dist_fn, void_dist_fn, 
				radius_bins = radius_bins,
				xedges = xedges, yedges=yedges):
    """Get void weight matrix from R-binned arrays of void number 
	density/void completeness

    """
    raw_void_dist = np.load(raw_void_dist_fn)
    void_dist = np.load(void_dist_fn)
    rcenters,_ = edges_to_centers(radius_bins)
    xcenters,_ = edges_to_centers(xedges)
    ycenters,_ = edges_to_centers(yedges)
    R, X, Y = np.meshgrid(rcenters, xcenters, ycenters)
    R = R.ravel(); X = X.ravel(); Y = Y.ravel()
    
    assert void_dist.shape[0] == rcenters.shape[0]    
    assert raw_void_dist.shape[0] == rcenters.shape[0]    
    
    void_weight_matrix = raw_void_dist / void_dist
    # Nearest interpolation returns closest value.
    void_weight_interpolator = NearestNDInterpolator((R, X, Y),
					 void_weight_matrix.ravel())

    return lambda r, x, y: void_weight_interpolator((r, x, y)), void_weight_matrix

def get_known_void_weight(r, x, y, void_weight_matrix, rcenters, xcenters, ycenters):
    """Get void weights from matrix and void position.

    """
    N_grid_r, N_grid_x, N_grid_y = void_weight_matrix.shape
    iy = np.abs(y[:,None].astype(np.float32) -\
		ycenters[None,:].astype(np.float32)).argmin(axis=-1)
    ix = np.abs(x[:,None].astype(np.float32) -\
		xcenters[None,:].astype(np.float32)).argmin(axis=-1)
    ir = np.abs(r[:, None].astype(np.float32) -\
		rcenters[None,:].astype(np.float32)).argmin(axis=-1)
    return void_weight_matrix[ir, ix, iy]
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} RAW_VOID_DENS VOID_DENS VOID_CAT(S)")
    raw_void_dens_fn = sys.argv[1]
    void_dens_fn = sys.argv[2]
    void_cat_fn_list = sys.argv[3:]
    void_weight_nearest, void_weight_matrix =\
		 get_known_void_weight_matrix(raw_void_dens_fn, void_dens_fn)
    void_wt_coeff_fn = 'void_weights_c_of_r_real.dat' 
    void_wt_coeff = np.loadtxt(void_wt_coeff_fn, dtype = np.float32)
    rc, rw = edges_to_centers(radius_bins)
    xc, xw = edges_to_centers(xedges)
    yc, yw = edges_to_centers(yedges)
    #batch_add_void_weights(void_cat_fn_list, get_weights_func=get_known_void_weight_matrix, void_weight_matrix=void_weight_matrix, rcenters=rc, xcenters=xc, ycenters=yc)
    batch_add_void_weights(void_cat_fn_list, void_weight_nearest,
    			 out_dir_suffix='_wt_nearest')

#    batch_add_void_weights(void_cat_fn_list, get_void_weights_interp, 
#			coeffs=void_wt_coeff, 
#			comp_function = lambda y, x: FUNCTION(y, x, N_grid=2500,
#			Cmin = 0.8))

