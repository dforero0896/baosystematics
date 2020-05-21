#!/usr/bin/env python
import numpy as np
from scipy import stats
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from uncertainties import ufloat
WORKDIR ='/hpcstorage/dforero/projects/baosystematics' 
cases = ['gal_w', 'gal_nw', 'void_nw']
labels = [r'\alpha_{\mathrm{gal, w}}', r'\alpha_{\mathrm{gal, now}}', r'\alpha_{\mathrm{void,now}}']
def find_outliers(data, threshold = 3):
    zscore = np.abs(stats.zscore(data))
    outliers = zscore > threshold
    return  outliers

def single_cloud_plot(x_samples, y_samples, x_label, y_label, guides = True, quantity_label=r'\alpha', **kwargs):
    x_complete = np.copy(x_samples)
    y_complete = np.copy(y_samples)
    widths = [6,2]
    heights = [2,6]
    x_outliers = find_outliers(x_samples) #mask
    y_outliers = find_outliers(y_samples) #mask
    xy_outliers = x_outliers | y_outliers #mask
    x_outliers = x_samples[xy_outliers] #outliers
    y_outliers = y_samples[xy_outliers] #outliers
    #x_samples = x_samples[~xy_outliers]
    #y_samples = y_samples[~xy_outliers]
    # Compute means and standard deviations the means are replaced by the medians
    x_mean, y_mean = np.median(x_samples), np.median(y_samples)
    x_std, y_std = np.std(x_samples), np.std(y_samples)
    x_value = ufloat(x_mean, x_std)
    y_value = ufloat(y_mean, y_std)
    g = (sns.jointplot(x = x_samples, y=y_samples, space=0.01, alpha=0.1,color='k')).plot_joint(sns.kdeplot, zorder=0, n_levels=6, cmap = 'inferno')
    xlims = g.ax_joint.get_xlim()
    ylims = g.ax_joint.get_ylim()
    g.set_axis_labels(x_label,y_label)
    g.ax_joint.plot([-10, 10], [-10, 10], ':k')
    g.ax_joint.set_xlim(xlims); g.ax_joint.set_ylim(ylims)
    if guides: 
        g.ax_joint.axvline(1, lw = 2, ls = ':', c = 'k')
        g.ax_joint.axhline(1, lw = 2, ls = ':', c = 'k')
    x_mean_line = g.ax_joint.axvline(x_mean, lw=2, ls=':', c='r', label=r'${}={:.6L}$'.format(quantity_label, x_value))
    y_mean_line = g.ax_joint.axhline(y_mean, lw=2, ls=':', c='b', label=r'${}={:.6L}$'.format(quantity_label, y_value))
    y_x_mean_diff = np.abs(y_value-x_value)
    y_x_mean_diff_handle = mpl.patches.Patch(linewidth=0,fill=False, edgecolor='none', visible=False, label=r'$\Delta{}={:.3eL}$'.format(quantity_label, y_x_mean_diff))
    g.ax_joint.legend(handles=[x_mean_line, y_mean_line, y_x_mean_diff_handle], loc='upper left', bbox_to_anchor=(-0.1, 1.4), fontsize=12, ncol=2)
    # Histogram along x
    if guides: g.ax_marg_x.axvline(1, lw = 2, ls = ':', c = 'k')
    g.ax_marg_x.axvline(x_mean, lw = 2, ls = ':', c = 'r')
    # Histogram along y
    if guides: g.ax_marg_y.axhline(1, lw = 2, ls = ':', c = 'k')
    g.ax_marg_y.axhline(y_mean, lw = 2, ls = ':', c = 'b')

    
    return g 
  
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
    abs_fn = abs_fn.replace(f"baofit/ind_", '')
    abs_fn = abs_fn[1:].replace('/', ' ')
    return abs_fn

if __name__=='__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} SAMPLES_1 SAMPLES_2 [SAMPLES_3 ... SAMPLES_N] OUT_DIR")

    import itertools
    import seaborn as sns
    sns.set(style="white", color_codes=True) 
    outdir = sys.argv[-1]
    os.makedirs(outdir, exist_ok=True)
    samples_fn = sys.argv[1:-1]
    samples =  []
    for f in samples_fn:
        dat = np.loadtxt(f, usecols=[0,1])
        if len(dat)==0:
            continue
        samples.append(dat)
    
    # Keep elements up to length of shortest sequence
    min_length = min([len(s) for s in samples])
    samples = [s[:min_length] for s in samples]
    pairs = itertools.combinations(range(len(samples)), 2)
    workdir=os.path.dirname(os.path.abspath(outdir))
    for ix, iy in pairs:
        x_label = process_filenames(samples_fn[ix], workdir=workdir)
        y_label = process_filenames(samples_fn[iy], workdir=workdir)
        
        # Do plots for alpha
        x_samples = samples[ix][:,0]
        y_samples = samples[iy][:,0]
        g = single_cloud_plot(x_samples, y_samples, x_label+r' $\alpha$', y_label+r' $\alpha$', guides=True, quantity_label=r'\alpha')
        oname = f"{outdir}/alpha_clouds_{x_label.replace(' ','-')}_vs_{y_label.replace(' ','-')}.pdf"
        g.savefig(oname, dpi=200)
        print(f"Saved filename: {oname}")
        # Do plots for sigma_alpha
        x_samples = samples[ix][:,1]
        y_samples = samples[iy][:,1]
        g = single_cloud_plot(x_samples, y_samples, x_label+r' $\sigma_{\alpha}$', y_label+r' $\sigma_{\alpha}$', guides=False, quantity_label=r'\sigma')
        oname = f"{outdir}/sigma_alpha_clouds_{x_label.replace(' ','-')}_vs_{y_label.replace(' ','-')}.pdf"
        g.savefig(oname, dpi=200)
        print(f"Saved filename: {oname}")
        sys.exit(0)
