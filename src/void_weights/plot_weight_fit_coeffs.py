#!/usr/bin/env python
import numpy as np
import sys
import os
from cycler import cycler 
import matplotlib.pyplot as plt

def plot_weight_fit_coeffs(filename, ax, label='', **kwargs):

    data = np.loadtxt(filename)
    
    for i in range(1,4):
        ax.plot(data[:,0], data[:,i], label = label+' $c_%i$'%(i-1), **kwargs)
        ax.set_ylabel('$c_i$', fontsize=15)


if __name__ == '__main__':
    fitfig, ax = plt.subplots(1,1, figsize=(7, 5), constrained_layout=True)
    fitfig.suptitle('Model: $w_v(R) = c_0(R) + c_1(R)w_g + c_2(R)w_g^2$', fontsize=15)
    ax.set_xlabel(r'$R$ [$h^{-1}$ Mpc]', fontsize=15)
    colorc = 'bgr'
    ax.set_prop_cycle(cycler(color=colorc))
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax, label='real box1', ls = '-')
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax, label='redshift box1', ls = '--')
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax, label='real box5', ls = ':', lw=3)
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax, label='redshift box5', ls = '-.')
    ax.legend()
    fitfig.savefig('r_vs_z_wtcoeffs.pdf', dpi=200)
    



