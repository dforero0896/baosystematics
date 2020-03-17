#!/usr/bin/env python
import pandas as pd
import numpy as np
def mask_with_function(data, comp_mesh, seed=2, noise=True, box_size=2500, N_grid=None, sigma_noise=0.3, cmin=0, noise_sampler=None):
  np.random.seed(seed)
  if not N_grid:
    print("Using N_grid = box_size")
    N_grid = box_size
  ix = data['x'] * N_grid // box_size
  iy = data['y'] * N_grid // box_size
  comp = comp_mesh(iy, ix)
  data['w']=1/np.clip(comp, cmin, 1) #save weights as inverse smooth completeness
  rand = np.random.random(len(data))
  print(f"Noise = {noise}")
  if noise:
    if noise_sampler is not None:
      print("Using non-default noise sampler.")
      comp += noise_sampler(len(data)) # noise sampler must accept number of samples to graw as parameter.
    else:
      comp += np.random.normal(0, sigma_noise, len(data)) #add noise to completeness
  data['comp']=np.clip(comp, cmin, 1)
  data_ret = data[data['comp'] > rand]
  return data_ret
if __name__ == '__main__':
  import sys
  if len(sys.argv)!=5:
    sys.exit("ERROR: Unexpected number of arguments.\nUSAGE: %s CATALOG OUT_BASE SUFFIX NOISE"%sys.argv[0])
  data_fn=sys.argv[1]
  obase = sys.argv[2]
  suffix = sys.argv[3]
  noise = bool(int(sys.argv[4]))
  data = pd.read_csv(data_fn, delim_whitespace=True, usecols=(0, 1, 2, 3), names=['x', 'y', 'z', 'r'])
  parabola = (lambda y, x: -1.6e-7*((x-1250)**2 + (y-1250)**2) + 1)
  egg_cart = (lambda y, x: -0.25*(np.sin(8*np.pi*x/2500) + np.sin(8*np.pi*y/2500))+0.75)
  masked_data = mask_with_function(data, egg_cart, noise=noise)
  masked_data.to_csv(obase+".ANG.%s.dat"%suffix, sep = " ", header=False, index=False)
