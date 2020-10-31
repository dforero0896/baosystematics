#!/usr/bin/env python

import os
import sys
import numpy as np
import pandas as pd
import time
import gc
from Corrfunc.theory.xi import xi
from dotenv import load_dotenv
load_dotenv()
from mask_comp_func import mask_with_function
from params import flat, NGRID, NGAL
WORKDIR=os.environ.get("WORKDIR")
sys.path.append(f"{WORKDIR}/bin/pydive/pydive")
from dive import galaxies_to_voids
sys.path.append(f"{WORKDIR}/bin/Revolver")
from python_tools.galaxycat import GalaxyCatalogue
from python_tools.recon import Recon
from python_tools.fastmodules import survey_cuts_logical

def box_void_tpcf(catalog, catalog_fn, box_size, nthreads, bins, bin_centers, odir, comp, ngal_complete=NGAL['1'], recon=False):
  if recon and comp <= 0.25: r_dimless=[0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
  elif recon and comp == 0.3: r_dimless=[0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13]
  elif recon and comp > 0.3: r_dimless=[0.8, 0.87, 0.93, 1.0, 1.07, 1.13]
  elif not recon: r_dimless=[0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
  nthreads=32
  BASE=os.path.basename(catalog_fn)
  data = pd.DataFrame(catalog, columns=['x', 'y', 'z', 'r'])
  data.set_index("r", inplace=True)
  data.sort_index(0, inplace=True)
  Ntot = data.shape[0]
  #mask = data.index <= 50
  #data = data.loc[mask]
  data = data.loc[:50]
  OLD_BASE=BASE
  current_time = time.time()
  for sr in r_dimless:

        RMIN=sr/((comp*ngal_complete)**(1./3))
        ODIR=f"{odir}/tpcf_void_mock_nowt_R-scaled{sr}-50"
        os.makedirs(ODIR, exist_ok=True)
        os.makedirs(ODIR+"/DD_files", exist_ok=True)
        if recon:
          BASE = OLD_BASE#.replace(".dat", f".R-scaled{sr}-50.dat")
        else:
          BASE = OLD_BASE.replace(".dat", f".R-scaled{sr}-50.dat")
        DD=f"{ODIR}/DD_files/DD_{BASE}"
        TPCF=f"{ODIR}/TwoPCF_{BASE}"
        print(f"==> DD COUNTS:\t{DD}")
        print(f"==> OUTPUT:\t{TPCF}")
        try:
            time_since_creation = current_time - os.path.getmtime(TPCF)
            time_threshold = current_time - 1603882800
            print(time_since_creation, time_threshold)
#            if time_since_creation < time_threshold:
#                print(f"==> 2PCF recently computed, skipping.")
#                continue
        except OSError:
            pass
        d_sel=data.loc[RMIN:].values
        print(f"==> Rmin = {RMIN}, Rmax =50")
        N = d_sel.shape[0]
        print(f"==> Using {N}/{Ntot} tracers")
        xi_counts = xi(box_size, nthreads, bins, d_sel[:,0], d_sel[:,1], d_sel[:,2], verbose=True) 
        out=np.c_[bin_centers, xi_counts['xi'], np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
        np.savetxt(TPCF, out, fmt="%.3f %.8e %.0f %.0f")
        print(f"==> The correlation function is saved.")
        out=np.c_[xi_counts['rmin'], xi_counts['rmax'], xi_counts['npairs'], xi_counts['npairs']/(N * N), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
        np.savetxt(DD, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
        print(f"==> The DD counts are saved.", flush=True)



def reconstruction(catalog, cat_fn, odir, filename="params_recon_ds.py"):

  if os.access(filename, os.F_OK):
    print('Loading parameters from %s' % filename)
    if sys.version_info.major <= 2:
        import imp
        parms = imp.load_source("name", filename)
    elif sys.version_info.major == 3 and sys.version_info.minor <= 4:
        from importlib.machinery import SourceFileLoader
        parms = SourceFileLoader("name", filename).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location("name", filename)
        parms = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parms)
  else:
    sys.exit('Did not find settings file %s, aborting' % filename)
 
  handle_dat = os.path.splitext(os.path.basename(cat_fn))[0]
  handle_ran = handle_dat+'.ran'
  parms.__dict__['handle'] = handle_dat
  parms.__dict__['handle_ran'] = handle_ran
  parms.__dict__['output_folder'] = odir
  parms.__dict__['tracer_file'] = cat_fn
  for name in ['handle', 'handle_ran', 'output_folder', 'tracer_file', 'bias', 'f']:
    print(f"{name}:\t{parms.__dict__[name]}")
  
  os.makedirs(parms.output_folder, exist_ok=True)

  if parms.do_recon:
    print('\n ==== Running reconstruction for real-space positions ==== ')

    cat = GalaxyCatalogue(parms, randoms=False)

    recon = Recon(cat, ran=None, parms=parms)
    start = time.time()
    # now run the iteration loop to solve for displacement field
    if not parms.rsd_corr:
    
        print("==> RSD correction is %s, forcing niter=1."%parms.rsd_corr)
        parms.niter=1
    
    for i in range(parms.niter):
        recon.iterate(i, debug=parms.debug)

    # get new ra, dec and redshift for real-space positions
    
    if not parms.is_box:
        cat.ra, cat.dec, cat.redshift = recon.get_new_radecz(recon.cat)

    #recon.summary()    
    print("==> Applying shifts", flush=True) 
    recon.apply_shifts_full()    
    #recon.summary()    
    # save real-space positions to file
    root = parms.output_folder + parms.handle + '_pos'
    root2 = parms.output_folder + parms.handle_ran + '_pos'
    recon.export_shift_pos(root, root2=root2, rsd_only=False, save_mode=2)

    print(" ==== Done reconstruction ====\n")
    end = time.time()
    print("Reconstruction took %0.3f seconds" % (end - start))
  

def pipeline_single_uniform(filename, cmin):

  #filename is the complete, non reconstructed patchy galaxy catalog
  box_size=2500
  n_threads=32
  overwrite=True
  odir = os.path.abspath(os.path.dirname(filename)+"/../../")
  basename = os.path.basename(filename)
  rng=np.random.default_rng()
  print(f"==> Reading complete galaxy catalog")

  gal = pd.read_csv(filename, delim_whitespace=True, usecols=(0, 1, 2), names=['x', 'y', 'z'], engine="c")  
  print(f"==> Complete number of galaxies {gal.shape}")

  ds_gal_fn = f"{odir}/smooth/flat_{cmin}/mocks_gal_xyz/{basename.replace('.dat', '.flat.sigma0.0.dat')}"
  if not os.path.isfile(ds_gal_fn) or overwrite:
    
    print(f"==> Masking complete catalog with completeness {cmin}")
    mask_function = lambda y, x: flat(y, x, NGRID, cmin)
    ds_gal = mask_with_function(gal, mask_function, noise=False, box_size=box_size, N_grid=NGRID, sigma_noise=0, cmin=cmin, noise_sampler=lambda x:0, seed=rng.integers(low=0, high=1000)).iloc[:,:3]
    print(f"==> Saving {ds_gal_fn}")
    np.savetxt(ds_gal_fn, ds_gal, fmt="%.4f")
  else:
    ds_gal = pd.read_csv(ds_gal_fn, delim_whitespace=True, engine="c", usecols=(0, 1, 2), names=['x', 'y', 'z'])
  print(f"==> Downsampled number of galaxies {ds_gal.shape}") 
  

  print(f"==> Setting up reconstruction", flush=True)
  ds_gal_recon_odir = os.path.dirname(ds_gal_fn).replace("patchy_results", "patchy_recon_nods")+"/"
  ds_gal_recon_fn = f"{ds_gal_recon_odir}/{os.path.basename(ds_gal_fn).replace('.dat', '_pos_shift.npy')}"
#  if not os.path.isfile(ds_gal_recon_fn) or overwrite:
#    reconstruction(ds_gal, ds_gal_fn, ds_gal_recon_odir)

  print(f"Loading reconstructed galaxy catalog", flush=True)
#  ds_gal_recon = np.load(ds_gal_recon_fn)
#  print(f"==> Downsampled number of reconstructed galaxies {ds_gal_recon.shape}") 

#  print(f"==> Extracting voids from reconstructed catalog", flush=True)
  ds_voids_recon_fn = ds_gal_recon_fn.replace('mocks_gal_xyz', 'mocks_void_xyz').replace('.npy', '.VOID.npy')
#  if not os.path.isfile(ds_voids_recon_fn) or overwrite:
#    ds_voids_recon = galaxies_to_voids(ds_gal_recon.astype(np.double), box_size=box_size, is_box=True, cpy_range=80, n_threads=n_threads)
#    print(f"==> Saving reconstructed void catalog", flush=True)
#    np.save(ds_voids_recon_fn, ds_voids_recon)
#  else:
#    ds_voids_recon = np.load(ds_voids_recon_fn)
  ds_voids_recon_fn = ds_voids_recon_fn.replace(".npy", ".dat")

  bins = np.linspace(0.0001, 200, 41)
  bin_centers = 0.5 * (bins[1:] + bins[:-1])

  print(f"==> Computing reconstructed void 2PCF")
#  box_void_tpcf(ds_voids_recon, ds_voids_recon_fn, box_size, 32, bins, bin_centers, f"{odir.replace('patchy_results', 'patchy_recon_nods')}/smooth/flat_{cmin}/", cmin, NGAL['1'], recon=True) 
  

  print(f"==> Extracting voids from downsampled catalog", flush=True)
  ds_voids_fn = ds_gal_fn.replace('mocks_gal_xyz', 'mocks_void_xyz').replace('.dat', '.VOID.dat')
  if not os.path.isfile(ds_voids_fn.replace(".dat", ".npy")) or overwrite:
    ds_voids = galaxies_to_voids(ds_gal.values.astype(np.double), box_size=box_size, is_box=True, cpy_range=80, n_threads=n_threads)
    print(f"==> Saving voids from downsampled catalog")
    np.save(ds_voids_fn.replace(".dat", ".npy"), ds_voids)
  else:
    ds_voids=np.load(ds_voids_fn.replace(".dat", ".npy"))
  print(f"==> Downsampled number of voids {ds_voids.shape}")

  print(f"==> Computing downsampled void 2PCF")
  box_void_tpcf(ds_voids, ds_voids_fn, box_size, 32, bins, bin_centers, f"{odir}/smooth/flat_{cmin}/", cmin, NGAL['1'], recon=False) 
  
  del ds_gal
#  del ds_gal_recon
  del ds_voids
#  del ds_voids_recon
  gc.collect()

if __name__ == '__main__':
  test_filename=f"{WORKDIR}/patchy_results/box1/redshift/nosyst/mocks_gal_xyz/CATALPTCICz0.466G960S1005638091_zspace.dat"
  pipeline_single_uniform(test_filename, cmin=0.1)

