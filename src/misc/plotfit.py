#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
if len(sys.argv)!=4:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t%s MEAN_FILE BESTFIT_FILE OUT_DIR'%sys.argv[0])
mean_file = sys.argv[1]
bestfit_file = sys.argv[2]
outdir = sys.argv[3]
name=os.path.splitext(os.path.basename(mean_file))[0]
def plot_bao(s, xi, **kwargs):
	plt.plot(s, s**2*xi, **kwargs)
def plot_bao_error(s, xi, xi_std, **kwargs):
	plt.fill_between(s, s**2*(xi + xi_std), s**2*(xi - xi_std), **kwargs)
mean_data = np.loadtxt(mean_file)
bestfit_data = np.loadtxt(bestfit_file)
plot_bao(mean_data[:,0], mean_data[:,1], label = 'Mean', c= 'r')
plot_bao(bestfit_data[:,0], bestfit_data[:,2], label = 'Best fit', c = 'b')
plot_bao_error(mean_data[:,0], mean_data[:,1], mean_data[:,2], alpha = 0.2, color= 'r')
plt.xlabel('$s$ [$h^{-1}$Mpc]')
plt.ylabel('$s^2\\xi_0$')
plt.legend(loc=0)
plt.gcf()
plt.tight_layout()
plt.savefig(os.path.join(outdir, 'bestfit_%s.png'%name), dpi=200)
