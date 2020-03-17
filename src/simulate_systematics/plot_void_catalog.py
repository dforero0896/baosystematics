#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
names = ['x', 'y', 'z', 'r']
def get_histogram(cat, rmin, rmax):
#  print('Initial number of objects %i'%len(cat))
  cat_bin = cat[(cat['r'] > rmin ) & (cat['r'] < rmax)]
#  print('New number of objects %i'%len(cat_bin))
  H, xedges, yedges = np.histogram2d(cat_bin['x'].values, cat_bin['y'].values, density=True, bins=(20, 20))
  return H, xedges, yedges
if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s CATALOG'%sys.argv[0])
  cat_fn = sys.argv[1]
  cat = pd.read_csv(cat_fn, delim_whitespace=True, names=names, usecols=(0,1,2,3))
  radius_bins = np.append(np.linspace(0, 21, 13), [25, 30, 50])
  side_x = int(np.sqrt(len(radius_bins)-1))
  side_y = int((len(radius_bins)-1) / side_x)
  nrow = side_y
  ncol = side_x
  fig = plt.figure(figsize=(ncol+1, nrow+1)) 
  spec = gridspec.GridSpec(nrow, ncol,
           wspace=0.0, hspace=0.45, 
           top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1), 
           left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
  ax = np.empty((side_x, side_y), dtype=type(plt.axes))
  for i in range(ax.shape[0]):
    for k in range(ax.shape[1]):
      ax[i,k] = fig.add_subplot(spec[k, i])
  histograms = []
  mins = []
  maxs = []
  for i, a in enumerate(ax.ravel()):
    hist, xedges, yedges = get_histogram(cat, radius_bins[i], radius_bins[i+1])
    histograms.append(hist)
    mins.append(np.min(hist))
    maxs.append(np.max(hist))
    a.set_title("(%.0f, %.0f)"%(radius_bins[i], radius_bins[i+1]), fontsize = 6)
  vmin = min(mins)
  vmax = max(maxs)
  X, Y = np.meshgrid(xedges, yedges)
  for a, hist in zip(ax.ravel(), histograms):
    h=a.pcolormesh(X, Y, hist)
#    cb=fig.colorbar(h, ax=a)#x.ravel().tolist())
#    cb.ax.tick_params(labelsize=6)
#  [a.set_xlabel(r'$X$ [Mpc]') for a in ax[-1,:]]
  [a.set_aspect('equal', 'box') for a in ax.ravel()]
#  [a.set_ylabel(r'$Y$ [Mpc]') for a in ax[:,0]]
  plt.setp([a.get_yticklabels() for a in ax.ravel()], visible=False)
  plt.setp([a.get_xticklabels() for a in ax.ravel()], visible=False)
  plt.show()
