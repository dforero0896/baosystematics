#!/usr/bin/env python
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')



if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} CATALOG_1 [CATALOG_2 ... CATALOG_N] OUTDIR")
    catalog_fn = sys.argv[1:-1]
    odir = sys.argv[-1]
    os.makedirs(odir, exist_ok=True)
    obin = f"{odir}/void_radii_distribution.npy"
    radius_bins = np.append(np.linspace(0, 35, 71), [50])
    nbins = 100
    if not os.path.isfile(obin):
        radii_dist = np.empty([len(catalog_fn), nbins, 2])
        for i, fn in enumerate(catalog_fn):
            print(f"==> Reading file: {fn}")
            data = pd.read_csv(fn, header=None, delim_whitespace=True, usecols=[3], names=['r'])
            hist, bin_edges = np.histogram(data['r'].values, bins=nbins, density=True, range=[0, 50])
            delta_r = bin_edges[1:] - bin_edges[:-1]
            bin_centers = bin_edges[:-1] + 0.5 * delta_r
            radii_dist[i,:,1] = hist
            radii_dist[i,:,0] = bin_centers
        np.save(obin, radii_dist)
    else: 
        radii_dist = np.load(obin)
    avg_dist = radii_dist[:,:,1].mean(axis=0)
    std_dist = radii_dist[:,:,1].std(axis=0)
    bin_centers = radii_dist[0,:,0]
    fig, ax = plt.subplots(1, 1)
    ax.plot(bin_centers, avg_dist, c = 'k')
    ax.fill_between(bin_centers, avg_dist - std_dist, avg_dist + std_dist, alpha=0.2, color = 'k')
    ax.set_xlabel(r'$R$ [$h^{-1}$ Mpc]', fontsize=12)
    ax.set_ylabel('Void number density', fontsize=12)
    
    fig.tight_layout()

    fig.savefig(f"{odir}/void_radii_distribution.pdf", dpi=200)
