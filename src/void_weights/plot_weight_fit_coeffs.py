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
sys.path.append(f"../misc")
from params import *
from style_plots import set_size
from compute_fit_coeffs  import load_binaries
import matplotlib as mpl

def plot_weight_fit_coeffs(filename, ax, label='', ngal=None, **kwargs):

    data = np.loadtxt(filename)
    if ngal is not None: r_scaling = ngal**(1./4)
    else: r_scaling=1
    print(f"{filename}: {r_scaling}")
    for i in range(1,4):
        ax.plot(r_scaling * data[:,0], data[:,i], label = label+' $c_%i$'%(i-1), **kwargs)
        ax.set_ylabel('$c_i$', fontsize=12)


if __name__ == '__main__':
    fitfig, ax = plt.subplots(2,1, figsize=set_size('mnras_full', subplots=(2,1)), 
				constrained_layout=True, sharex=True)
    fitfig.suptitle('Model: $w_v(R) = c_0(R) + c_1(R)w_g + c_2(R)w_g^2$', fontsize=11)
    ax[1].set_xlabel(r'$\bar{n}_{\mathrm{gal}}^{1/4}~R$ [$h^{-1/4}$ Mpc$^{1/4}$]', fontsize=11)
    colorc = 'bgr'
    cmap = mpl.cm.get_cmap('inferno')
    colorc = [cmap(i) for i in [0.25, 0.5, 0.75]]
    [a.set_prop_cycle(cycler(color=colorc)) for a in ax]
    ax[0].text(0.05, 0.1, 'Real space', fontsize=11, transform=ax[0].transAxes)
    ax[1].text(0.05, 0.1, 'Redshift space', fontsize=11,transform=ax[1].transAxes)
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax[0], 
				#label='box1', 
				ls = '-', ngal = NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax[1], 
				#label='box1', 
				ls = '--', ngal=NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax[0], 
				#label='box5', 
				ls = '-', lw=1, ngal=NGAL['5'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax[1], 
				#label='box5', 
				ls = '--', ngal=NGAL['5'])
    [a.legend() for a in ax]
    [a.set_yscale('symlog') for a in ax]
    odir = f"{WORKDIR}/patchy_results/box1/plots"
    oname = f"{odir}/r_vs_z_wtcoeffs.pdf"
    fitfig.savefig(oname, dpi=200, bbox_inches='tight')
    print(f"==> Saved figure in {oname}")
    [a.clear() for a in ax] 


    ax[0].text(0.05, 0.1, r'Box 1: $\bar{n}_{\mathrm{gal}}=%.5e$ $h^3~$Mpc$^{-3}$'%NGAL['1'], transform=ax[0].transAxes)
    ax[1].text(0.05, 0.1, r'Box 5: $\bar{n}_{\mathrm{gal}}=%.5e$ $h^3~$Mpc$^{-3}$'%NGAL['5'], transform=ax[1].transAxes)
    
    ax[1].set_xlabel(r'$\bar{n}_{\mathrm{gal}}^{1/4}~R$ [$h^{-1/4}$ Mpc$^{1/4}$]', fontsize=11)
    [a.set_prop_cycle(cycler(color=colorc)) for a in ax]
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax[0], 
				label='real', 
				ls = '-', ngal = NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax[0], 
				label='redshift', 
				ls = '--', ngal=NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax[1], 
				label='real', ls = '-', lw=1, ngal=NGAL['5'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax[1], 
				label='redshift', 
				ls = '--', ngal=NGAL['5'])
    [a.legend() for a in ax]
    [a.set_yscale('symlog') for a in ax]
    odir = f"{WORKDIR}/patchy_results/box1/plots"
    oname = f"{odir}/box1_vs_box2_wtcoeffs.pdf"
    fitfig.savefig(oname, dpi=200, bbox_inches='tight')
    print(f"==> Saved figure in {oname}")


    # Compare raw void densities with scaled radii for boxes 1 and 5.
    fignv, ax = plt.subplots(1, 1)
    boxes = ['1', '5']
    spaces = ['real', 'redshift']
    raw_nv_fns = []
    for i, box in enumerate(boxes):
        for j, space in enumerate(spaces):
            raw_nv_fns.append(f"{WORKDIR}/patchy_results/box{box}/{space}/nosyst/plots/void_radii_distribution.npy")
            
            Rbins, store_means, _, completeness = load_binaries([raw_nv_fns[-1]],								ax=ax, ngal=NGAL[box],
							label=f" box{box} {space}")
            Rbin_width =  (Rbins[1] - Rbins[0])
    ax.set_xlabel(r'$\bar{n}_{\mathrm{gal}}^{1/4}~R$', fontsize=12)
    ax.set_ylabel(r'$n_{\mathrm{void}}$', fontsize=12)
    ax.legend(loc='best')
    fignv.tight_layout()
    oname=f"{odir}/nv_vs_scaledR.pdf"
    fignv.savefig(oname, dpi=200, bbox_inches='tight')
    print(f"==> Saved figure in {oname}")
    

    
