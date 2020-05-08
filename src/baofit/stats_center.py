#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from getdist import loadMCSamples, MCSamples, plots
from pymultinest.analyse import Analyzer
import sys, os

def stats_center(fileroot, nparams=3, plot = True, cat_type=None):
  # Accepts cat_type for backward compatibility  
  # Set parameter names and labels for plotting 
  npar = nparams   # number of parameters
  print(fileroot)
  if cat_type is not None:
    if cat_type == 'void':
      npar = 4
      names = ['alpha', 'B', 'Snl', 'c']
      labels = [r'\alpha', r'B', r'\Sigma_{\rm nl}', r'c']
    elif cat_type=='gal':
      npar = 3
      names = ['alpha', 'B', 'Snl']
      labels = [r'\alpha', r'B', r'\Sigma_{\rm nl}']
    else:
      sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
  
  names = ['alpha', 'B', 'Snl']
  labels = [r'\alpha', r'B', r'\Sigma_{\rm nl}']
  lowbound = ['N'] * npar
  upbound = ['N'] * npar
  # I/O files
  path, name = os.path.split(fileroot)
  if path == '':
    fileroot = './' + fileroot
  chains = fileroot + '.txt'
  fparam = fileroot + '.paramnames'
  frange = fileroot + '.ranges'
  ofile = fileroot + 'mystats.txt'
  if not os.path.isfile(chains):
    print('Error: cannot access {}'.format(chains), file=sys.stderr)
    sys.exit(1)
  
  np.savetxt(fparam, np.transpose([names, labels]), fmt='%s')
  np.savetxt(frange, np.transpose([names, lowbound, upbound]), fmt='%s')
  # Output file
  ofile = fileroot + 'mystats.txt'

  a = Analyzer(npar, outputfiles_basename=fileroot)
  best = a.get_best_fit()
  stats = a.get_stats()

  # best-fit parameter and minimum chi-squared
  bestfit = best['parameters']
  chi2 = best['log_likelihood'] * -2
  # Median and sigma
  median = []
  sigma_med = []
  med_sigma_med = []
  for j in range(npar):
    med_par = stats['marginals'][j]['median']
    sigma_med_par = stats['marginals'][j]['sigma']
    median.append(med_par)
    sigma_med.append(sigma_med_par)
    med_sigma_med.append(med_par)
    med_sigma_med.append(sigma_med_par)
  # Read evidence from FILE_ROOTstats.dat
  fstat = fileroot + 'stats.dat'
  with open(fstat, "r") as f:
    f.readline()
    line = f.readline()
    evi = float(line.split(':')[1].split()[0])
  med_sigma_med.append(chi2)
  med_sigma_med.append(evi)
  # Export file
  with open(ofile, 'w') as f:
    f.write('{0:.5f} {1:.6f} {2:.5f} {3:.6f} {4:.5f} {5:.6f} {6:.6f} {7:.6f} {8:s}\n'.format(*med_sigma_med, fileroot)) 
  
  # Load samples file to do plots
  if plot:
    sample = loadMCSamples(fileroot, \
        settings={'fine_bins_2D':1024,'fine_bins':8192})
    print(sample)
    g = plots.getSubplotPlotter()
    g.settings.lab_fontsize = 16
    g.triangle_plot(sample, filled='True', \
        line_args={'lw':2,'color':'#006FED'})
    if cat_type == 'void': #Fix c-param plot
      ax = g.subplots[npar-1,npar-1]
      xmin, xmax = ax.get_xlim()
      dx = xmax - xmin
      dx_mag = 10**(int(np.log10(dx)))
      if dx / dx_mag > 5:
        dx_mag *= 2
      elif dx / dx_mag < 2:
        dx_mag /= 2.5
      elif dx / dx_mag < 3:
        dx_mag /= 2
      xmin_new = int(xmin / dx_mag) * dx_mag
      xmax_new = int(xmax / dx_mag) * dx_mag
      nx = int(np.round((xmax_new - xmin_new) / dx_mag + 1))
      if (xmax - xmax_new) / dx < 0.05:
        xmax_new -= dx_mag
        nx -= 1
      if (xmin_new - xmin) / dx < 0.05:
        xmin_new += dx_mag
        nx -= 1
      ax.set_xticks(np.round(np.linspace(xmin_new, xmax_new, nx), 0))
      for ax in g.subplots[npar-1,:npar-1]:
        ax.set_yticks(np.round(np.linspace(xmin_new, xmax_new, nx), 0))

    g.fig.savefig(fileroot+'triplot.pdf', bbox_inches='tight', transparent=True)

def stats_center_getdist(fileroot, cat_type, plot=True):
  # Setting parameter names and ranges
  if cat_type == 'void':
    npar = 4
    names = ['alpha', 'B', 'Snl', 'c']
    labels = [r'\alpha', r'B', r'\Sigma_{\rm nl}', r'c']
  elif cat_type=='gal':
    npar = 3
    names = ['alpha', 'B', 'Snl']
    labels = [r'\alpha', r'B', r'\Sigma_{\rm nl}']
  else:
    sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
  
  lowbound = ['N'] * npar
  upbound = ['N'] * npar
    
  # I/O files
  path, name = os.path.split(fileroot)
  if path == '':
    fileroot = './' + fileroot
  chains = fileroot + '.txt'
  fparam = fileroot + '.paramnames'
  frange = fileroot + '.ranges'
  ofile = fileroot + 'mystats.txt'
  if not os.path.isfile(chains):
    print('Error: cannot access {}'.format(chains), file=sys.stderr)
    sys.exit(1)
  
  np.savetxt(fparam, np.transpose([names, labels]), fmt='%s')
  np.savetxt(frange, np.transpose([names, lowbound, upbound]), fmt='%s')
  
  # Load sample from FILE_ROOT.txt
  sample = loadMCSamples(fileroot, \
      settings={'fine_bins_2D':1024,'fine_bins':8192})
  if plot:
    g = plots.getSubplotPlotter()
    g.settings.lab_fontsize = 16
    g.triangle_plot(sample, filled='True', \
        line_args={'lw':2,'color':'#006FED'})
  stats = sample.getMargeStats()
  par = stats.parWithName(names[0])
  lower = par.limits[0].lower
  upper = par.limits[0].upper
  sigma = (upper - lower) * 0.5
  best = (upper + lower) * 0.5
  
  # Read evidence from FILE_ROOTstats.dat
  fstat = fileroot + 'stats.dat'
  with open(fstat, "r") as f:
    f.readline()
    line = f.readline()
    evi = float(line.split(':')[1].split()[0])
  
  with open(ofile, "w") as f:
    f.write('{0:.5f} {1:.6f} {2:.6f}\n'.format(best, sigma, evi))
  if cat_type == 'void' and plot:
    ax = g.subplots[npar-1,npar-1]
    xmin, xmax = ax.get_xlim()
    dx = xmax - xmin
    dx_mag = 10**(int(np.log10(dx)))
    if dx / dx_mag > 5:
      dx_mag *= 2
    elif dx / dx_mag < 2:
      dx_mag /= 2.5
    elif dx / dx_mag < 3:
      dx_mag /= 2
    xmin_new = int(xmin / dx_mag) * dx_mag
    xmax_new = int(xmax / dx_mag) * dx_mag
    nx = int(np.round((xmax_new - xmin_new) / dx_mag + 1))
    if (xmax - xmax_new) / dx < 0.05:
      xmax_new -= dx_mag
      nx -= 1
    if (xmin_new - xmin) / dx < 0.05:
      xmin_new += dx_mag
      nx -= 1
    ax.set_xticks(np.round(np.linspace(xmin_new, xmax_new, nx), 0))
    for ax in g.subplots[npar-1,:npar-1]:
      ax.set_yticks(np.round(np.linspace(xmin_new, xmax_new, nx), 0))
  if plot:
    g.fig.savefig(fileroot+'triplot.pdf', bbox_inches='tight', transparent=True)
if __name__=='__main__':
  if len(sys.argv) != 3:
    print('Usage: {} FILE_ROOT N_PARAMS'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

  # Getting catalog type
  nparams = int(sys.argv[2])
  fileroot = sys.argv[1]
  stats_center(fileroot, nparams=nparams, plot=True)
