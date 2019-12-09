#!/usr/bin/env python
import numpy as np
import os
import sys
try:
	import matplotlib.pyplot as plt
except:
	import matplotlib
	matplotlib.use("Agg")	
	import matplotlib.pyplot as plt
WORKDIR ='/global/homes/d/dforero/scratch/baosystematics' 
OUT_DIR = os.path.join(WORKDIR, 'results/allsyst_v7/baofit')
VOID_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_void/')
VOID_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_void/')
void_all_ngc = os.path.join(VOID_ALL, 'alpha_hist_ngc.dat')
void_all_sgc = os.path.join(VOID_ALL, 'alpha_hist_sgc.dat')
void_no_ngc = os.path.join(VOID_NO, 'alpha_hist_ngc.dat')
void_no_sgc = os.path.join(VOID_NO, 'alpha_hist_sgc.dat')
hist_all_ngc = np.loadtxt(void_all_ngc)
hist_all_sgc = np.loadtxt(void_all_sgc)
hist_no_ngc = np.loadtxt(void_no_ngc)
hist_no_sgc = np.loadtxt(void_no_sgc)

def plot_cols(f, **kwargs):
	plt.plot(f[:,0], f[:,1], **kwargs)

plot_cols(hist_all_ngc, label = 'NGC ALLSYST', ls = '--', lw = 3, c = 'r')
plot_cols(hist_all_sgc, label = 'SGC ALLSYST', ls = '-', lw = 3, c = 'r')
plot_cols(hist_no_ngc, label = 'NGC NOSYST', ls = '--', lw = 3, c = 'b')
plot_cols(hist_no_sgc, label = 'SGC NOSYST', ls = '-', lw = 3, c = 'b')
plt.legend()
plt.xlabel('$\\alpha$')
plt.ylabel('$P(\\alpha)$')
plt.gcf()
plt.savefig(os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'), dpi=200)
