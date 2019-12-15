#!/usr/bin/env python
import numpy as np
import os
import sys
try:
	raise ImportError
	import matplotlib.pyplot as plt
except:
	import matplotlib
	matplotlib.use("Agg")	
	import matplotlib.pyplot as plt
WORKDIR ='/global/homes/d/dforero/scratch/baosystematics' 
OUT_DIR = os.path.join(WORKDIR, 'results/allsyst_v7/baofit')
VOID_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_combined_void/')
VOID_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_combined_void/')
void_all_cbz = os.path.join(VOID_ALL, 'alpha_hist_cbz.dat')
void_no_cbz = os.path.join(VOID_NO, 'alpha_hist_cbz.dat')

GAL_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_combined_gal/')
GAL_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_combined_gal/')
gal_all_cbz = os.path.join(GAL_ALL, 'alpha_hist_cbz.dat')
gal_no_cbz = os.path.join(GAL_NO, 'alpha_hist_cbz.dat')
def plot_cols(f, **kwargs):
	plt.plot(f[:,0], f[:,1], **kwargs)
if os.path.isfile(void_all_cbz) and os.path.isfile(void_no_cbz):
	void_hist_all_cbz = np.loadtxt(void_all_cbz)
	void_hist_no_cbz = np.loadtxt(void_no_cbz)
	plot_cols(void_hist_all_cbz, label = 'VOID NGC ALLSYST', ls = '--', lw = 2, c = 'r')
	plot_cols(void_hist_no_cbz, label = 'VOID NGC NOSYST', ls = '--', lw = 2, c = 'b')

if os.path.isfile(gal_all_cbz) and os.path.isfile(gal_no_cbz):
	gal_hist_all_cbz = np.loadtxt(gal_all_cbz)
	gal_hist_no_cbz = np.loadtxt(gal_no_cbz)
	plot_cols(gal_hist_all_cbz, label = 'GAL NGC ALLSYST', ls = '--', lw = 2, c = 'k')
	plot_cols(gal_hist_no_cbz, label = 'GAL NGC NOSYST', ls = '--', lw = 2, c = 'g')
plt.legend()
plt.xlabel('$\\alpha$')
plt.ylabel('$P(\\alpha)$')
plt.gcf()
plt.savefig(os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'), dpi=200)
print('Plot saved in %s '%os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'))
