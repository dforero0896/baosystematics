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
void_hist_all_ngc = np.loadtxt(void_all_ngc)
void_hist_all_sgc = np.loadtxt(void_all_sgc)
void_hist_no_ngc = np.loadtxt(void_no_ngc)
void_hist_no_sgc = np.loadtxt(void_no_sgc)

GAL_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_gal/')
GAL_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_gal/')
gal_all_ngc = os.path.join(GAL_ALL, 'alpha_hist_ngc.dat')
gal_all_sgc = os.path.join(GAL_ALL, 'alpha_hist_sgc.dat')
gal_no_ngc = os.path.join(GAL_NO, 'alpha_hist_ngc.dat')
gal_no_sgc = os.path.join(GAL_NO, 'alpha_hist_sgc.dat')
gal_hist_all_ngc = np.loadtxt(gal_all_ngc)
gal_hist_all_sgc = np.loadtxt(gal_all_sgc)
gal_hist_no_ngc = np.loadtxt(gal_no_ngc)
gal_hist_no_sgc = np.loadtxt(void_no_sgc)
def plot_cols(f, **kwargs):
	plt.plot(f[:,0], f[:,1], **kwargs)

plot_cols(void_hist_all_ngc, label = 'VOID NGC ALLSYST', ls = '--', lw = 2, c = 'r')
plot_cols(void_hist_all_sgc, label = 'VOID SGC ALLSYST', ls = '-', lw = 2, c = 'r')
plot_cols(void_hist_no_ngc, label = 'VOID NGC NOSYST', ls = '--', lw = 2, c = 'b')
plot_cols(void_hist_no_sgc, label = 'VOID SGC NOSYST', ls = '-', lw = 2, c = 'b')

plot_cols(gal_hist_all_ngc, label = 'GAL NGC ALLSYST', ls = '--', lw = 2, c = 'k')
plot_cols(gal_hist_all_sgc, label = 'GAL SGC ALLSYST', ls = '-', lw = 2, c = 'k')
plot_cols(gal_hist_no_ngc, label = 'GAL NGC NOSYST', ls = '--', lw = 2, c = 'g')
plot_cols(gal_hist_no_sgc, label = 'GAL SGC NOSYST', ls = '-', lw = 2, c = 'g')
plt.legend()
plt.xlabel('$\\alpha$')
plt.ylabel('$P(\\alpha)$')
plt.gcf()
plt.savefig(os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'), dpi=200)
print('Plot saved in %s '%os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'))
