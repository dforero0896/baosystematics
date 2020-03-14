import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
NCORES = 32
WORKDIR = "/home/epfl/dforero/scratch/projects/baosystematics"
RESULTS = WORKDIR+"/patchy_results/simulated_systematics"
cmin_map = 0.6
cmin_cut = 0
COMP = RESULTS+"/completeness_cmin%s_halfgauss"%cmin_map
# Please be aware of changing the output directory when changing other params.
BOX = "1"
SPACE = "redshift"
DATA = WORKDIR+"/patchy_results/box%s/%s/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091_zspace.dat"%(BOX, SPACE)
RANDIR = WORKDIR+"/patchy_results/randoms"
RANDOM = RANDIR+"/box_uniform_random_seed1_0-2500.dat"
RUN_FCFC=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')
RUN_DIVE = os.path.join(WORKDIR, 'bin/DIVE_box/DIVE_box') 
box_size=2500
DATA_NOISE=True    

# Define random sampler for noise
from scipy.stats import truncnorm
def noise_sampler(sigma_noise, n_samples):
  return truncnorm.rvs(-np.inf, 0, loc=0, size=n_samples, scale=sigma_noise)

