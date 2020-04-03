import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
NCORES = 16
BOX = "1"
NMOCKS = 500
SPACE = "real"
# Define relevant paths
WORKDIR = "/home/epfl/dforero/scratch/projects/baosystematics"
RESULTS = WORKDIR+"/patchy_results"
ODIR = RESULTS+f"/box{BOX}/{SPACE}"
cmin_map = 0.8
cmin_cut = 0
COMP = RESULTS+"/simulated_systematics/completeness_cmin%s_halfgauss"%cmin_map
# Please be aware of changing the output directory when changing other params.
DATA = WORKDIR+"/patchy_results/box%s/%s/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091_zspace.dat"%(BOX, SPACE) # Small-scale tests only
RANDIR = WORKDIR+"/patchy_results/randoms" # Small-scale tests only
RANDOM = RANDIR+"/box_uniform_random_seed1_0-2500.dat" # Small-scale tests only 
RUN_FCFC=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')
RUN_DIVE = os.path.join(WORKDIR, 'bin/DIVE_box/DIVE_box') 
box_size=2500
DATA_NOISE=True    

# Define random sampler for noise
from scipy.stats import truncnorm
def noise_sampler(sigma_noise, n_samples):
  return truncnorm.rvs(-np.inf, 0, loc=0, size=n_samples, scale=sigma_noise)
#noise_sampler = None

# Define masking functions to be used
def parabola(y, x, N_grid, Cmin):
  return -(2 * (1-Cmin) / N_grid**2 ) * ((x- 0.5 * N_grid)**2 +\
		 (y- 0.5 * N_grid)**2) + 1
def xplane(y, x, N_grid, Cmin):
  return ( (1-Cmin) / N_grid ) * x + Cmin
def flat(y, x, N_grid, Cmin):
  return Cmin
def parabola_off(y, x, N_grid, Cmin):
  return -((1-Cmin)/(2*N_grid**2)) * (x**2 + y**2) + 1
funclist = [parabola, xplane, flat, parabola_off]

# Define which function is actually being used
FUNCTION = parabola

# Define radius and distance bins to sample denstities
radius_bins = np.append(np.linspace(0, 21, 22), [25, 30, 50])
radius_bin_widths = radius_bins[1:] - radius_bins[:-1]
xy_bins = 256
xedges = np.linspace(0, box_size, xy_bins+1)
yedges = np.linspace(0, box_size, xy_bins+1)
