#!/usr/bin/env python3
import numpy as np
from getdist import loadMCSamples
import sys, os

if len(sys.argv) != 3:
  print('Usage: {} FILE_ROOT CAT_TYPE'.format(sys.argv[0]), file=sys.stderr)
  sys.exit(1)

# Getting catalog type
cat_type = sys.argv[2]

# Setting parameter names and ranges
if cat_type == 'void':
  npar = 4
  names = ['alpha', 'B', 'Snl', 'c']
  labels = [r'$\alpha$', r'$B$', r'$\Sigma_{\rm nl}$', r'$c$']
elif cat_type=='gal':
  npar = 3
  names = ['alpha', 'B', 'Snl']
  labels = [r'$\alpha$', r'$B$', r'$\Sigma_{\rm nl}$']
else:
  sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')

lowbound = ['N'] * npar
upbound = ['N'] * npar

# I/O files
fileroot = sys.argv[1]
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

