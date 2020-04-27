#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys
import os
WORKDIR = '/hpcstorage/dforero/projects/baosystematics'
sys.path.append(f"{WORKDIR}/src/simulate_systematics")
from params import *
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
			 out_dir_suffix='_wt', save=True, overwrite=False, **kwargs):
    """Apply void weights as a function of galaxy weights.
   """ 
    
    if out_cat_fn is None: out_cat_fn = os.path.dirname(void_cat_fn)+\
				out_dir_suffix+"/"+os.path.basename(void_cat_fn)
    if os.path.isfile(out_cat_fn) and not overwrite:
        print(f"==> File {out_cat_fn} already exists")
        return 0
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

def add_scaled_void_radii(void_cat_fn, get_dens_func, out_cat_fn = None,
			 out_dir_suffix='_scaledR', save=True, 
			 overwrite=False, **kwargs):
    """Add column with scaled void radii.
   """ 
    
    if out_cat_fn is None: out_cat_fn = os.path.dirname(void_cat_fn)+\
				out_dir_suffix+"/"+os.path.basename(void_cat_fn)
    if os.path.isfile(out_cat_fn) and not overwrite:
        print(f"==> File {out_cat_fn} already exists")
        return 0
    # Import data
    print(f"==> Reading {void_cat_fn}")
    void_cat = pd.read_csv(void_cat_fn, delim_whitespace = True,\
			 names = ['x', 'y', 'z', 'r', 'w'],\
			 dtype=np.float32)
    void_cat.dropna(axis=1, inplace=True)
    print(f"==> Computing local halo density with {get_dens_func.__name__}")
    ngal = get_dens_func(void_cat['x'], void_cat['y'], void_cat['z'],
				**kwargs)
    void_cat['scaledR'] = ngal**(1./4) * void_cat['r']
    
    if save:
        print(f"==> Saving catalog to {out_cat_fn}")
        os.makedirs(os.path.dirname(out_cat_fn), exist_ok=True)
        void_cat.to_csv(out_cat_fn, index=False, header = False, sep = ' ',\
			 float_format='%.5f')
        print("==> Done")
    return void_cat

def batch_add_void_weights(void_cat_fn_list, get_weights_func, 
				out_dir_suffix = '_wt', overwrite=False, **kwargs):
    

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
			out_cat_fn = None, save=True, overwrite=overwrite, **kwargs)
    print(f"==> MPI process {rank} finished.")
    MPI.Finalize()

def batch_add_scaled_void_radii(void_cat_fn_list, get_dens_func, 
				out_dir_suffix = '_scaledR', overwrite=False, **kwargs):
    

    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    if rank ==0 : print(f"==> Using {size} processes.")
    void_cat_chunk_fn = np.array_split(void_cat_fn_list, size)[rank]
    print(f"==> MPI process {rank} has {len(void_cat_chunk_fn)} jobs allocated.")
    for void_cat_fn in void_cat_chunk_fn:
        add_scaled_void_radii(void_cat_fn, get_dens_func, 
			out_dir_suffix = out_dir_suffix,
			out_cat_fn = None, save=True, overwrite=overwrite, **kwargs)
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
    """Convert bin edges to centers.

    params: edges (1d array, dim N): Bin edges
   
    returns: centers (1d array, dim N-1): Bin centers
    returns: widths (1d array, dim N-1): Bin widths"""


    widths = edges[1:] - edges[:-1]
    centers = edges[:-1] + 0.5 * widths
    return centers, widths
def get_known_void_weight_matrix(raw_void_dist_fn, void_dist_fn):
    """Get void weight matrix from 3D (R, X, Y) arrays of void density.

    param: raw_void_dist_fn (str): Path to the (R, X, Y) void distribution of voids
	without systematics applied.
    param: void_dist_fn (str): Path to the (R, X, Y) void distribution of voids
	with systematics applied.

    returns: void_weight_matrix (3d array): The void weight matrix constructed as
	raw_void_dist/void_dist (inverse void completeness). Coordinates are (R,X,Y).

    """
    raw_void_dist = np.load(raw_void_dist_fn)
    print(f"Loaded raw void distribution from {raw_void_dist_fn}")
    void_dist = np.load(void_dist_fn)
    print(f"Loaded new void distribution from {void_dist_fn}")
    void_weight_matrix = raw_void_dist / void_dist
    np.nan_to_num(void_weight_matrix, copy=False, nan=0., posinf=0, neginf=0)
    return void_weight_matrix

def get_known_void_weight(r, x, y, void_weight_matrix, 
				radius_bins = radius_bins,
				xedges = xedges, yedges=yedges):
    """Get void weight by sampling the matrix of known weights (see function: 
	get_known_void_weight_matrix).

    param: r (array_like): Radius of void to be weighted.
    param: x (array_like): X-coordinate of void to be weighted.
    param: y (array_like): Y-coordinate of void to be weighted.
    param: radius_bins (1d array, optional): Radius bin-edges used when creating the 
	matrices (R, X, Y).
    param: xedges (1d array, optional): X-coordinate bin-edges used when creating the 
	matrices (R, X, Y).
    param: yedges (1d array, optional): Y-coordinate bin-edges used when creating the 
	matrices (R, X, Y).

    returns: void_weight (array_like): The weight to be applied to the void at position
	(x,y) and radius r.
    """

    # Clip arrays to bin edges for (dimension-wise) "nearest" extrapolation.
    r=np.clip(r, radius_bins[0], radius_bins[-1])
    side='left'
    # Extend leftmost bin edge for the (very unlikely) case that some void has
    # any([r, x, y] == [0, 0, 0]). The rightmost edge is also extended to make
    # sure clipped values are included.
    radius_bins[0]-=1e-5; radius_bins[-1]+=1e-5
    xedges[0]-=1e-5; xedges[-1]+=1e-5
    yedges[0]-=1e-5; yedges[-1]+=1e-5
    # Search indices that define which bin a coordinate corresponds to.
    rindex = np.searchsorted(radius_bins, r, side=side) -1
    xindex = np.searchsorted(xedges, x, side=side)  -1
    yindex = np.searchsorted(yedges, y, side=side) -1
    return void_weight_matrix[rindex, xindex, yindex]

def get_numdens_from_matrix(x, y, z, n_matrix, box_size=box_size, N_grid=NGRID):
    """Get tracer number density  by sampling the matrix of number densities.

    param: x (array_like): X-coordinate of void to be weighted.
    param: y (array_like): Y-coordinate of void to be weighted.
    param: xedges (1d array, optional): X-coordinate bin-edges used when creating the 
	matrices (R, X, Y).
    param: yedges (1d array, optional): Y-coordinate bin-edges used when creating the 
	matrices (R, X, Y).

    returns: ntracer (array_like): The local tracer number density at point (x,y).
    """

    xedges = np.linspace(0, box_size, N_grid+1)
    yedges = np.linspace(0, box_size, N_grid+1)
    # Clip arrays to bin edges for (dimension-wise) "nearest" extrapolation.
    side='left'
    # Extend leftmost bin edge for the (very unlikely) case that some void has
    # any([x, y] == [0, 0]). The rightmost edge is also extended to make
    # sure clipped values are included.
    xedges[0]-=1e-5; xedges[-1]+=1e-5
    yedges[0]-=1e-5; yedges[-1]+=1e-5
    # Search indices that define which bin a coordinate corresponds to.
    xindex = np.searchsorted(xedges, x, side=side)  -1
    yindex = np.searchsorted(yedges, y, side=side) -1
    xcenters, xwidths = edges_to_centers(xedges)    
    ycenters, ywidths = edges_to_centers(yedges)  
    x_width = xwidths[xindex]
    y_width = ywidths[yindex]
    nvals=n_matrix[xindex, yindex]
    nvals/=(box_size * x_width * y_width)
    return nvals 

def get_numdens_radial(x, y, z, n_matrix, box_size = box_size, N_grid=NGRID):

    zedges = np.linspace(0, box_size, N_grid + 1)
    zedges[0]-=1e-5; zedges[-1]+=1e-5
    side='left'
    zindex = np.searchsorted(zedges, z, side=side)  -1
    zcenters, zwidths = edges_to_centers(zedges)    
    nvals = n_matrix[zindex]
    nvals/=(box_size * box_size * zwidths[zindex])
    return nvals 
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} RAW_VOID_DENS VOID_DENS VOID_CAT(S)")
    raw_void_dens_fn = sys.argv[1]
    void_dens_fn = sys.argv[2]
    void_cat_fn_list = sys.argv[3:]
    void_weight_matrix =\
		 get_known_void_weight_matrix(raw_void_dens_fn, void_dens_fn)
    void_wt_coeff_fn = 'void_weights_c_of_r_real.dat' 
    void_wt_coeff = np.loadtxt(void_wt_coeff_fn, dtype = np.float32)
    rc, rw = edges_to_centers(radius_bins)
    xc, xw = edges_to_centers(xedges)
    yc, yw = edges_to_centers(yedges)
    # Use weights directly from weight matrix
    batch_add_void_weights(void_cat_fn_list, get_weights_func=get_known_void_weight,
				 void_weight_matrix=void_weight_matrix, overwrite=False)
    # Use interpolation for coefficients and anytical galaxy completeness
#    batch_add_void_weights(void_cat_fn_list, get_void_weights_interp, 
#			coeffs=void_wt_coeff, 
#			comp_function = lambda y, x: FUNCTION(y, x, N_grid=2500,
#			Cmin = 0.8))

