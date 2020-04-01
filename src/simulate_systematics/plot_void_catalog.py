#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import os
from params import *
names = ['x', 'y', 'z', 'r']
def get_histogram(cat, rmin, rmax, bins=20, weights = None):
  cat_bin = cat[(cat['r'] > rmin ) & (cat['r'] < rmax)]
  H, xedges, yedges = np.histogram2d(cat_bin['x'].values, cat_bin['y'].values, density=False, bins=(bins, bins), range = [[0, box_size], [0, box_size]], weights = weights)
  return H, xedges, yedges
if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s CATALOG'%sys.argv[0])
  from mpi4py import MPI
  comm = MPI.COMM_WORLD # Communicator
  nproc = comm.Get_size()   # Size of communicator
  iproc = comm.Get_rank()   # Ranks in communicator
  inode = MPI.Get_processor_name()    # Node where this MPI process runs
  odir = os.path.abspath(f"{os.path.dirname(sys.argv[1])}/../plots")
  try:
    if iproc==0: os.makedirs(odir, exist_ok=True)
  except:
    odir = '.'
  out_fn = f"{odir}/void_density_map.npy"
  radius_bins = np.append(np.linspace(0, 21, 22), [25, 30, 50])
  xy_bins = 256

  # Set values for subplot
  side_x = int(np.sqrt(len(radius_bins)-1))
  side_y = int((len(radius_bins)-1) / side_x)
  nrow = side_y
  ncol = side_x
  # List of input catalogs
  catalogs = sys.argv[1:]
  # List of input catalogs per process
  catalogs_split = np.array_split(catalogs, nproc)
  # Weights for final average.
  hist_weights =  [len(c) for c in catalogs_split]
  cat_array_all = None

  if iproc == 0:
    print(hist_weights)
    # Initialize Gridspec to familiar subplots sintaxis.
    fig = plt.figure(figsize=(ncol+1+0.2*ncol, nrow+1)) 
    spec = gridspec.GridSpec(nrow, ncol,
           wspace=0.0, hspace=0.45, 
           top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
           left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
    ax = np.empty((side_x, side_y), dtype=type(plt.axes))
    for i in range(ax.shape[0]):
      for k in range(ax.shape[1]):
        ax[i,k] = fig.add_subplot(spec[k, i])
    # Create recieving buffer
    cat_array_all = np.empty([nproc, len(radius_bins)-1, xy_bins, xy_bins], dtype= np.float32)

  # Create send buffers
  cat_arrays = np.empty((len(radius_bins)-1, xy_bins, xy_bins, len(catalogs_split[iproc])), dtype=np.float32)
  # Bottleneck
  if not os.path.exists(out_fn):
    if iproc==0: print(f"==> Computing histogram with {nproc} processes.")
    for nmock, cat_fn in enumerate(catalogs_split[iproc]):
      print(f"==> MPI process {iproc}: {cat_fn}")
      cat = pd.read_csv(cat_fn, delim_whitespace=True, names=['x', 'y', 'r'], usecols=(0,1,3), dtype=np.float32)
      for i, lbound in enumerate(radius_bins[:-1]):
        hist, xedges, yedges = get_histogram(cat, radius_bins[i], radius_bins[i+1], bins = xy_bins)
        cat_arrays[i, :, :, nmock] = hist
    pmean = cat_arrays.mean(axis=3)
    print(f"==> MPI process {iproc} waiting for the others.")
    comm.Barrier()
  
    if iproc==0: print(f"==> MPI process 0 gathering data.")
    comm.Gather(pmean, cat_array_all, root=0)  
    if iproc==0:
      histograms = np.average(cat_array_all, axis=0, weights = hist_weights)
      print(f"==> MPI process 0 saving file.")
      np.save(out_fn, histograms)    
  else:
    if iproc==0:
      print(f"==> Loading data from {out_fn}.")
      histograms = np.load(out_fn)
      print(f"==> Done")
  if iproc==0:
    xedges = np.linspace(0, box_size, xy_bins+1)
    yedges = np.linspace(0, box_size, xy_bins+1)
    X, Y = np.meshgrid(xedges, yedges)
    abs_vmin = np.min(histograms)
    abs_vmax = np.max(histograms)
    for i, a in enumerate(ax.ravel()):
      bin_hist =  histograms[i, :, :]
      bin_hist -= np.min(bin_hist)
      bin_hist/=np.max(bin_hist)
      vmin, vmax, mean = np.min(bin_hist), np.max(bin_hist), np.mean(bin_hist)
      h=a.pcolorfast(X, Y, bin_hist, vmin=abs_vmin, vmax=vmax, cmap = plt.get_cmap('hot'))
      h.set_rasterized(True)
      a.set_title("(%.0f, %.0f)"%(radius_bins[i], radius_bins[i+1]), fontsize = 6)
      a.set_ylabel("(%.1f, %.1f)"%(vmin/vmax, mean/vmax), fontsize=6)
      a.set_aspect('equal', 'box')
    cb=fig.colorbar(h, ax=ax.ravel().tolist())
  #    cb.ax.tick_params(labelsize=6)
  #  [a.set_xlabel(r'$X$ [Mpc]') for a in ax[-1,:]]
  #  [a.set_ylabel(r'$Y$ [Mpc]') for a in ax[:,0]]
    plt.setp([a.get_yticklabels() for a in ax.ravel()], visible=False)
    plt.setp([a.get_xticklabels() for a in ax.ravel()], visible=False)
  #  plt.show()
    fig.savefig(f"{odir}/all_void_density_maps.pdf", dpi=300)
    print(f"Saved plot in {odir}.")
  MPI.Finalize()
