#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *
# Define a masking function
if len(sys.argv) != 3:
  sys.exit("USAGE: %s NOISE NGRID"%sys.argv[0])
N_grid = int(sys.argv[2]) #2500
sigma_noise = float(sys.argv[1]) #0.4
print("Grid size: %s\tNoise level: %s"%(N_grid, sigma_noise))
def parabola(y, x, N_grid, Cmin):
  return -(2 * (1-Cmin) / N_grid**2 ) * ((x- 0.5 * N_grid)**2 + (y- 0.5 * N_grid)**2) + 1
def xplane(y, x, N_grid, Cmin):
  return ( (1-Cmin) / N_grid ) * x + Cmin
def flat(y, x, N_grid, Cmin):
  return Cmin
def parabola_off(y, x, N_grid, Cmin):
  return -((1-Cmin)/(2*N_grid**2)) * (x**2 + y**2) + 1
functions = [flat, parabola, xplane, parabola_off]
ran_comp_mins = [1, cmin_map, cmin_map, cmin_map]
dat_comp_mins = [0.8, cmin_map, cmin_map, cmin_map]

# Import data catalog
names = ['x', 'y', 'z']
data = pd.read_csv(DATA, delim_whitespace = True, usecols=(0, 1, 2), names = names)
rand_wt_col = 4
data_wt_col = 4
# Setup fcfc run
conf_file = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%SPACE
RUN=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')
nsampler = lambda size: noise_sampler(sigma_noise, size)
#nsampler=None


bash_script=open('joblist_analyt.sh', 'w')
for i, function in enumerate(functions):
  # Create data catalog with mask
  masked_dat_fn = os.path.join(COMP, os.path.basename(DATA).replace('.dat', '.ANG.'+function.__name__+'.sigma%s.grid%s.dat'%(sigma_noise, N_grid)))
  if not os.path.exists(masked_dat_fn):
    print("Creating %s"%masked_dat_fn)
    masked_dat = mask_with_function(data, lambda y, x: function(y, x, N_grid, dat_comp_mins[i]), noise=DATA_NOISE, box_size=2500, N_grid=N_grid, sigma_noise=sigma_noise, cmin=cmin_cut, noise_sampler=nsampler)
    masked_dat.to_csv(masked_dat_fn, sep = ' ', header=False, index=False)
  # Define files for fcfc
  for weight in [0,1]:
    dd_file = os.path.join(COMP,"DD_"+os.path.basename(masked_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    dr_file = os.path.join(COMP,"DR_"+os.path.basename(masked_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    out_file = os.path.join(COMP, "TwoPCF_"+os.path.basename(masked_dat_fn).replace('.dat', '.ANALYT.wt%s.dat'%weight))
    if not os.path.exists(dd_file):
      count_mode=1
    else:
      NCORES=1
      count_mode=0
    if weight == 0 : 
      rand_wt_col=0
      data_wt_col=0
    elif weight == 1:
      rand_wt_col=4
      data_wt_col=4
    bash_script.write('srun -n 1 -c %s %s --conf=%s --data=%s --count-mode=%s --dd=%s --dr=%s --output=%s --rand-wt-col=%s --data-wt-col=%s --cf-mode=3\n'%(NCORES, RUN, conf_file, masked_dat_fn, count_mode, dd_file, dr_file, out_file, rand_wt_col, data_wt_col))
bash_script.close()
