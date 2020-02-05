#!/usr/bin/env python
import numpy as np
from scipy import stats
import sys
import os
from getdist import plots, MCSamples
WORKDIR ='/hpcstorage/dforero/projects/baosystematics' 
ALL_RESULTS = os.path.join(WORKDIR, 'results/allsyst_v7')
NO_RESULTS = os.path.join(WORKDIR, 'results/nosyst_v7')
systresults = {'allsyst': ALL_RESULTS, 'nosyst':NO_RESULTS}
def mcsamples_alpha(cap, systkey='nosyst'):
    cases = ['gal_w', 'gal_nw', 'void']
    labels = [r'\alpha_{\mathrm{gal, w}}', r'\alpha_{\mathrm{gal, now}}', r'\alpha_{\mathrm{void}}']
    cases_files = [os.path.join(systresults[systkey], s) for s in ['baofit/individual_combined_gal/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_gal_nowt/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_void/alpha_samples_%s.dat'%cap]]
    print([np.loadtxt(f, usecols=0).shape for f in cases_files])
    cases_data = np.stack([np.loadtxt(f, usecols=0) for f in cases_files], axis = 1)
    samples = MCSamples(samples = cases_data, names = cases, labels = labels) 
    return samples, cases_data
def plot_triplot(samples_list, label_list, **kwargs):
    g = plots.get_subplot_plotter()
    g.triangle_plot(samples_list, legend_labels = label_list, filled=False, **kwargs)
    return g
def plot_clouds(gplot, data, **kwargs):
    for row in range(data.shape[1]):
        for col in range(row):
            gplot.subplots[row, col].plot(data[:,col],data[:,row], 'o', **kwargs)
            gplot.subplots[row, col].axhline(1, ls = ':', lw=1.5, c='k')

def plot_hist(gplot, data, **kwargs):
    for row in range(data.shape[1]):
        n, _, _ = gplot.subplots[row, row].hist(data[:,row], density=True, histtype='step',**kwargs)
        if gplot.subplots[row,row].get_ylim()[-1] < max(n)+1:
            gplot.subplots[row,row].set_ylim(0, max(n)+1)

if __name__=='__main__':
    samples_no, data_no = mcsamples_alpha('cbz', 'nosyst')
    samples_all, data_all = mcsamples_alpha('cbz', 'allsyst')
    g = plot_triplot([samples_no, samples_all], ['No Syst.', 'All Syst.'], contour_colors=['b', 'r'], contour_lws=[3, 3], contour_args={'alpha':0}, line_args = {'alpha':0})
#    [ax.clear() for ax in g.subplots.ravel() if ax != None]
    plot_clouds(g, data_no, c='b', alpha=0.5, markersize=3)
    plot_hist(g, data_no, bins=20, color='b',lw=2)
    plot_clouds(g, data_all, c='r', alpha=0.5, markersize=3)
    plot_hist(g, data_all, bins=20, color='r', lw=2)
    [ax.axvline(1, ls = ':', lw = 1.5, c='k') for ax in g.subplots.ravel() if ax != None]
    g.export(os.path.join(ALL_RESULTS, 'baofit/triplot_alpha_comparison.pdf'))
