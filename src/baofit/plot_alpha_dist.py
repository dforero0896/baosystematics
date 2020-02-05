#!/usr/bin/env python
import numpy as np
import os
import sys
import matplotlib
matplotlib.use("Agg")	
import matplotlib.pyplot as plt
WORKDIR ='/hpcstorage/dforero/projects/baosystematics' 
OUT_DIR = os.path.join(WORKDIR, 'results/allsyst_v7/baofit')
VOID_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_combined_void/')
VOID_ALL_AVG = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/avg_combined_void/')
VOID_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_combined_void/')
VOID_NO_AVG = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/avg_combined_void/')
void_all_cbz = os.path.join(VOID_ALL, 'alpha_hist_cbz.dat')
void_no_cbz = os.path.join(VOID_NO, 'alpha_hist_cbz.dat')
void_all_cbz_samples = os.path.join(VOID_ALL, 'alpha_samples_cbz.dat')
void_no_cbz_samples = os.path.join(VOID_NO, 'alpha_samples_cbz.dat')
void_all_cbz_avg = [os.path.join(VOID_ALL_AVG, f) for f in os.listdir(VOID_ALL_AVG) if 'mystats' in f][0]
void_no_cbz_avg = [os.path.join(VOID_NO_AVG, f) for f in os.listdir(VOID_NO_AVG) if 'mystats' in f][0]
GAL_ALL = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/individual_combined_gal/')
GAL_ALL_AVG = os.path.join(WORKDIR, 'results/allsyst_v7/baofit/avg_combined_gal/')
GAL_NO = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/individual_combined_gal/')
GAL_NO_AVG = os.path.join(WORKDIR, 'results/nosyst_v7/baofit/avg_combined_gal/')
gal_all_cbz = os.path.join(GAL_ALL, 'alpha_hist_cbz.dat')
gal_no_cbz = os.path.join(GAL_NO, 'alpha_hist_cbz.dat')
gal_all_cbz_samples = os.path.join(GAL_ALL, 'alpha_samples_cbz.dat')
gal_no_cbz_samples = os.path.join(GAL_NO, 'alpha_samples_cbz.dat')
gal_all_cbz_avg = [os.path.join(GAL_ALL_AVG, f) for f in os.listdir(GAL_ALL_AVG) if 'mystats' in f][0]
gal_no_cbz_avg = [os.path.join(GAL_NO_AVG, f) for f in os.listdir(GAL_NO_AVG) if 'mystats' in f][0]
def plot_cols(f, ax = plt.gca(), **kwargs):
	ax.plot(f[:,0], f[:,2], **kwargs)
	color = kwargs.pop('c')
	ax.fill_between(f[:,0], f[:,2], color=color, alpha=0.2)
def plot_horiz(alpha_sigma_z, n, ax = plt.gca(), xpos = 0.5, **kwargs):
	alpha, sigma, z = alpha_sigma_z
	sigma/=np.sqrt(n)
	ax.axhline(alpha, **kwargs)
	y = np.ones(2)
#	color = kwargs.pop('c')
#	ax.fill_between([0,1], (alpha-sigma)*y, (alpha+sigma)*y, alpha=0.2, color = color)
	try:
		label = kwargs.pop('label')
	except KeyError:
	#	print('No label found')
		pass
	ax.errorbar([xpos], [alpha], yerr = sigma, capsize = 2, **kwargs)
	
def get_n_mocks(filename):
	with open(filename) as f:
		n = [int(i) for i in f.readline().split() if i.isdigit()][0]
		f.readline()
		mean = float(f.readline().split(' ')[-1])
		std = float(f.readline().split(' ')[-1])
		orig_std = float(f.readline().split(' ')[-1])
	return n, mean, std, orig_std 
def get_difference_samples(allsyst, nosyst):
	fall = np.loadtxt(allsyst)
	fnone = np.loadtxt(nosyst)
	max_elem = min([len(fall), len(fnone)])
	fall = fall[:max_elem]
	fnone = fnone[:max_elem]
	diff = fall-fnone
	return diff
fig, ax = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3,1]}, figsize = (6,7))
fig1, ax1 = plt.subplots(1, 1, figsize = (6,2.5))
if os.path.isfile(void_all_cbz) and os.path.isfile(void_no_cbz):
	n_all, a_all, std_all, ostd_all = get_n_mocks(void_all_cbz)
	n_no, a_no, std_no, ostd_no = get_n_mocks(void_no_cbz)
	void_hist_all_cbz = np.loadtxt(void_all_cbz)
	void_hist_no_cbz = np.loadtxt(void_no_cbz)
	void_alpha_sigma_z_all = np.loadtxt(void_all_cbz_avg)
	void_alpha_sigma_z_no = np.loadtxt(void_no_cbz_avg)
	plot_cols(void_hist_all_cbz, ax = ax[0], label = 'VOID All syst.', ls = '-.', lw = 2, c = 'r')
	plot_cols(void_hist_no_cbz, ax = ax[0], label = 'VOID No syst.', ls = '--', lw = 2, c = 'b')
	plot_horiz((a_all, std_all, 0), n_all, ax = ax[1], ls = '-.', c = 'r', xpos=0.2)
	plot_horiz((a_no, std_no, 0), n_no, ax = ax[1], ls = '--', c = 'b', xpos=0.4)
	plot_horiz(void_alpha_sigma_z_all, n_all, ax = ax1, ls = '-.', c = 'r', xpos=0.2, label = 'VOID All syst.')
	plot_horiz(void_alpha_sigma_z_no, n_no, ax = ax1, ls = '--', c = 'b', xpos=0.4, label = 'VOID No syst.')
	diff = get_difference_samples(void_all_cbz_samples, void_no_cbz_samples)
	
	
if os.path.isfile(gal_all_cbz) and os.path.isfile(gal_no_cbz):
	n_all, a_all, std_all, ostd_all = get_n_mocks(gal_all_cbz)
	n_no, a_no, std_no, ostd_no = get_n_mocks(gal_no_cbz)
	gal_hist_all_cbz = np.loadtxt(gal_all_cbz)
	gal_hist_no_cbz = np.loadtxt(gal_no_cbz)
	gal_alpha_sigma_z_all = np.loadtxt(gal_all_cbz_avg)
	gal_alpha_sigma_z_no = np.loadtxt(gal_no_cbz_avg)
	plot_cols(gal_hist_all_cbz, ax = ax[0], label = 'GAL All syst.', ls = '-', lw = 2, c = 'k')
	plot_cols(gal_hist_no_cbz, ax = ax[0], label = 'GAL No syst.', ls = ':', lw = 2, c = 'g')
	plot_horiz((a_all, std_all, 0), n_all, ax = ax[1], ls = '-', c = 'k', xpos=0.8)
	plot_horiz((a_no, std_no, 0), n_no, ax = ax[1], ls = ':', c = 'g', xpos=0.6)
	plot_horiz(gal_alpha_sigma_z_no, n_no, ax = ax1, ls = ':', c = 'g', xpos=0.6, label = 'GAL No syst.')
	plot_horiz(gal_alpha_sigma_z_all, n_all, ax = ax1, ls = '-', c = 'k', xpos=0.8, label = 'GAL All syst.')
fig.legend()
fig1.legend(loc=4)
ax[0].set_xlabel('$\\alpha$')
ax[0].set_ylabel('$P(\\alpha)$')
ax[1].set_ylabel(r'$\alpha$')
ax[1].set_xticklabels([])
ax[1].set_xlim(0,1)
ax1.set_ylabel(r'$\alpha$')
ax1.set_xticklabels([])
ax1.set_xlim(0,1)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'), dpi=200)
fig1.tight_layout()
fig1.savefig(os.path.join(OUT_DIR, 'alpha_mean_comparison_ALLvsNO.png'), dpi=200)
print('Plot saved in %s '%os.path.join(OUT_DIR, 'alpha_comparison_ALLvsNO.png'))
