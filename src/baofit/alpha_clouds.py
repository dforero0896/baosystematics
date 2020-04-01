#!/usr/bin/env python
import numpy as np
from scipy import stats
import sys
import os
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from uncertainties import ufloat
WORKDIR ='/hpcstorage/dforero/projects/baosystematics' 
cases = ['gal_w', 'gal_nw', 'void_nw']
labels = [r'\alpha_{\mathrm{gal, w}}', r'\alpha_{\mathrm{gal, now}}', r'\alpha_{\mathrm{void,now}}']
def single_cloud_plot(x_samples, y_samples, fig, x_label, y_label, guides = True, quantity_label=r'\alpha', **kwargs):
    widths = [6,2]
    heights = [2,6]
    # Compute means and standard deviations
    x_mean, y_mean = np.mean(x_samples), np.mean(y_samples)
    x_std, y_std = np.std(x_samples), np.std(y_samples)
    x_value = ufloat(x_mean, x_std)
    y_value = ufloat(y_mean, y_std)
    # Create gridspec
    gs = fig.add_gridspec(2, 2, width_ratios = widths, height_ratios = heights, wspace=0, hspace=0)
    # Main panel
    main = fig.add_subplot(gs[1,0]) 
    main.plot(x_samples, y_samples, color = 'k', lw = 0, marker = 'o', alpha = 0.2)
    if guides: 
        main.axvline(1, lw = 2, ls = ':', c = 'k')
        main.axhline(1, lw = 2, ls = ':', c = 'k')
    main.plot(main.get_xlim(), main.get_ylim(), lw=2, ls=':', c='k')
    x_mean_line = main.axvline(x_mean, lw=2, ls=':', c='r', label=r'${}={:.6L}$'.format(quantity_label, x_value))
    y_mean_line = main.axhline(y_mean, lw=2, ls=':', c='b', label=r'${}={:.6L}$'.format(quantity_label, y_value))
    main.set_xlabel(r'%s'%(x_label), fontsize=15)
    main.set_ylabel(r'%s'%(y_label), fontsize=15)
    y_x_mean_diff = np.abs(y_value-x_value)
    y_x_mean_diff_handle = mpl.patches.Patch(linewidth=0,fill=False, edgecolor='none', visible=False, label=r'$\Delta{}={:.3eL}$'.format(quantity_label, y_x_mean_diff))
    main.legend(handles=[x_mean_line, y_mean_line, y_x_mean_diff_handle], loc='upper left', bbox_to_anchor=(0.0, 1.5), fontsize=12, ncol=2)
    # Histogram along x
    x_hist = fig.add_subplot(gs[0,0], sharex = main)
    x_hist.hist(x_samples, density = True, histtype='step', color = 'r', lw=3, **kwargs)
    if guides: x_hist.axvline(1, lw = 2, ls = ':', c = 'k')
    x_hist.axvline(x_mean, lw = 2, ls = ':', c = 'r')
    plt.setp(x_hist.get_xticklabels(), visible=False)
    plt.setp(x_hist.get_yticklabels(), visible=False)
    # Histogram along y
    y_hist = fig.add_subplot(gs[1,1], sharey = main)
    y_hist.hist(y_samples, density = True, histtype='step', color = 'b', orientation='horizontal', lw=3, **kwargs)
    if guides: y_hist.axhline(1, lw = 2, ls = ':', c = 'k')
    y_hist.axhline(y_mean, lw = 2, ls = ':', c = 'b')
    plt.setp(y_hist.get_yticklabels(), visible=False)
    plt.setp(y_hist.get_xticklabels(), visible=False)

    
    return fig
  
def samples_alpha(cap, systresults, systkey='nosyst'):
    cases_files = [os.path.join(systresults[systkey], s) for s in ['baofit/individual_combined_gal/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_gal_nowt/alpha_samples_%s.dat'%cap, 'baofit/individual_combined_void/alpha_samples_%s.dat'%cap]]
    cases_data_list = [np.loadtxt(f, usecols=0) for f in cases_files]
    lengths = [d.shape[0] for d in cases_data_list]
    min_len = min(lengths)
    cases_data = np.stack([d[:999] for d in cases_data_list], axis = 1)
    return cases_data, cases, labels
def plot_all_elg():
    ALL_RESULTS = os.path.join(WORKDIR, 'results/allsyst_v7')
    NO_RESULTS = os.path.join(WORKDIR, 'results/nosyst_v7')
    systresults = {'allsyst': ALL_RESULTS, 'nosyst':NO_RESULTS}
    data_no, cases_no, labels_no = samples_alpha('cbz', systresults, 'nosyst')
    data_all, cases_all, labels_all = samples_alpha('cbz', systresults, 'allsyst')
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
                            fig = single_cloud_plot(data_x[:,case_x_id], data_y[:,case_y_id], fig, x_label = f"{systcases[ix].capitalize()} ${labels_no[case_x_id]}$", y_label = f"{systcases[iy].capitalize()} ${labels_no[case_y_id]}$")
                            outname = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/plots/alpha_clouds_%s-%s_vs_%s-%s.pdf'%(systcases[ix], cases_no[case_x_id], systcases[iy], cases_no[case_y_id]))
                            fig.savefig(outname)
                            print(outname)
    fig.savefig(outname)
    #os.system('evince %s'%outname)

def process_filenames(fn, funcname='parabola', workdir=f"{WORKDIR}/patchy_results/box1"):
    abs_fn = os.path.realpath(os.path.dirname(fn))
    abs_fn = abs_fn.replace(workdir, '')
    abs_fn = abs_fn.replace(f"/{funcname}", f"_{funcname}")
    abs_fn = abs_fn.replace(f"baofit/individual_", '')
    abs_fn = abs_fn[1:].replace('/', ' ')
    return abs_fn

if __name__=='__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} SAMPLES_1 SAMPLES_2 [SAMPLES_3 ... SAMPLES_N] OUT_DIR")
    import itertools
#    workdir=f"{WORKDIR}/results"
    workdir=f"{WORKDIR}/patchy_results/box1"
    outdir = sys.argv[-1]
    os.makedirs(outdir, exist_ok=True)
    samples_fn = sys.argv[1:-1]
    samples =  [np.loadtxt(f, usecols=[0,1]) for f in samples_fn]
    # Keep elements up to length of shortest sequence
    min_length = min([len(s) for s in samples])
    samples = [s[:min_length] for s in samples]
    pairs = itertools.combinations(range(len(samples_fn)), 2)
    for ix, iy in pairs:
        x_label = process_filenames(samples_fn[ix], workdir=workdir)
        y_label = process_filenames(samples_fn[iy], workdir=workdir)
        
        # Do plots for alpha
        x_samples = samples[ix][:,0]
        y_samples = samples[iy][:,0]
        fig = plt.figure(figsize=(8,8))
        fig = single_cloud_plot(x_samples, y_samples, fig, x_label+r' $\alpha$', y_label+r' $\alpha$')
        oname = f"{outdir}/alpha_clouds_{x_label.replace(' ','-')}_vs_{y_label.replace(' ','-')}.pdf"
        fig.savefig(oname, dpi=200)
        plt.close(fig)
        print(f"Saved filename: {oname}")

        # Do plots for sigma_alpha
        x_samples = samples[ix][:,1]
        y_samples = samples[iy][:,1]
        fig = plt.figure(figsize=(8,8))
        fig = single_cloud_plot(x_samples, y_samples, fig, x_label+r' $\sigma_{\alpha}$', y_label+r' $\sigma_{\alpha}$', guides=False, quantity_label=r'\sigma')
        oname = f"{outdir}/sigma_alpha_clouds_{x_label.replace(' ','-')}_vs_{y_label.replace(' ','-')}.pdf"
        fig.savefig(oname, dpi=200)
        plt.close(fig)
        
        print(f"Saved filename: {oname}")
