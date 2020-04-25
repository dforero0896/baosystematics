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
from compute_fit_coeffs  import load_binaries

def plot_weight_fit_coeffs(filename, ax, label='', ngal=None, **kwargs):

    data = np.loadtxt(filename)
    if ngal is not None: r_scaling = ngal**(1./3)
    else: r_scaling=1
    print(f"{filename}: {r_scaling}")
    for i in range(1,4):
        ax.plot(r_scaling * data[:,0], data[:,i], label = label+' $c_%i$'%(i-1), **kwargs)
        ax.set_ylabel('$c_i$', fontsize=12)


if __name__ == '__main__':
    fitfig, ax = plt.subplots(1,2, figsize=(12, 5), 
				constrained_layout=True, sharey=True)
    fitfig.suptitle('Model: $w_v(R) = c_0(R) + c_1(R)w_g + c_2(R)w_g^2$', fontsize=12)
    [a.set_xlabel(r'$\bar{n}_{\mathrm{halo}}^{1/3}~R$ [$h^{-1}$ Mpc]', fontsize=12) for a in ax]
    colorc = 'bgr'
    [a.set_prop_cycle(cycler(color=colorc)) for a in ax]
    ax[0].set_title('Real space', fontsize=12)
    ax[1].set_title('Redshift space', fontsize=12)
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax[0], 
				label='real box1', 
				ls = '-', ngal = NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax[1], 
				label='redshift box1', 
				ls = '--', ngal=NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax[0], 
				label='real box5', ls = ':', lw=3, ngal=NGAL['5'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax[1], 
				label='redshift box5', 
				ls = '-.', ngal=NGAL['5'])
    [a.legend() for a in ax]
    [a.set_yscale('symlog') for a in ax]
    odir = f"{WORKDIR}/patchy_results/box1/plots"
    oname = f"{odir}/r_vs_z_wtcoeffs.pdf"
    fitfig.savefig(oname, dpi=200)
    print(f"==> Saved figure in {oname}")
    [a.clear() for a in ax] 


    ax[0].set_title(r'Box 1: $\bar{n}_{\mathrm{halo}}=%.5e$ $h^3~$Mpc$^{-3}$'%NGAL['1'])
    ax[1].set_title(r'Box 5: $\bar{n}_{\mathrm{halo}}=%.5e$ $h^3~$Mpc$^{-3}$'%NGAL['5'])
    
    [a.set_xlabel(r'$\bar{n}_{\mathrm{halo}}^{1/3}~R$ [$h^{-1}$ Mpc]', fontsize=12) for a in ax]
    colorc = 'bgr'
    [a.set_prop_cycle(cycler(color=colorc)) for a in ax]
    plot_weight_fit_coeffs('void_weights_c_of_r_real.dat', ax=ax[0], 
				label='real box1', 
				ls = '-', ngal = NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift.dat', ax=ax[0], 
				label='redshift box1', 
				ls = '--', ngal=NGAL['1'])
    plot_weight_fit_coeffs('void_weights_c_of_r_real_box5.dat', ax=ax[1], 
				label='real box5', ls = ':', lw=3, ngal=NGAL['5'])
    plot_weight_fit_coeffs('void_weights_c_of_r_redshift_box5.dat', ax=ax[1], 
				label='redshift box5', 
				ls = '-.', ngal=NGAL['5'])
    [a.legend() for a in ax]
    [a.set_yscale('symlog') for a in ax]
    odir = f"{WORKDIR}/patchy_results/box1/plots"
    oname = f"{odir}/box1_vs_box2_wtcoeffs.pdf"
    fitfig.savefig(oname, dpi=200)
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
    ax.set_xlabel(r'$\bar{n}_{\mathrm{gal}}^{1/3}~R$', fontsize=12)
    ax.set_ylabel(r'$n_{\mathrm{void}}$', fontsize=12)
    ax.legend(loc='best')
    fignv.tight_layout()
    oname=f"{odir}/nv_vs_scaledR.pdf"
    fignv.savefig(oname, dpi=200)
    print(f"==> Saved figure in {oname}")
    

    
