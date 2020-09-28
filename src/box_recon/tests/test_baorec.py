#!/usr/bin/env python
import os
import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.interpolate import interp1d
mpl.use('Agg')
import matplotlib.pyplot as plt
from cosmo_calc import *
import glob
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.getenv("WORKDIR")
boxes = ['1', '5']
spaces=['redshift']#, 'real']
redshift=dict(zip(boxes, [0.466, 0.638]))

plin = "/hpcstorage/dforero/projects/baosystematics/data/LinearSpectra/Pk.input_zinit_normalized_at_z0.DAT"
def normalizePk(z, Pk):
    a = 1./(1+z)
    norm = (D(a)/D(1))**2
    print(f"Then: {D(a)}")
    print(f"Now: {D(1)}")
    return Pk * norm
def plot_powspec(ifile, **kwargs):
    data = [pd.read_csv(f, usecols=[0, 5], comment='#', engine='c', delim_whitespace=True, names=['k', 'Pk']).values for f in ifile]
    data = np.array(data)
    print(data.shape)
    avg = data.mean(axis=0)
    print(avg.shape)
    std = data.std(axis=0)
    print(std.shape)
    plt.errorbar(avg[:,0], avg[:,1], yerr=std[:,1], **kwargs)
    return np.c_[avg, std[:,1]]
if __name__ == '__main__':
    plin_data = np.loadtxt(plin)
    plin_interp = interp1d(plin_data[:,0], plin_data[:,1]) 
    plt.loglog(plin_data[:,0], plin_data[:,1], label='Linear norm at z=0', ls='--')
    print(redshift.values())
    for i, z in enumerate(np.concatenate(([0],list(redshift.values()),np.linspace(1, 4, 5)))):
        a = 1./(1+z)
        b=1.92
        model = plin_data[:,1] * (D(a)/D(1))**2 * b**2
    #    print(f"Model z = {z}: Plin/Model = {plin_data[:,1]/model}.")
        plt.loglog(plin_data[:,0], model, label="%.2f"%z, ls='-.')
    for box in boxes:
        for space in spaces:
            z = redshift[box]    
            path = f"{WORKDIR}/patchy_recon/box{box}/{space}/nosyst/powspec_gal_mock_nowt/powspec*"
            print(path)
            after_file = glob.glob(path)
            print(len(after_file))
            after_data=plot_powspec(after_file, label=f"After box {box} {space}")
            plt.loglog(plin_data[:,0], normalizePk(z,plin_data[:,1]), label=f'Linear norm at z={z}', ls='--')
            #print(f"sqrt(Sim/Plin(z={z})) = {np.sqrt(pbefore_data[:,1] / normalizePk(z,plin_interp(pbefore_data[:,0])))}")
            #bias =np.sqrt(pbefore_data[:,1] / normalizePk(z,plin_interp(pbefore_data[:,0])))
    
    plt.ylim(1e2, 1e6)
    plt.legend()
    plt.gcf()
    oname = "before_after_pspec.pdf"
    plt.savefig(oname, dpi=300)
    print(f"==> Saved {os.path.realpath(oname)}.")
