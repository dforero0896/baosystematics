#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
from scipy import interpolate, optimize
import sys
import os
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import *
def load_binaries(filenames, ax = None, ngal=None, **kwargs):
   
    store_means=np.empty((len(filenames), 100))
    store_stds = np.copy(store_means)
    completeness = []
    for i, data_bin in enumerate(filenames):
        try:
            label = data_bin.split('/')[-3]
            completeness.append(float(label.replace('flat_', '')))
        except: label = '1'
        data = np.load(data_bin)
        data_mean = data[:,:,1].mean(axis=0)
        store_means[i,:] = data_mean
        data_std = data[:,:,0].std(axis=0)
        store_stds[i,:] = data_std
        Rbins = data[0,:,0]
        try:
            add_label=kwargs.pop('label')
        except:
            add_label=''
        if ax is not None:
            if ngal is not None: r_scaling = ngal**(1./3)
            else: r_scaling=1
            ax.plot(r_scaling * Rbins, data_mean, label = label+add_label, **kwargs)
            ax.fill_between(r_scaling * Rbins, data_mean-data_std, data_mean+data_std, alpha=0.2)
    
    return Rbins, store_means, store_stds, completeness

def find_intersection_arrays(x, y1, y2, **kwargs):

    fhist1 = interpolate.interp1d(x, y1)
    fhist2 = interpolate.interp1d(x, y2)
    xstar = optimize.fsolve(lambda x_: fhist1(x_) - fhist2(x_), **kwargs)
    ystar = fhist1(xstar)
    return xstar, ystar
if __name__ == '__main__':
    WORKDIR = '/home/epfl/dforero/scratch/projects/baosystematics'
    if len(sys.argv) < 3:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} BIN_HIST_1 [... BIN_HIST_N] ODIR")
    data_bins = sys.argv[1:-1]
    odir = sys.argv[-1]
    fig, ax = plt.subplots(1, 1)
    os.makedirs(odir, exist_ok=True) 
    Rbins, store_means, store_stds, completeness = load_binaries(data_bins, ax=ax)
    Rbin_width =  (Rbins[1] - Rbins[0])
    # Get point where curves cross
    Rstar, nstar = find_intersection_arrays(Rbins, store_means[0], store_means[1], x0 = 13)
    ax.plot(Rstar, nstar, 'ro', label = r'$R^* = %.3f$ $h^{-1}$ Mpc'%Rstar)
    ax.set_xlabel(r'$R$ [$h^{-1}$ Mpc]', fontsize=15)
    ax.set_ylabel(r'Void number density', fontsize=15)
    ax.legend()
    ax.set_xlim(0, 30)
    fig.tight_layout()
    oname = f"{odir}/void_ndensity_vs_size_vs_comp.pdf"
    fig.savefig(oname, dpi=200)
    cfig, ax = plt.subplots(1,2, figsize=(9,4))
    # Iterate over radius bins
    data_complete = store_means[0,:] #n
    std_complete = store_stds[0,:] #delta n
    sorted_comp_ids = np.argsort(completeness)
    completeness = np.array(completeness)[sorted_comp_ids]
    galaxy_weights = 1 / np.array(completeness)
    galaxy_weights_linsp = np.linspace(min(galaxy_weights), max(galaxy_weights), 100)
    print(f"==> WARNING: The program assumes the first argument passed was the raw (no systematics) void distribution npy")
    fit_params_container = []
    used_R = []
    for i,R in enumerate(Rbins):
        data = store_means[1:,i] #n'
        std = store_stds[1:, i] #delta n'
        data = data[sorted_comp_ids]
        std = std[sorted_comp_ids]
        # Discard "empty" bins
        if any(data<1e-8) or data_complete[i] < 1e-10: continue
        void_comp = data/data_complete[i] # Void completeness assumes first argument is void distribution w/o systematics.
        void_comp_error = np.sqrt((std/data_complete[i])**2 + (data * std_complete[i] / (data_complete[i]**2))**2)
        void_weights = 1 / void_comp
        # Do polynomial fit to weight relations.
        fit_poly = np.polynomial.polynomial.Polynomial.fit(galaxy_weights, void_weights, deg = 2)
        fit_params_container.append(fit_poly.coef) #[x0, x1, x2]
        used_R.append(R)
        # Plot some of the fits.
        if i%10==0:
            ax[0].errorbar(completeness, void_comp, yerr=void_comp_error, label = '$R \in (%.1f, %.1f)$'%(R-0.5 * Rbin_width, R + 0.5 * Rbin_width), marker = 'o')
            points = ax[1].errorbar(galaxy_weights, void_weights, yerr=void_comp_error/void_comp**2, label = '$R \in (%.0f, %.0f)$'%(R-Rbin_width, R + Rbin_width), marker = 'o', lw = 0)
            ax[1].plot(galaxy_weights_linsp, fit_poly(galaxy_weights_linsp), color = points[0].get_color())
    ax[0].set_xlabel('Galaxy completeness', fontsize=15)
    ax[0].set_ylabel('Void completeness', fontsize=15)
    ax[1].set_xlabel('Galaxy weights', fontsize=15)
    ax[1].set_ylabel('Void weights', fontsize=15)
    ax[0].legend()
    cfig.tight_layout()
    oname = f"{odir}/void_ndensity_vs_comp_vs_size.pdf"
    cfig.savefig(oname, dpi=200)


    fitfig, ax = plt.subplots(1,1, figsize=(7, 5), constrained_layout=True)
    fitfig.suptitle('Model: $w_v(R) = c_0(R) + c_1(R)w_g + c_2(R)w_g^2$', fontsize=15)
    fit_params_container = np.array(fit_params_container)
    used_R = np.array(used_R)
    # Change env variables:
    RMIN, RMAX =16, 50
    R_mask = (used_R > RMIN) & (used_R < RMAX)
    R_linsp = np.linspace(0.1, 50, 100)
    # Iterate over coefficients to fit to c_i(R)
    axins = ax.inset_axes([0.5, 0.5, 0.5, 0.5])
    for i in range(3):
        fit_coeff = np.polynomial.polynomial.Polynomial.fit(used_R[R_mask], fit_params_container[R_mask,i], deg = 1)
        fit_coeff_coeff = fit_coeff.coef
        pts, = ax.plot(used_R, fit_params_container[:,i], marker = 'o', label = '$c_%i = %.2f  %+.2fR$'%(i, *fit_coeff.coef))
        ax.plot(R_linsp, fit_coeff(R_linsp), color=pts.get_color())
        axins.plot(used_R, fit_params_container[:,i], marker = 'o', label = '$c_%i = %.2f  %+.2fR$'%(i, *fit_coeff.coef))
        axins.plot(R_linsp, fit_coeff(R_linsp), color=pts.get_color())
        axins.set_xlim(RMIN, RMAX)
        axins.set_ylim(-0.5, 1.5)
 
        ax.set_ylabel('$c_i$', fontsize=15)
    
    ax.set_xlabel(r'$R$ [$h^{-1}$ Mpc]', fontsize=15)
    ax.legend()
    #fitfig.tight_layout()
    oname = f"{odir}/void_weight_fits.pdf"
    print(f"==> Saved coefficients plot to {odir}/void_weight_fits.pdf")
    fitfig.savefig(oname, dpi=200)
    fit_params_out = np.concatenate((used_R[:,None], fit_params_container), axis=1)
    np.savetxt(f"{odir}/void_weight_c_of_r.dat", fit_params_out, fmt = "%.3f %.3f %.3f %.3f")
    print(f"==> Saved fit coefficients to {odir}/void_weight_c_of_r.dat")



