#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from getdist import loadMCSamples, MCSamples, plots
import sys, os

def stats_center(fileroot, cat_type, plot=True):
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
    f.write('{0:.5f} {1:.6f} {2:.6f}'.format(best, sigma, evi))
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
    print('Usage: {} FILE_ROOT CAT_TYPE'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

  # Getting catalog type
  cat_type = sys.argv[2]
  fileroot = sys.argv[1]
  stats_center(fileroot, cat_type, plot=True)
