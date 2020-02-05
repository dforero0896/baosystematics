#!/usr/bin/env python
import os
# Parameters for generation of template non-wiggle void Pk.
# The parameters here override those in the .conf files

# Paths 
WORKDIR = '/home/epfl/dforero/scratch/projects/baosystematics'
BIN = os.path.join(WORKDIR, 'bin')
SRC = os.path.join(WORKDIR, 'src')
RESULTS = os.path.join(WORKDIR, 'results')
# Parameters
N = 100 # Number of catalogs to generate
N_in = 1 # Number seed offset in case those already exist
R_min = 15.5 # Radius cut min
R_max = 50 # Radius cut max
box_size = 5000 # Box size in Mpc
halo_density = 12000 # Halo density
n_halo = box_size * halo_density # Number of haloes to output


