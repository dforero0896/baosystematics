#!/usr/bin/env python3
import sys
import os
import numpy as np
from scipy.interpolate import interp1d
from .fitfunc import *
from .params import *
from scipy.special import spherical_jn
from scipy.optimize import minimize

if not os.path.isdir(output_dir):
  print('Error: output_dir "{}" does not exist.'.format(output_dir),\
      file=sys.stderr)
  sys.exit(1)
bname = input_data.split('/')[-1]
logfile = output_dir + '/BAOfit_' + bname + '.log'
outfile = output_dir + '/BAOfit_' + bname + '.out'
bestfile = output_dir + '/BAOfit_' + bname + '.best'

print('Read the input 2PCF to be fitted.')
try:
  sd, xid = np.loadtxt(input_data, usecols=(0,1), unpack=True)
  ndbin = sd.size
except:
  print('Error: cannot read the input data.', file=sys.stderr)
  sys.exit(1)

print('Get the indices of data for fitting.')
imin, imax, nidx = get_index(sd, fit_smin, fit_smax)
if npoly >= nidx:
  print('Error: too many nuisance parameters.', file=sys.stderr)
  sys.exit(1)

print('Read/Compute the covariance matrix.')
nmock, Rcov = get_cov()
if nmock < nidx + 3:
  print('Error: the number of mocks is not enough.', file=sys.stderr)
  sys.exit(1)
if ndbin != Rcov.shape[0]:
  print('Error: bin size of data and mocks do not match.', file=sys.stderr)
  sys.exit(1)
chi2_norm = nmock - nidx - 2

print('Initialize matrices for least square fitting of the nuisance params.')
basis, A, M = init_lstsq(sd, Rcov, npoly, imin, imax)

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

Pnw = pk_nw(k, Plin)

print('Pre-compute terms for the model')
k2 = k**2
eka2 = np.exp(-k2 * damp_a**2) * 0.5 / np.pi**2
sm = np.linspace(smin, smax, num_s_bin)

nkbin = k.size
nsbin = sm.size
j0 = np.zeros([nsbin, nkbin])
for i in range(nsbin):
  j0[i,:] = spherical_jn(0, sm[i] * k)


def chi2_func(params, alpha):
  '''Define the (log) likelihood.'''
  Snl, B = params[0], params[1]
  # Compute the model 2PCF with a given alpha
  xim = xi_model_fast(k, Plin, Pnw, nsbin, Snl, k2, lnk, eka2, j0)
  fxim = interp1d(sm, xim, kind='cubic')
  xi = fxim(sd[imin:imax] * alpha)

  # Least square fitting of nuisance parameters
  dxi = xid[imin:imax] - xi * B**2
  poly = np.dot(M[:,imin:imax], dxi)
  a_poly = bwd_subst(A, poly)

  # Compute chi-squared
  diff = np.zeros(ndbin)
  diff[imin:imax] = dxi - np.dot(np.transpose(basis[:,imin:imax]), a_poly)
  chisq = np.sum((fwd_subst(Rcov, diff))**2)
  return chisq * chi2_norm


def best_fit(params, alpha):
  '''Compute the best-fit theoretical curve.'''
  Snl, B = params[0], params[1]
  # Compute the model 2PCF with a given alpha
  xim = xi_model_fast(k, Plin, Pnw, nsbin, Snl, k2, lnk, eka2, j0)
  fxim = interp1d(sm, xim, kind='cubic')
  xi = fxim(sd[imin:imax] * alpha)

  # Least square fitting of nuisance parameters
  dxi = xid[imin:imax] - xi * B**2
  poly = np.dot(M[:,imin:imax], dxi)
  a_poly = bwd_subst(A, poly)

  # Compute best-fit
  if alpha >= 1:
    imin0, imax0, nidx0 = get_index(sm, sm[1], sm[-2] / alpha)
  else:
    imin0, imax0, nidx0 = get_index(sm, sm[1] / alpha, sm[-2])
  best = B**2 * fxim(sm[imin0:imax0] * alpha)
  for i in range(npoly):
    best += a_poly[i] * sm[imin0:imax0]**(i - 2)
  return [sm[imin0:imax0], best]


# Run minimum finder for grids of alpha
galpha = np.linspace(amin, amax, anum)
chi2 = np.zeros(anum)
minchi2 = 1e99
dim = 2
ic = np.ones(dim)
minx = np.zeros(dim)
besta = 0

flog = open(logfile, 'w', 1)

for i in range(anum):
  print('Fitting for alpha = {0:g} ({1:d}/{2:d})'.format(galpha[i], i+1, anum))
  res = minimize(chi2_func, ic, args=(galpha[i],),\
      method='Powell',\
      options={'maxiter':100000, 'maxfev':100000, 'xtol':1e-6, 'ftol':1e-6})

  chi2[i] = chi2_func(res.x, galpha[i])
  strlog = '{0:g} {1:g}'.format(galpha[i], chi2[i])
  for j in range(dim):
    strlog += ' {0:g}'.format(res.x[j])
  strlog += '\n'
  flog.write(strlog)

  if minchi2 > chi2[i]:
    minchi2 = chi2[i]
    besta = galpha[i]
    minx = res.x

#  ic = res.x  # The best-fit as the initial guess of the next iteration.

flog.close()

mean, sigma = chi2_dist(galpha, chi2)
dof = len(sd) - len(ic) - npoly

with open(outfile, 'w') as f:
  f.write('# mean_alpha sigma_alpha best_alpha min_chi2 dof Snl B\n')
  f.write('{0:g} {1:g} {2:g} {3:g} {4:g}'.format(mean, sigma,\
      besta, minchi2, dof))
  for i in range(dim):
    f.write(' {0:g}'.format(minx[i]))
  f.write('\n')

sb, bestfit = best_fit(minx, besta)
np.savetxt(bestfile, np.transpose([sb,bestfit]), fmt='%g')

