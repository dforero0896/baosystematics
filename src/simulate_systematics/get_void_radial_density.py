#!/usr/bin/env python
import numpy as np
import pandas as pd
import dask.dataframe as dd
import dask.array as da
from dask.distributed import Client
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import os
from params import *
names = ['x', 'y', 'z', 'r', 'w', 'scaledr']
def get_histogram(cat, rmin, rmax, bins=20, weights = False):
  cat_bin = cat[(cat['r'] > rmin ) & (cat['r'] < rmax)]
  H, edges = da.histogram(cat_bin['z'].values, density=False, bins=bins, range = [[0, box_size], [0, box_size]])
  return H.compute(scheduler='processes'), edges

def histogram_from_partition(df):
  
  hist, edges = da.histogram(df['z'].values, bins=np.linspace(0, box_size, NGRID +1), density=True)
  return hist

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s CATALOG_DIR'%sys.argv[0])
  odir = os.path.abspath(f"{sys.argv[1]}/../plots")
  os.makedirs(odir, exist_ok=True)
  out_fn = f"{odir}/void_radial_density.npy"

  # Set values for subplot
  side_y = int(np.sqrt(len(radius_bins)-1))
  side_x = int((len(radius_bins)-1) / side_y)
  nrow = side_y
  ncol = side_x
  
  zedges = np.linspace(0, box_size, NGRID + 1)
  if not os.path.exists(out_fn):
    data = dd.read_csv(f"{sys.argv[1]}/*", delim_whitespace=True, names=['z', 'r'], usecols=[2, 3])
    #data = data.persist()
    data['rid'] = da.digitize(data['r'].values, bins=radius_bins, right=True)
    histograms=[]
    for i in range(len(radius_bins)-1):
      hist, edges = get_histogram(data, radius_bins[i], radius_bins[i+1], bins=zedges) 
      histograms.append(hist)
    histograms = np.array(histograms)
    np.save(out_fn, histograms)    
  else:
    histograms = np.load(out_fn)
  # Initialize Gridspec to familiar subplots sintaxis.
  fig = plt.figure(figsize=(ncol+1+0.2*ncol, nrow+1)) 
  spec = gridspec.GridSpec(nrow, ncol,
         wspace=0.0, hspace=0.45, 
         top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
         left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
  ax = np.empty((side_y, side_x), dtype=type(plt.axes))
  for i in range(ax.shape[0]):
    for k in range(ax.shape[1]):
      ax[i,k] = fig.add_subplot(spec[i, k])

  vmax = np.max(histograms)//500
  for i, a in enumerate(ax.ravel()):
    a.plot(histograms[i,:]/500, c = 'k')
    a.set_title("(%.0f, %.0f)"%(radius_bins[i], radius_bins[i+1]), fontsize = 10)
    a.set_xlim(0, 2500)
    a.set_ylim(0,vmax)
  fig.add_subplot(111, frameon=False)
  plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

  #fig.text(0.5, 0.04, '$Z$ [Mpc/$h$]', ha='center')
  #fig.text(0.04, 0.5, 'Void number', va='center', rotation='vertical')
  plt.xlabel('$Z$ [Mpc/$h$]', labelpad=25)
  plt.ylabel('Void number', labelpad=55)
  [a.set_xticks([1250]) for a in ax.ravel()]
  plt.setp([a.get_yticklabels() for a in ax[:,1:].ravel()], visible=False)
  plt.setp([a.get_xticklabels() for a in ax[:-1, :].ravel()], visible=False)

  oname = f"{odir}/all_void_radial_density.pdf"
   
  fig.savefig(oname, dpi=300, bbox_inches = "tight")
  print(f"Saved plot in {oname}")
