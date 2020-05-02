#!/usr/bin/env python
import sys
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#import modin.pandas as pd
import pandas as pd
from params import *
def plot_all_histograms(histograms, bin_edges, ax, color='k', xlabel='', ylabel='', fontsize=15, function=parabola):
    delta_x = bin_edges[1] - bin_edges[0]
    bin_x = (bin_edges + 0.5 * delta_x)[:-1]
    # Compute volume of rings for normalization
#    bin_volumes = (4 * np.pi ) * np.array([((r+delta_x)**2 - r**2) for r in bin_edges[:-1]])
#    histograms= histograms / bin_volumes[:, None]
#    histograms/=np.max(histograms, axis=0)
    mean_counts = histograms.mean(axis=1)
    std_counts = histograms.std(axis=1)
    
    ax.fill_between(bin_x, mean_counts - std_counts, mean_counts + std_counts, alpha=0.5, color=color)
    ax.plot(bin_x, mean_counts, color = color)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_xlim(0, box_size/2)
def plot_map(X, Y, image, ax, fontsize=15):
    img = ax.pcolormesh(X,Y, image)
    img.set_rasterized(True)
    plt.colorbar(img, ax=ax)
    ax.set_aspect('equal')
    ax.set_xlabel(r'$x$ [$h^{-1}$ Mpc]', fontsize=fontsize)
    ax.set_ylabel(r'$y$ [$h^{-1}$ Mpc]', fontsize=fontsize)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s COMP_FUNC CATALOG'%sys.argv[0])
    funcname = sys.argv[1]
    for i in funclist:
       if funcname == i.__name__:
           function = i
           print(f"Using completeness {function.__name__}.")
           break
#       else:
#           sys.exit("ERROR: Function not recognized, use %s"%funclist)
    catalogs = sys.argv[2:]
    xedges = np.linspace(0, box_size, box_size+1)
    yedges = xedges
    xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
    ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
    xybins= box_size
    rbins = 100
    rbin_edges = np.linspace(0, rbins, rbins+1)
    rbin_centers = rbin_edges[:-1] + 0.5 * (rbin_edges[1:] - rbin_edges[:-1])
    cat_arrays = np.empty((xybins, xybins, len(catalogs)))
    odir = os.path.abspath(f"{os.path.dirname(catalogs[0])}/../plots")
    os.makedirs(odir, exist_ok=True)
    oname = f"{odir}/galaxy_spherical_distribution.dat"
    if True:#:not os.path.exists(oname):
        r_hist = np.empty((rbins, len(catalogs)))
        for i, catalog in enumerate(catalogs):
            cat = pd.read_csv(catalog, delim_whitespace=True, names = ['x', 'y', 'w'], usecols=(0,1,3))
            hist, xedges, yedges = np.histogram2d(cat['x'].values, cat['y'].values, bins = (xedges, yedges)) 
            cat_arrays[:, :, i] = hist
            # Compute raw density
            # Compute raw density
            raw_density = cat['w'].sum() / box_size**2 # 2D density
            # Compute the r coordinate for each object on the angular plane.
            cat['r'] = np.sqrt((cat['x'] - 0.5 * box_size)**2 + (cat['y'] - 0.5 * box_size)**2)
            r_hist[:,i], bin_edges = np.histogram(cat['r'].values, bins=rbin_edges, density = False)
            # Compute expected number of objects per bin
            c_analytical= function(box_size/2 * np.ones(len(bin_edges[:-1])), box_size/2 + bin_edges[:-1], box_size, cmin_map) # Completeness
            expected_histogram = raw_density * 4*np.pi*(bin_edges[1:]**2 - bin_edges[:-1]**2)# * c_analytical 
            r_hist[:,i]/=expected_histogram # Normalized by analytical estimate
        np.savetxt(oname, r_hist)
        np.save(f"{odir}/ngal.npy", cat_arrays)
    else:
        cat_arrays = np.load(f"{odir}/ngal.npy")
        r_hist = np.loadtxt(oname)
        bin_edges = rbin_edges
    rfig, rax = plt.subplots(1,1)
    plot_all_histograms(r_hist, bin_edges, ax=rax, xlabel=r'Distance from center [$h^{-1}$ Mpc]', ylabel='Number density')
    c_analytical= function(box_size/2 * np.ones(len(bin_edges[:-1])), box_size/2 + bin_edges[:-1], box_size, cmin_map)
    rax.plot(bin_edges[:-1],c_analytical, c = 'r', ls = '--')
    rfig.tight_layout()
    rfig.savefig(f"{odir}/galaxy_spherical_distribution.pdf", dpi=200)
    print(f"==> Saved {odir}/galaxy_spherical_distribution.pdf")
    X, Y  = np.meshgrid(xcenters, ycenters)
    hist = cat_arrays.mean(axis=2)
    hist/=np.max(hist)
    comp_func = function(Y, X, box_size, cmin_map)
    diff = hist - comp_func
    fig, ax = plt.subplots(1, 1)
    plot_map(X, Y, diff , ax=ax)
    fig.tight_layout()
    fig.savefig(f"{odir}/ngal-comp.pdf", dpi=200)
    print(f"==> Saved {odir}/ngal-comp.pdf")

