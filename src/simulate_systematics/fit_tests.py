#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *
N_grid = 2500
def xplane(y, x, N_grid, Cmin):
  return ( (1-Cmin) / N_grid ) * x + Cmin
ran_comp_mins = [1, 0.1, 0.1]
dat_comp_mins = [0.8, 0.1, 0.1]

# Import data catalog
names = ['x', 'y', 'z']
rand_wt_col = 4
data_wt_col = 4
# Setup fcfc run
conf_file = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%SPACE
RUN=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')

bash_script=open('joblist_fit.sh', 'w')
function = xplane
mask_dat_fn_list = [f for f in os.listdir(COMP) if f.startswith(os.path.basename(DATA).replace('.dat', '')) and function.__name__ in f and not 'VOID' in f]
for mask_dat_base in mask_dat_fn_list:
  # Load data catalog with mask
  masked_dat_fn = os.path.join(COMP, mask_dat_base)
  masked_dat = pd.read_csv(masked_dat_fn, delim_whitespace = True, usecols=(0, 1, 2, 3, 4), names = ['x', 'y', 'z', 'w', 'comp'])
  # Create random catalog with mask
  masked_ran_fn = os.path.join(COMP,os.path.basename(RANDOM).replace('.dat', mask_dat_base.replace(os.path.basename(DATA).replace('.dat',''), ''))).replace(function.__name__, function.__name__+"_fit")
  # Perform leastsq for plane
  design_matrix = np.c_[np.ones(len(masked_dat)), masked_dat['x'].values]
  weight_vector = np.linalg.solve(design_matrix.T.dot(design_matrix), design_matrix.T.dot(masked_dat['comp'].values))
  print(weight_vector)
  def xplane_fit(y, x, slope, interp):
    return slope * x + interp
  if not os.path.exists(masked_ran_fn):
    print("Creating %s"%masked_ran_fn)
    ran = pd.read_csv(RANDOM, delim_whitespace=True, usecols=(0, 1, 2), names = names)
    masked_ran = mask_with_function(ran, lambda y, x: xplane_fit(y, x, weight_vector[1], weight_vector[0]), noise=False, box_size=2500, N_grid=N_grid)
    masked_ran.to_csv(masked_ran_fn, sep = ' ', header=False, index=False)
  # Define files for fcfc
  for weight in [0,1]:
    dd_file = os.path.join(COMP,"DD_"+os.path.basename(masked_dat_fn).replace(function.__name__, function.__name__+"_fit").replace('.dat', '.wt%s.dat'%weight))
    dr_file = os.path.join(COMP,"DR_"+os.path.basename(masked_dat_fn).replace(function.__name__, function.__name__+"_fit").replace('.dat', '.wt%s.dat'%weight))
    rr_file = os.path.join(COMP,"RR_"+os.path.basename(masked_ran_fn).replace('.dat', '.wt%s.dat'%weight))
    out_file = os.path.join(COMP, "TwoPCF_"+os.path.basename(masked_dat_fn).replace(function.__name__, function.__name__+"_fit").replace('.dat', '.wt%s.dat'%weight))
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
    bash_script.write('srun -n 1 -c %s %s --conf=%s --data=%s --rand=%s --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --rand-wt-col=%s --data-wt-col=%s\n'%(NCORES, RUN, conf_file, masked_dat_fn, masked_ran_fn, count_mode, dd_file, dr_file, rr_file, out_file, rand_wt_col, data_wt_col))
bash_script.close()
