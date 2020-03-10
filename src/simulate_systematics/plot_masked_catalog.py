#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
names = ['x', 'y', 'z', 'w']
if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s CATALOG'%sys.argv[0])
  cat_fn = sys.argv[1]
  cat = pd.read_csv(cat_fn, delim_whitespace=True, names=names, usecols=(0,1,2,3))
  H, xedges, yedges = np.histogram2d(cat['x'].values, cat['y'].values, density=True, bins=(50, 50))
  H_w, xedges, yedges = np.histogram2d(cat['x'].values, cat['y'].values, density=True, bins=(50, 50), weights = cat['w'].values)
  vmin = min([np.min(H), np.min(H_w)])
  vmax = max([np.max(H), np.max(H_w)])
  fig, ax = plt.subplots(1, 2, sharey=True, figsize=(20, 8))
  X, Y = np.meshgrid(xedges, yedges)
  hm=ax[0].pcolormesh(X, Y, H.T, vmin=vmin, vmax=vmax)
  hw=ax[1].pcolormesh(X, Y, H_w.T, vmin=vmin, vmax=vmax)
  fig.colorbar(hm, ax=ax[0])
  fig.colorbar(hw, ax=ax[1])
  [a.set_xlabel(r'$X$ [Mpc]') for a in ax]
  [a.set_aspect('equal', 'box') for a in ax]
  ax[0].set_ylabel(r'$Y$ [Mpc]')
  plt.show()
