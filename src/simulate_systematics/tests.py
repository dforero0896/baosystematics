#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
WORKDIR = "/home/epfl/dforero/scratch/projects/baosystematics"
RESULTS = WORKDIR+"/patchy_results/simulated_systematics"
COMP = RESULTS+"/completeness"
BOX = "1"
SPACE = "redshift"
DATA = WORKDIR+"/patchy_results/box%s/%s/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091_zspace.dat"%(BOX, SPACE)
RANDIR = WORKDIR+"/patchy_results/randoms"
RANDOM = RANDIR+"/box_uniform_random_seed1_0-2500_SMALL.dat"
# Define a masking function
if len(sys.argv) != 3:
  sys.exit("USAGE: %s NOISE NGRID"%sys.argv[0])
box_size=2500
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
functions = [parabola, xplane, parabola_off, flat]
ran_comp_mins = [1, 0.1, 0.1, 0.1]
dat_comp_mins = [0.8, 0.1, 0.1, 0.1]

# Import data catalog
names = ['x', 'y', 'z']
data = pd.read_csv(DATA, delim_whitespace = True, usecols=(0, 1, 2), names = names)
rand_wt_col = 4
data_wt_col = 4
# Setup fcfc run
conf_file = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%SPACE
RUN=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')

bash_script=open('joblist.sh', 'w')
for i, function in enumerate(functions):
  # Create data catalog with mask
  masked_dat_fn = os.path.join(COMP, os.path.basename(DATA).replace('.dat', '.ANG.'+function.__name__+'.sigma%s.grid%s.dat'%(sigma_noise, N_grid)))
  if not os.path.exists(masked_dat_fn):
    print("Creating %s"%masked_dat_fn)
    masked_dat = mask_with_function(data, lambda y, x: function(y, x, N_grid, dat_comp_mins[i]), noise=True, box_size=2500, N_grid=N_grid, sigma_noise=sigma_noise)
    masked_dat.to_csv(masked_dat_fn, sep = ' ', header=False, index=False)

  # Create random catalog with mask
  masked_ran_fn = os.path.join(COMP,os.path.basename(RANDOM).replace('.dat', '.ANG.'+function.__name__+".grid%s.dat"%(N_grid)))
  if not os.path.exists(masked_ran_fn):
    print("Creating %s"%masked_ran_fn)
    ran = pd.read_csv(RANDOM, delim_whitespace=True, usecols=(0, 1, 2), names = names)
    masked_ran = mask_with_function(ran, lambda y, x: function(y, x, N_grid, ran_comp_mins[i]), noise=False, box_size=2500, N_grid=N_grid, sigma_noise=sigma_noise)
    masked_ran.to_csv(masked_ran_fn, sep = ' ', header=False, index=False)
  # Define files for fcfc
  for weight in [0,1]:
    dd_file = os.path.join(COMP,"DD_"+os.path.basename(masked_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    dr_file = os.path.join(COMP,"DR_"+os.path.basename(masked_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    rr_file = os.path.join(COMP,"RR_"+os.path.basename(masked_ran_fn).replace('.dat', '.wt%s.dat'%weight))
    out_file = os.path.join(COMP, "TwoPCF_"+os.path.basename(masked_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    if not os.path.exists(rr_file):
      count_mode=7
    else:
      count_mode=3
    if weight == 0 : 
      rand_wt_col=0
      data_wt_col=0
    elif weight == 1:
      rand_wt_col=4
      data_wt_col=4
    bash_script.write('srun -n 1 -c 32 %s --conf=%s --data=%s --rand=%s --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --rand-wt-col=%s --data-wt-col=%s\n'%(RUN, conf_file, masked_dat_fn, masked_ran_fn, count_mode, dd_file, dr_file, rr_file, out_file, rand_wt_col, data_wt_col))
bash_script.close()
