#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
def plot_bao(s, xi, **kwargs):
#	fit_range_mask = (s >= 60) & (s <= 150)
	fit_range_mask = (s >= 0) & (s <= 200)
	plt.plot(s[fit_range_mask], s[fit_range_mask]**2*xi[fit_range_mask], **kwargs)
def plot_bao_error(s, xi, xi_std, **kwargs):
	fit_range_mask = (s >= 60) & (s <= 150)
	s = s[fit_range_mask]
	xi = xi[fit_range_mask]
	xi_std = xi_std[fit_range_mask]
	plt.fill_between(s, s**2*(xi + xi_std), s**2*(xi - xi_std), **kwargs)
def plotfit(mean_files, bestfit_file, outdir, title):
	name=os.path.splitext(os.path.basename(mean_files[0]))[0]#+'_'+title.lower().replace(' ','')
	for mean_file in mean_files:
		print(mean_file)
		mean_data = np.loadtxt(mean_file)
		plot_bao(mean_data[:,0], mean_data[:,1], label = 'Mean',  lw = 2)
		plot_bao_error(mean_data[:,0], mean_data[:,1], mean_data[:,2], alpha = 0.2)
	bestfit_data = np.loadtxt(bestfit_file)
	plot_bao(bestfit_data[:,0], bestfit_data[:,-1], label = 'Best fit', c = 'b', lw = 3, ls = '--')
	plt.xlabel(r'$s$ [$h^{-1}$Mpc]')
	plt.ylabel(r'$s^2\xi_0$')
	plt.xlim(60, 150)
	plt.ylim(-25, 30)
	plt.legend(loc=0)
	plt.title(title)
	plt.gcf()
	plt.tight_layout()
	oname = os.path.join(outdir, 'bestfit_%s.pdf'%name)
	plt.savefig(oname, dpi=200)
	print(f"==> Saved {oname}")
if __name__=='__main__':

	if len(sys.argv)<5:
		sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t%s MEAN_FILE BESTFIT_FILE OUT_DIR TITLE'%sys.argv[0])
	mean_files = sys.argv[1:-3]
	bestfit_file = sys.argv[-3]
	outdir = sys.argv[-2]
	title = sys.argv[-1]

	plotfit(mean_files, bestfit_file, outdir, title)
