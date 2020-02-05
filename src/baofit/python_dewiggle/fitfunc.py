#!/usr/bin/env python3
import os
import sys
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import simps
from .params import *


def chi2_dist(x, chi2):
  '''Compute the mean and standard deviation given a chi2 distribution.
  Arguments:
    x: the array of parameter values;
    chi2: the corresponding chi-squared.
  Return: [mean, sigma].'''
  # Probabiliry distribution assuming Gaussian variables.
  likelihood = np.exp(-0.5 * chi2)
  normalize = simps(likelihood, x)
  prob_dist = likelihood / normalize
  # Mean value
  mean = simps(x * prob_dist, x)
  # Standard deviation
  sigma = np.sqrt(simps((x - mean)**2 * prob_dist, x))
  return [mean, sigma]


def xi_model_fast(k, Plin, Pnw, nbin, Snl, k2, lnk, eka2, j0):
  '''Compute the template correlation function.
  Arguments:
    k, Plin, Pnw: arrays for the linear power spectra;
    nbin: number of s bins;
    Snl: the BAO damping factor;
    c: the parameter for modeling void non-wiggle power spectrum;
    k2, lnk, eka2, j0: pre-computed values for the model.
  Return: xi_model.'''
  Pm = (Plin - Pnw) * np.exp(-0.5 * k2 * Snl**2) + Pnw
  Pm *= k2 * k * eka2
  xim = np.zeros(nbin)
  if k_interp == True:
    for i in range(nbin):
      xim[i] = np.sum(Pm * j0[i,:] * (lnk[1] - lnk[0]))
  else:
    for i in range(nbin):
      xim[i] = simps(Pm * j0[i,:], lnk)
  return xim


def get_cov():
  '''Read/Compute the pre-processed covariance matrix.
  Return: [Nmock, Rcov], where Rcov is the upper triangular matrix from the
    QR decomposition of the mock matrix.'''
  if compute_cov == True:
     # Read the list of 2PCF from mocks
     mocks = []
     with open(input_mocks) as f:
       for line in f:
         fname = line.rstrip('\n')
         if fname != '':
           mocks.append(fname)
     Nmock = len(mocks)

     # Read 2PCF of mocks
     ximock = [None] * Nmock
     for i in range(Nmock):
       ximock[i] = np.loadtxt(mocks[i], usecols=(1,), unpack=True)
     ximock = np.array(ximock)

     # Compute the mock matrix M (C = M^T . M)
     mean = np.mean(ximock, axis=0)
     ximock -= mean

     # QR decomposition of M
     Rcov = np.linalg.qr(ximock, mode='r')

     if save_cov == True:
       np.savetxt(cov_file, Rcov, header=str(Nmock))
  else:         # comput_cov = False
    with open(cov_file) as f:
      Nmock = int(f.readline())
    Rcov = np.loadtxt(cov_file, skiprows=1)

  return [Nmock, Rcov]


def get_index(sd, fitmin, fitmax):
  '''Get indices of the data to be fitted.
  Arguments:
    sd: s bins for the data;
    fitmin: minimum s for the fitting;
    fitmax: maximum s for the fitting.
  Return: [index_min, index_max, num_index].'''
  imin = imax = -1
  for i in range(sd.size):
    if imin == -1 and sd[i] >= fitmin:
      imin = i
    if imax == -1 and sd[i] > fitmax:
      imax = i
      break

  if imin == -1 or imax == -1:
    print('Error: cannot find the fitting range in data.', file=sys.stderr)
    sys.exit(1)

  nidx = imax - imin
  if nidx < 1:
    print('Error: cannot find enough bins for fitting.', file=sys.stderr)
    sys.exit(1)

  return [imin, imax, nidx]


def init_lstsq(sd, Rcov, npoly, imin, imax):
  '''Initialize the least square fitting for nuisance parameters.
  Refs:
    Numerical Recipes 3rd edition, section 15.4.
    (But the matrix manipulations are simplified here.)
  Arguments:
    sd: the s array for data;
    Rcov: the upper triangular matrix from QR decomp of cov;
    npoly: the number of nuisance parameters;
    imin: the minimum index for the fitting range;
    imax: the maximum index for the fitting range.
  Return: [basis function, design matrix, RHS matrix for LS].'''
  # The basis function and design maxtrix
  nd = sd.size
  basis = np.zeros([npoly, nd])
  A = np.zeros([npoly, nd])
  for i in range(npoly):
    basis[i,imin:imax] = sd[imin:imax]**(i - 2)
    A[i,:] = fwd_subst(Rcov, basis[i,:])

  # Construct U from the QR decomposition of A
  U = np.linalg.qr(np.transpose(A), mode='r')
  # Construct M = U^{-T} . A^T
  M = np.zeros([npoly, nd])
  col = np.zeros(npoly)
  for i in range(nd):
    col = fwd_subst(U, A[:,i])
    M[:,i] = col
  # Construct M . R^{-T}
  for i in range(npoly):
    M[i,:] = bwd_subst(Rcov, M[i,:])

  return [basis, U, M]


def pk_lin():
  '''Run camb (if necessary) and read the linear matter power spectrum.
  Return: [k, P(k)].'''
  if plin_run == True:
    pk_file = call_camb()
  else:
    pk_file = input_plin

  try:
    k, Pk = np.loadtxt(pk_file, comments='#', unpack=True, usecols=(0,1))
  except:
    print('Error: cannot read the linear power spectrum file.', file=sys.stderr)
    sys.exit(1)

  return [k, Pk]


def pk_nw(k, Plin):
  '''Compute the non-wiggle matter P(k) with the Eisenstein & Hu 1998 formulae.
  Arguments: array of k and the linear P(k).
  Return: P_nw (k).'''
  if pnw_run == True:
    Omh2 = Omega_m * h**2
    Obh2 = Omega_b * h**2
    Ofac = Omega_b / Omega_m
    # Eq. 26
    s = 44.5 * np.log(9.83 / Omh2) / np.sqrt(1 + 10 * Obh2**0.75)
    # Eq. 31
    alpha = 1 - 0.328*np.log(431*Omh2)*Ofac + 0.38*np.log(22.3*Omh2)*Ofac**2
    # Eq. 30
    Gamma = Omega_m * h * (alpha + (1 - alpha) / (1 + (0.43 * k * s)**4))
    # Eq. 28
    q = k * (Tcmb / 2.7)**2 / Gamma
    # Eq. 29
    L0 = np.log(2 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1 + 62.5 * q)
    T0 = L0 / (L0 + C0 * q**2)
    Pnw = T0**2 * k**ns
  else:         # pnw_run == False
    knw, Pnw0 = np.loadtxt(input_pnw, comments='#', unpack=True, usecols=(0,1))
    fnw = interp1d(knw, Pnw0, kind='cubic')
    Pnw = fnw(k)
  # Re-normalize the non-wiggle P(k) with the amplitudes at k < k_norm.
  A = np.mean(Plin[k < k_norm] / Pnw[k < k_norm])
  Pnw = Pnw * A
  return Pnw


def call_camb():
  '''Set the configuration file for CAMB and run it.
  Return: filename of the output matter power spectrum.'''
  file_root = 'CAMB'
  str_conf = '''output_root = %s
get_scalar_cls = F
get_transfer = T
w = %g
hubble = %g
use_physical = T
ombh2 = %.8g
omch2 = %.8g
omnuh2 = %.8g
omk = %.8g
temp_cmb = %g
helium_fraction = %g
massless_neutrinos = %g
nu_mass_eigenstates = %g
massive_neutrinos = %g
share_delta_neff = T
nu_mass_fractions = %g
transfer_high_precision = T
transfer_kmax = %g
transfer_k_per_logint = 100
transfer_num_redshifts = 1
transfer_interp_matterpower = F
transfer_power_var = 7
transfer_redshift(1) = %g
transfer_filename(1) = transfer_out.dat
transfer_matterpower(1) = matterpower.dat
reionization = F
initial_power_num = 1
scalar_spectral_index(1) = %s
scalar_nrun(1) = 0
scalar_nrunrun(1) = 0
scalar_amp(1) = %s
accurate_polarization = T
accurate_reionization = T
output_file_headers = F
massive_nu_approx = 1''' % (file_root, w, h*100.0, Omega_b*h**2, \
    (Omega_m-Omega_b)*h**2-omnuh2, omnuh2, omk, Tcmb, helium_fraction, \
    massless_neutrinos, nu_mass_eigenstates, massive_neutrinos, \
    nu_mass_fractions, transfer_kmax, transfer_redshift, ns, scalar_amp)

  conf_file = 'CAMB.ini'
  try:
    # Save the configuration file
    f = file(conf_file, 'w')
    f.write(str_conf)
    f.close()
    # Call CAMB
    os.system(camb_exe+' '+conf_file)
  except:
    print('Error: failed to run CAMB!', file=sys.stderr)
    print('Please check your params, or run CAMB manually.', file=sys.stderr)
    sys.exit(1)

  # Clean the configuration file and unused outputs.
  os.remove(conf_file)
  os.remove(file_root+'_transfer_out.dat')
  os.remove(file_root+'_params.ini')

  pklin_file=file_root+'_matterpower.dat'
  return pklin_file


def fwd_subst(R, b):
  '''Forward substitution.'''
  n = b.size
  x = np.zeros(n)
  for i in range(n):
    x[i] = b[i]
    for j in range(i):
      x[i] -= R[j,i] * x[j]
    x[i] /= R[i,i]
  return x


def bwd_subst(R, b):
  '''Backward substitution.'''
  n = b.size
  x = np.zeros(n)
  for i in range(n-1,-1,-1):
    x[i] = b[i]
    for j in range(i+1,n):
      x[i] = x[i] - R[i][j] * x[j]
    x[i] /= R[i][i]
  return x


