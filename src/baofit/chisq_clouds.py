#!/usr/bin/env python
import sys
WORKDIR = '/hpcstorage/dforero/projects/baosystematics'

sys.path.append("{}/src/baofit".format(WORKDIR))
from alpha_clouds import single_cloud_plot, process_filenames
import numpy as np
from scipy import stats
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from uncertainties import ufloat

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} SAMPLES_1 SAMPLES_2 [SAMPLES_3 ... SAMPLES_N] OUT_DIR")
    import itertools
    workdir=f"{WORKDIR}/patchy_results/box1"
    outdir = sys.argv[-1]
    os.makedirs(outdir, exist_ok=True)
    samples_fn = sys.argv[1:-1]
    samples =  [np.loadtxt(f, usecols=[0]) for f in samples_fn]
    # Keep elements up to length of shortest sequence
    min_length = min([len(s) for s in samples])
    samples = [s[:min_length] for s in samples]
    pairs = itertools.combinations(range(len(samples_fn)), 2)
    for ix, iy in pairs:
        x_label = process_filenames(samples_fn[ix], workdir=workdir)
        y_label = process_filenames(samples_fn[iy], workdir=workdir)
        
        # Do plots for chisq
        x_samples = samples[ix]
        y_samples = samples[iy]
        fig = plt.figure(figsize=(8,8))
        fig = single_cloud_plot(x_samples, y_samples, fig, x_label+r' $\chi^2$', y_label+r' $\chi^2$', quantity_label = r'\chi^2')
        oname = f"{outdir}/chisq_clouds_{x_label.replace(' ','-')}_vs_{y_label.replace(' ','-')}.pdf"
        fig.savefig(oname, dpi=200)
        plt.close(fig)
        print(f"Saved filename: {oname}")
