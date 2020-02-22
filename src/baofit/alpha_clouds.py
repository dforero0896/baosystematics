#!/usr/bin/env python
import numpy as np
from scipy import stats
import sys
import os
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
WORKDIR ='/hpcstorage/dforero/projects/baosystematics' 
ALL_RESULTS = os.path.join(WORKDIR, 'results/allsyst_v7')
NO_RESULTS = os.path.join(WORKDIR, 'results/nosyst_v7')
systresults = {'allsyst': ALL_RESULTS, 'nosyst':NO_RESULTS}
def single_cloud_plot(x_samples, y_samples, fig, x_label, y_label, systcase_x, systcase_y, **kwargs):
    widths = [6,2]
    heights = [2,6]
    gs = fig.add_gridspec(2, 2, width_ratios = widths, height_ratios = heights, wspace=0, hspace=0)
    main = fig.add_subplot(gs[1,0])
    x_hist = fig.add_subplot(gs[0,0], sharex = main)
    y_hist = fig.add_subplot(gs[1,1], sharey = main)
    x_hist.hist(x_samples, density = True, histtype='step', color = 'r', lw=3, **kwargs)
    plt.setp(x_hist.get_xticklabels(), visible=False)
    y_hist.hist(y_samples, density = True, histtype='step', color = 'b', orientation='horizontal', lw=3, **kwargs)
    plt.setp(y_hist.get_yticklabels(), visible=False)
    main.plot(x_samples, y_samples, color = 'k', lw = 0, marker = 'o', alpha = 0.2)
    main.axvline(1, lw = 2, ls = ':', c = 'k')
    x_hist.axvline(1, lw = 2, ls = ':', c = 'k')
    main.axhline(1, lw = 2, ls = ':', c = 'k')
    y_hist.axhline(1, lw = 2, ls = ':', c = 'k')
    main.set_xlabel('%s $%s$'%(systcase_x.capitalize(), x_label), fontsize=12)
    main.set_ylabel('%s $%s$'%(systcase_y.capitalize(), y_label), fontsize=12)
    return fig
def samples_alpha(cap, systkey='nosyst'):
    cases = ['gal_w', 'gal_nw', 'void']
    labels = [r'\alpha_{\mathrm{gal, w}}', r'\alpha_{\mathrm{gal, now}}', r'\alpha_{\mathrm{void}}']
    cases_files = [os.path.join(systresults[systkey], s) for s in ['baofit/individual_combined_gal/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_gal_nowt/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_void/alpha_samples_%s.dat'%cap]]
    cases_data_list = [np.loadtxt(f, usecols=0) for f in cases_files]
    lengths = [d.shape[0] for d in cases_data_list]
    min_len = min(lengths)
    cases_data = np.stack([d[:999] for d in cases_data_list], axis = 1)
    return cases_data, cases, labels

if __name__=='__main__':
    data_no, cases_no, labels_no = samples_alpha('cbz', 'nosyst')
    data_all, cases_all, labels_all = samples_alpha('cbz', 'allsyst')
    data_list = [data_all, data_no]
    systcases = list(systresults.keys())
    data_ind_x = [1]
    data_ind_y = [0]
    for ix, data_x in enumerate(data_list):
        for iy, data_y in enumerate(data_list):
            if ix >= iy:
                for case_x_id in range(len(cases_no)):
                    for case_y_id in range(len(cases_no)):
                        if case_x_id <= case_y_id:
                            fig = plt.figure(figsize=(8,8))
                            fig = single_cloud_plot(data_x[:,case_x_id], data_y[:,case_y_id], fig, x_label = labels_no[case_x_id], y_label = labels_no[case_y_id], systcase_x = systcases[ix], systcase_y = systcases[iy])
                            outname = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/plots/alpha_clouds_%s-%s_vs_%s-%s.pdf'%(systcases[ix], cases_no[case_x_id], systcases[iy], cases_no[case_y_id]))
                            fig.savefig(outname)
                            print(outname)
    fig.savefig(outname)
    #os.system('evince %s'%outname)
