#!/usr/bin/env python
import os
import numpy as np
import matplotlib as mpl
from scipy.interpolate import interp1d
mpl.use('Agg')
import matplotlib.pyplot as plt
from cosmo_calc import *
import glob
z=0.4656
before_file = glob.glob("/hpcstorage/dforero/projects/baosystematics/patchy_results/box1/real/nosyst/powspec_gal_mock_nowt/powspec_CATALPTCICz0.466G960S1005638091*")[0]
print(before_file)
after_file = glob.glob("/home/astro/dforero/scratch/projects/baosystematics/patchy_recon/box1/real/nosyst/powspec_gal_mock_nowt/powspec_CATCATALPTCICz0.466G960S1005638091*")[0]
print(after_file)
after_file_old = glob.glob("./powspec*1005638091*")[0]
plin = "/hpcstorage/dforero/projects/baosystematics/data/LinearSpectra/Pk.input_zinit_normalized_at_z0.DAT"
pbaorec_before="/hpcstorage/dforero/projects/baosystematics/patchy_recon/box5/real/nosyst/mocks_gal_xyz/powCATALPTCICz0.638G960S1005638091.dat.dat"
pbaorec_after="/hpcstorage/dforero/projects/baosystematics/patchy_recon/box5/real/nosyst/mocks_gal_xyz/powBAORECCATALPTCICz0.638G960S1005638091.datrS5.0.dat"
def normalizePk(z, Pk):
    a = 1./(1+z)
    norm = (D(a)/D(1))**2
    print(f"Then: {D(a)}")
    print(f"Now: {D(1)}")
    return Pk * norm
def plot_powspec(ifile, **kwargs):
    k, Pk = np.loadtxt(ifile, usecols=[0, 5], unpack = True)
    plt.loglog(k, Pk, **kwargs)
if __name__ == '__main__':
    
    plin_data = np.loadtxt(plin)
    pbefore_data = np.loadtxt(before_file, usecols=[0,5])
    pafter_data = np.loadtxt(after_file, usecols=[0,5])
#    pbaorec_before_data = np.loadtxt(pbaorec_before)
#    pbaorec_after_data = np.loadtxt(pbaorec_after)
    plin_interp = interp1d(plin_data[:,0], plin_data[:,1]) 
    plot_powspec(before_file, label="Before")
    plt.loglog(plin_data[:,0], plin_data[:,1], label='Linear norm at z=0')
    plt.loglog(plin_data[:,0], normalizePk(z,plin_data[:,1]), label=f'Linear norm at z={z}')
    #print(f"sqrt(Sim/Plin(z={z})) = {np.sqrt(pbefore_data[:,1] / normalizePk(z,plin_interp(pbefore_data[:,0])))}")
    bias =np.sqrt(pbefore_data[:,1] / normalizePk(z,plin_interp(pbefore_data[:,0])))
    
    for i, z in enumerate(np.concatenate(([0.,z],np.linspace(1, 4, 5)))):
        a = 1./(1+z)
        b=2.2
        model = plin_data[:,1] * (D(a)/D(1))**2 * b**2
    #    print(f"Model z = {z}: Plin/Model = {plin_data[:,1]/model}.")
        plt.loglog(plin_data[:,0], model, label="%.2f"%z)
    plot_powspec(after_file, label="After", ls='--', color='k')
    #plot_powspec(after_file_old, label="After old code", ls='--')
#    plt.loglog(pbaorec_before_data[:,0], pbaorec_before_data[:,1], label='BR before')
#    plt.loglog(pbaorec_after_data[:,0], pbaorec_after_data[:,1], label='BR after')
    plt.ylim(1e2, 1e6)
    plt.legend()
    plt.gcf()
    oname = "before_after_pspec.pdf"
    plt.savefig(oname, dpi=300)
    print(f"==> Saved {os.path.realpath(oname)}.")
