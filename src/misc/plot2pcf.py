#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys
import os
import re
import numpy as np
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

if len(sys.argv) != 4:
	sys.stdout.write('Usage: %s OBS_IN MOCK_IN OUT_PATH\n'%sys.argv[0])
	sys.exit(1)
obs_in = sys.argv[1]
mock_in = sys.argv[2]
out = sys.argv[3]
p, name = os.path.split(mock_in)
title = name.replace('TwoPCF_mockavg_', '').replace('_', ' ').upper()
mocks = np.loadtxt(mock_in)
obs = np.loadtxt(obs_in)
xdata = mocks[:,0]
fig, ax = plt.subplots(2,1,figsize = (7, 11), sharex = True)
plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'axes.labelsize': 'large'})
for i,a in enumerate(ax):
	a.set_ylabel('$s^2\\xi_%i$'%(2*i))
	a.fill_between(xdata, xdata**2*(mocks[:,2*i+1] - mocks[:,2*(i+1)]),xdata**2*(mocks[:,2*i+1] + mocks[:,2*(i+1)]), alpha=0.5, color='r', label = '$1\sigma$')
	a.plot(xdata, xdata**2*mocks[:,2*i+1], label = '$\\bar{\\xi}', c='r')
	a.plot(obs[:,0], obs[:,0]**2*obs[:,i+1], c = 'k', marker='o')
ax[1].set_xlabel('$s\ [h^{-1}\mathrm{Mpc}]$')
ax[0].set_title(title)
plt.tight_layout()
plt.gcf()
#plt.show()
fig.savefig(os.path.join(out,name.replace('ascii', 'png')), dpi = 200)
