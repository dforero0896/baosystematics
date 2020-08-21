#!/usr/bin/env python
import numpy as np
import os
import sys
from cosmo_calc import *
from test_baorec import *
from scipy.interpolate import interp1d
import zeus
import corner
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from multiprocessing import Pool
def model(k, z, b, plin_interp):
    a = 1./ (1+z)
    return plin_interp(k) * D(a)**2 * b**2

def loglike(theta, data, plin_interp):

    z, b = theta
    model_eval = model(data[:,0], z, b, plin_interp)
    
    return -0.5 * np.sum(((model_eval - data[:,1])/np.std(data[:,1]))**2)

def logprior(theta, kind='gauss'):

    z, b = theta
    lp = 0.
    if kind == 'flat':
        zmin, zmax = -10, 10
        bmin, bmax = -10, 10
        #lp = 0 if zmin < z < zmax else -np.inf
        #lp = 0 if bmin < b < bmax else -np.inf
        pz = 1 if zmin < z < zmax else 0
        pb = 1 if bmin < b < bmax else 0
        lp -= np.log(pz)
        lp -= np.log(pb)
    elif kind =='gauss':
        zmu, zsigma = 3, 2
        lp -= 0.5 * ((z - zmu) / zsigma)**2
        bmu, bsigma = 2, 2
        lp -= 0.5 * ((b-bmu) / bsigma)**2
    elif kind =="mix":
        zmin, zmax = 0, 10
        lp = 0 if zmin < z < zmax else -np.inf
        bmu, bsigma = 2, 2
        lp -= 0.5 * ((b-bmu) / bsigma)**2
        
    else : raise NotImplementedError

    return lp

def logpost(theta, data, plin_interp):

    return logprior(theta) + loglike(theta, data, plin_interp)

if __name__ == '__main__':

    plin_data = np.loadtxt(plin)
    plin_interp = interp1d(plin_data[:,0], plin_data[:,1]) 
    data = np.loadtxt(after_file, usecols = [0,5])
    ndim =2
    nwalkers = 20
    nsteps = 4000

    start = 0.01 * np.random.randn(nwalkers, ndim)
    with Pool() as pool:
        sampler = zeus.sampler(nwalkers, ndim, logpost, args = [data, plin_interp], pool=pool)
        sampler.run_mcmc(start, nsteps)
    sampler.summary

    # flatten the chains, thin them by a factor of 10, and remove the burn-in (first half of the chain)
    chain = sampler.get_chain(flat=True, discard=nsteps//2, thin=10)

    # plot marginal posterior distributions
    fig = corner.corner(chain, labels=['z', 'b'], truths=[3, 2]);

    fig.savefig("fit_zeff.pdf")
    labels=['m','c']
    for i in range(ndim):
        mcmc = np.percentile(chain[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        txt = "\mathrm{{{3}}} = {0:.3f}_{{-{1:.3f}}}^{{{2:.3f}}}"
        txt = txt.format(mcmc[1], q[0], q[1], labels[i])
        print(mcmc)
        #print(mcmc[1], q[0], q[1])
