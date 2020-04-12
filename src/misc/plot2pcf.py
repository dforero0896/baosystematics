#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys
import os
import re
import numpy as np
import matplotlib as mpl
from cycler import cycler
import matplotlib.gridspec as gridspec 
mpl.use("Agg")
#mpl.rcParams['text.usetex'] = True
#mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

if len(sys.argv) > 3:
	mocks_in = sys.argv[1:-1]
	out = sys.argv[-1]
else:
	sys.stderr.write('Usage: %s MOCK_IN OUT_NAME\n'%sys.argv[0])
	sys.exit(1)
os.makedirs(os.path.dirname(out), exist_ok=True)
fig = plt.figure(figsize = (10, 4))
spec = gridspec.GridSpec(ncols=3, nrows=2, figure=fig, height_ratios=[4, 1], hspace=0.05, wspace=0.2)
ax = np.empty((2, 3), dtype=type(plt.axes))
for i in range(ax.shape[0]):
	for k in range(ax.shape[1]):
		ax[i,k] = fig.add_subplot(spec[i,k])
plt.rcParams.update({'font.size': 10})
plt.rcParams.update({'axes.labelsize': 'xx-large'})
colorlist = list(mcolors.TABLEAU_COLORS.keys())
colorc = list(np.repeat(colorlist, 1))
[a.set_prop_cycle(cycler(color=colorc)) for a in ax.ravel()]
pole_ref = []
pole_std_ref=[]
pole_upper_ref = []
pole_lower_ref = []
for k, mock_in in enumerate(mocks_in):
	p, name = os.path.split(mock_in)
	name = os.path.splitext(name)[0]
	title = name.replace('TwoPCF_mockavg_', '').replace('_', ' ').capitalize()
	mocks = np.loadtxt(mock_in, skiprows=7)
	print(mock_in)
	xdata = mocks[:,0]
	for i in range(ax.shape[1]):
		if k==0:
			pole_ref.append(mocks[:,2*i+1])
			pole_std_ref.append(mocks[:,2*(i+1)])
			pole_upper_ref.append(pole_ref[i] + pole_std_ref[i])
			pole_lower_ref.append(pole_ref[i] - pole_std_ref[i])
		pole = mocks[:,2*i+1]
		pole_std = mocks[:,2*(i+1)]
		pole_upper = pole + pole_std
		pole_lower = pole - pole_std
		diff = xdata**2*pole - xdata**2*pole_ref[i]
		diff_upper = xdata**2*pole_upper - xdata**2*pole_upper_ref[i]
		diff_lower = xdata**2*pole_lower - xdata**2*pole_lower_ref[i]
		a = ax[0,i]
		a.fill_between(xdata, xdata**2*(pole_lower),xdata**2*(pole_upper), alpha=0.5)
		a.plot(xdata, xdata**2*pole, label =title)
		b = ax[1,i]
		b.fill_between(xdata, diff_lower, diff_upper, alpha=0.5)
		b.plot(xdata, diff)
		
ax[0,0].set_ylabel('$s^2\\xi_l$')
ax[1, 0].set_ylabel(r'$s^2[\xi_l(s)-\xi_l^{\mathrm{nosyst}}(s)]$')
[a.set_xlabel('$s\ [h^{-1}\mathrm{Mpc}]$') for a in ax[1,:]]
[a.axes.xaxis.set_ticklabels([]) for a in ax[0,:]]
ax[0,0].legend(bbox_to_anchor=(-0.2, 1.2),loc='upper left', fontsize=5)#, bbox_transform=fig.transFigure)  
fig.tight_layout()
fig.savefig(out, dpi = 200)
print(f"==> Saved figure in {os.path.abspath(out)}")
