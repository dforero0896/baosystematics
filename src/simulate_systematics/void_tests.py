#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *

# Import data catalog
names = ['x', 'y', 'z']
data_aux_col = 4
data_aux_min = 16
data_aux_max = 50
mask_dat_fn_list = [f for f in os.listdir(COMP) if f.startswith(os.path.basename(DATA).replace('.dat', '')) and 'VOID' not in f]
# Setup fcfc run
conf_file = WORKDIR+"/src/fcfc_box/fcfc_box_void_count_%s.conf"%SPACE

bash_script=open('joblist_void.sh', 'w')
for mask_dat_base in mask_dat_fn_list:
  # Data catalog with mask
  masked_dat_fn = os.path.join(COMP, mask_dat_base)
  in_name, in_ext = os.path.splitext(os.path.basename(masked_dat_fn))
  output_dat_fn = os.path.join(COMP, in_name+'.VOID'+in_ext)
  if os.path.exists(output_dat_fn):
    continue
  command = '%s %s %s %s %s %s\n'%(RUN_DIVE, masked_dat_fn, output_dat_fn, str(box_size), '0', '999')
  bash_script.write(command)
  # Define files for fcfc
  masked_ran_fn = os.path.join(COMP,os.path.basename(RANDOM).replace('.dat', mask_dat_base.replace(os.path.basename(DATA).replace('.dat',''), '')))
  for weight in [0]:
    dd_file = os.path.join(COMP,"DD_"+os.path.basename(output_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    dr_file = os.path.join(COMP,"DR_"+os.path.basename(output_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    rr_file = os.path.join(COMP,"RR_"+os.path.basename(masked_ran_fn).replace('.dat', '.wt%s.dat'%weight))
    out_file = os.path.join(COMP, "TwoPCF_"+os.path.basename(output_dat_fn).replace('.dat', '.wt%s.dat'%weight))
    if not os.path.exists(rr_file):
      count_mode=7
    else:
      count_mode=3
    if weight == 0 : 
      rand_wt_col=0
      data_wt_col=0
    elif weight == 1:
      rand_wt_col=5
      data_wt_col=5
    bash_script.write('srun -n 1 -c %s %s --conf=%s --data=%s --rand=%s --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --rand-wt-col=%s --data-wt-col=%s --data-aux-col=%s --data-aux-min=%s --data-aux-max=%s\n'%(NCORES, RUN_FCFC, conf_file, masked_dat_fn, masked_ran_fn, count_mode, dd_file, dr_file, rr_file, out_file, rand_wt_col, data_wt_col, data_aux_col, data_aux_min, data_aux_max))
bash_script.close()
