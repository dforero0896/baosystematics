#!/usr/bin/env python
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from python_dewiggle.fitfunc import xi_model_fast, pk_lin, pk_nw
from scipy.special import spherical_jn
from scipy.interpolate import interp1d
import sys
import os
from python_dewiggle.params import *
plt.rcParams.update({'font.size': 12})

#path in lesta
#/home/epfl/atamone/old/LastClaudio/Covariance/shuffle/outputnormalv7b/v7wosys/no_RIC/ALL/ELG_ALL_bin8_mean_xi0.dat
if len(sys.argv) != 4:
	sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s INPUT_2PCF BIAS SIGMA_NL\n'%sys.argv[0])
ifile = sys.argv[1]
idata = np.loadtxt(ifile)
s = idata[:,0]
xi_mean = idata[:,1]
xi_std = idata[:,2]
def plot_xi(data, **kwargs):
	plt.plot(data[:,0], data[:,0]**2*data[:,1], **kwargs)
def plot_xi_std(data, **kwargs):
	plt.fill_between(data[:,0], data[:,0]**2*(data[:,1]-data[:,2]),data[:,0]**2*(data[:,1]+data[:,2]), **kwargs)

print('Generate the linear power spectra')
if k_interp == False:
  k, Plin = pk_lin()
  lnk = np.log(k)
else:
  lnk = np.linspace(np.log(kmin), np.log(kmax), num_lnk_bin)
  k = np.exp(lnk)

  k0, Plin0 = pk_lin()
  fint = interp1d(np.log(k0), np.log(Plin0), kind='cubic')
  Plin = np.exp(fint(lnk))
Pnw = pk_nw(k,Plin)
print('Pre-compute terms for the model')
k2 = k**2
eka2 = np.exp(-k2 * damp_a**2) * 0.5 / np.pi**2
sm = np.linspace(smin, smax, num_s_bin)
nkbin = k.size
nsbin = sm.size
j0 = np.zeros([nsbin, nkbin])
for i in range(nsbin):
  j0[i,:] = spherical_jn(0, sm[i] * k)
Snl = float(sys.argv[3])
xi_template = xi_model_fast(k, Plin, Pnw, nsbin, Snl, k2, lnk, eka2, j0)
bias_sq =float(sys.argv[2])**2
xi_template*=bias_sq
plt.plot(sm, sm**2*xi_template, label='$\Sigma_{nl} = %i,\ B^2=%.2f$'%(Snl, bias_sq))
plot_xi(idata, lw = 3, ls=':', c='k')
plot_xi_std(idata, color='r', alpha=0.2)
#plt.xlim(82, 122)
#plt.xlim(8, 70)
plt.legend(loc=0)
plt.xlabel(r'$s$ $[h^{-1}$ Mpc$]$', fontsize=15)
plt.ylabel(r'$s^2\xi_0$', fontsize=15)
plt.tight_layout()
plt.show()
