#!/usr/bin/env python
import numpy as np
import sys
import os
from cycler import cycler 
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()
WORKDIR = os.environ.get('WORKDIR')
SRC = os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import *
def plot_weight_fit_coeffs(filename, ax, label='', ngal=None, **kwargs):

    data = np.loadtxt(filename)
    if ngal is not None: r_scaling = ngal**(1./3)
    else: r_scaling=1
    for i in range(1,4):
        ax.plot(r_scaling * data[:,0], data[:,i], label = label+' $c_%i$'%(i-1), **kwargs)
        ax.set_ylabel('$c_i$', fontsize=15)


if __name__ == '__main__':
    fitfig, ax = plt.subplots(1,1, figsize=(7, 5), constrained_layout=True)
    fitfig.suptitle('Model: $w_v(R) = c_0(R) + c_1(R)w_g + c_2(R)w_g^2$', fontsize=15)
    ax.set_xlabel(r'$R$ [$h^{-1}$ Mpc]', fontsize=15)
    colorc = 'bgr'
    ax.set_prop_cycle(cycler(color=colorc))
    n_box1 = 3.976980e-4
    n_box5 = 1976125e-4
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax, label='real box1', ls = '-', ngal = n_box1)
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax, label='redshift box1', ls = '--', ngal=n_box1)
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax, label='real box5', ls = ':', lw=3, ngal=n_box5)
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax, label='redshift box5', ls = '-.', ngal=n_box5)
    ax.legend()
    odir = f"{WORKDIR}/patchy_results/box1/plots"
    oname = f"{odir}/r_vs_z_wtcoeffs.pdf"
    fitfig.savefig(oname, dpi=200)
    



