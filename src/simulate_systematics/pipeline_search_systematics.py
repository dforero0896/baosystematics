#!/usr/bin/env python

import os
import sys
import numpy as np
import pandas as pd
import time
import gc
import glob
import subprocess
from Corrfunc.theory.xi import xi
from Corrfunc.theory.DD import DD
from Corrfunc.utils import convert_3d_counts_to_cf
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get("WORKDIR")
SRC=os.environ.get("SRC")
sys.path.append(f"{WORKDIR}/bin/pydive/pydive")
from dive import galaxies_to_voids
sys.path.append(f"{WORKDIR}/bin/Revolver")
from python_tools.galaxycat import GalaxyCatalogue
from python_tools.recon import Recon
from python_tools.fastmodules import survey_cuts_logical
from params import *
sys.path.append(f"{SRC}/void_weights")
from apply_void_weights import get_numdens_from_matrix, get_numdens_radial

def box_void_tpcf(data, box_size, nthreads, bins, bin_centers, TPCF, ddfn, RMIN, RMAX, overwrite=False):
  nthreads=32
  current_time = time.time()
  print(f"==> DD COUNTS:\t{ddfn}")
  print(f"==> OUTPUT:\t{TPCF}")
  N = data.shape[0]
  print(f"==> Rmin = {RMIN}, Rmax = {RMAX}")
  xi_counts = xi(box_size, nthreads, bins, data[:,0], data[:,1], data[:,2], verbose=True) 
  out=np.c_[bin_centers, xi_counts['xi'], np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
  np.savetxt(TPCF, out, fmt="%.3f %.8e %.0f %.0f")
  print(f"==> The correlation function is saved.")
  out=np.c_[xi_counts['rmin'], xi_counts['rmax'], xi_counts['npairs'], xi_counts['npairs']/(N * N), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
  np.savetxt(ddfn, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
  print(f"==> The DD counts are saved.", flush=True)

def box_void_tpcf_ls(data, rand, box_size, nthreads, bins, bin_centers, TPCF, RMIN, RMAX, rrfn=None, ddfn=None, drfn=None, overwrite=False):
  nthreads=32
  current_time = time.time()
  print(f"==> DD COUNTS:\t{ddfn}")
  print(f"==> OUTPUT:\t{TPCF}")
  print(f"==> Rmin = {RMIN}, Rmax = {RMAX}")
  
  Ndata = data.shape[0]
  Nrand = rand.shape[0]
  if not os.path.isfile(ddfn) or overwrite:
    print(f"==> Computing DD counts", flush=True)
    DD_c = DD(1, nthreads, bins, data[:,0], data[:,1], data[:,2], weights1=None, periodic=True, verbose=True, boxsize=box_size)
    out=np.c_[bins[:-1], bins[1:], DD_c['npairs'], DD_c['npairs']/(Ndata * Ndata), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
    np.savetxt(ddfn, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
    print(f"==> The DD counts are saved.", flush=True)
  else:
    DD_c = np.genfromtxt(ddfn, usecols=(2,), names=['npairs'])
  
  if rrfn is None or not os.path.isfile(rrfn):
    print(f"==> Computing RR counts", flush=True)
    RR = DD(1, nthreads, bins, rand[:,0], rand[:,1], rand[:,2], weights1=None, periodic=True, verbose=True, boxsize=box_size)
    out=np.c_[bins[:-1], bins[1:], RR['npairs'], RR['npairs']/(Nrand * Nrand), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
    np.savetxt(rrfn, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
    print(f"==> The RR counts are saved.", flush=True)
  else:
    RR = np.genfromtxt(rrfn, usecols=(2,), names=['npairs'])
  if not os.path.isfile(drfn) or overwrite:
    print(f"==> Computing DR counts", flush=True)
    DR = DD(0, nthreads, bins, data[:,0], data[:,1], data[:,2], weights1=None, periodic=True, verbose=True, boxsize=box_size, X2=rand[:,0], Y2=rand[:,1], Z2=rand[:,2], weights2=None)
    out=np.c_[bins[:-1], bins[1:], DR['npairs'], DR['npairs']/(Ndata * Nrand), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
    np.savetxt(drfn, out, fmt="%.8f %.8f %.2f %.8e %.0f %.0f %.0f %.0f")
    print(f"==> The DR counts are saved.", flush=True)
  else:
    DR = np.genfromtxt(drfn, usecols=(2,), names=['npairs'])

  xi = convert_3d_counts_to_cf(Ndata, Ndata, Nrand, Nrand, DD_c, DR, DR, RR)
  out=np.c_[bin_centers, xi, np.zeros_like(bin_centers), np.zeros_like(bin_centers)]
  np.savetxt(TPCF, out, fmt="%.3f %.8e %.0f %.0f")
  print(f"==> The correlation function is saved.")


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
  

def pipeline_single(njobs, jobid, n_threads, onlyrr=True):

  box_size=2500
  overwrite=True
  bins = np.linspace(0.00001, 200, 41)
  bin_centers = 0.5 * (bins[1:] + bins[:-1])
  RMAX = 50

  for space in ['redshift', 'real'][::-1]:
    for box in ['1', '5']:
#      ngal = NGAL[box]
      for syst in ['radialgauss', 'smooth/parabola_0.8']:
        print(f"{space} {box} {syst}")
        odir = f"{WORKDIR}/patchy_results/box{box}/{space}/{syst}"
        if syst == "radialgauss":
          void_rand_fn = f"{odir}/void_ran/void_ran.dat"
          #vran = pd.read_csv(void_rand_fn, delim_whitespace=True, usecols=(0, 1, 2, 3, 4), engine="c", names= ['x', 'y', 'z', 'r', 'sr']).values
          #vran = vran[vran[:,3]<RMAX]
        filenames = glob.glob(f"{odir}/mocks_gal_xyz/CAT*")
        myfilenames = np.array_split(filenames, njobs)[jobid]
        for filename in myfilenames:
          gal_fn=filename
          #print(f"==> Reading complete galaxy catalog")

          gal = pd.read_csv(filename, delim_whitespace=True, usecols=(0, 1, 2), names=['x', 'y', 'z'], engine="c").values
          print(f"==> Complete number of galaxies {gal.shape}")
          ngal = gal.shape[0] / (box_size)**3
          del gal
          voids_fn = gal_fn.replace('mocks_gal_xyz', 'mocks_void_xyz').replace('.dat', '.VOID.dat')
          #print(f"==> Reading void catalog.", flush=True)
          #if syst=='radialgauss':
          #  voids = pd.read_csv(voids_fn, delim_whitespace=True, names=['x', 'y', 'z', 'r'], usecols=(0, 1, 2, 3), engine="c").values
          #elif syst=='smooth/parabola_0.8':
          #  voids = pd.read_csv(voids_fn, delim_whitespace=True, names=['x', 'y', 'z', 'r', 'w'], usecols=(0, 1, 2, 3, 4), engine="c").values



          print(f"==> Computing radius cuts: ")
          

          r_dimless=[0.87, 0.93, 1.0, 1.13, 1.19, 1.25, 1.33]
          if box=='1' and space=='redshift' and syst=='radialgauss':
              r_dimless=[1.]
          elif box=='1' and space=='redshift' and syst=='smooth/parabola_0.8':
              r_dimless=[1.19]
          elif box=='1' and space=='real' and syst=='radialgauss':
              r_dimless=[1.]
          elif box=='1' and space=='real' and syst=='smooth/parabola_0.8':
              r_dimless=[1.13]
          elif box=='5' and space=='redshift' and syst=='radialgauss':
              r_dimless=[0.93]
          elif box=='5' and space=='redshift' and syst=='smooth/parabola_0.8':
              r_dimless=[1.]
          elif box=='5' and space=='real' and syst=='radialgauss':
              r_dimless=[0.93]
          elif box=='5' and space=='real' and syst=='smooth/parabola_0.8':
              r_dimless=[1.]
          for sr in r_dimless:
          
            RMIN = sr / (ngal**(1./3))
            print(RMIN)
            break
            TPCF=f"{odir}/tpcf_void_mock_nowt_R-dl{sr}-{RMAX}/"
            os.makedirs(TPCF, exist_ok=True)
            os.makedirs(f"{TPCF}/DD_files/", exist_ok=True)
            DD_f = TPCF+f"/DD_files/DD_{os.path.basename(voids_fn)}"
            TPCF+=f"TwoPCF_{os.path.basename(voids_fn)}"
            #print(DD_f, TPCF)
            if os.path.isfile(TPCF):
                if os.path.getmtime(TPCF)>1607355694:
                    print("==> Skipping TPCF since it was recently created")
                    continue
            #mask_data = (voids[:,3] > RMIN) & (voids[:,3] < RMAX)  
            if syst=='radialgauss':
             # mask_rand = (vran[:,3] > RMIN)
              RR = os.path.dirname(TPCF)+f"/RR_files"
              os.makedirs(RR, exist_ok=True)
              RR +=f"/RR_void_ran_R-dl{sr}-{RMAX}.dat"
              DR = os.path.dirname(TPCF)+f"/DR_files"
              os.makedirs(DR, exist_ok=True)
              DR+=f"/DR_{os.path.basename(voids_fn)}"
              if os.path.isfile(RR): 
                print(f"==> Found RR counts, nor rewriting.")
                count_mode=3
              else: count_mode=7
              print(count_mode)
              subprocess.check_call(["srun", "-n1", f"-c{n_threads}", f"{WORKDIR}/bin/FCFC_box/2pcf", "--conf=fcfc.conf", f"--data={voids_fn}", f"--rand={void_rand_fn}", f"--dd={DD_f}", f"--dr={DR}", f"--rr={RR}", f"--output={TPCF}", "--data-aux-col=4", "--rand-aux-col=4", f"--data-aux-min={RMIN}", f"--data-aux-max={RMAX}", f"--rand-aux-min={RMIN}", f"--rand-aux-max={RMAX}", f"--count-mode={count_mode}", "--moment=2", "--cf-mode=1"])
              #box_void_tpcf_ls(voids[mask_data], vran[mask_rand], box_size, n_threads, bins, bin_centers, TPCF, RMIN, RMAX, RR, DD_f, DR)
            elif syst == 'smooth/parabola_0.8': 
              count_mode=1
              #print(f"==> Using {mask.sum()}/{voids.shape[0]} voids", flush=True)
              if onlyrr: continue
              subprocess.check_call(["srun", "-n1", f"-c{n_threads}", f"{WORKDIR}/bin/FCFC_box/2pcf", "--conf=fcfc.conf", f"--data={voids_fn}", f"--rand={void_rand_fn}", f"--dd={DD_f}", f"--output={TPCF}", "--data-aux-col=4", "--rand-aux-col=4", f"--data-aux-min={RMIN}", f"--data-aux-max={RMAX}", f"--rand-aux-min={RMIN}", f"--rand-aux-max={RMAX}", f"--count-mode={count_mode}", "--moment=2", "--cf-mode=3"])
              #box_void_tpcf(voids[mask_data], box_size, n_threads, bins, bin_centers, TPCF, DD, RMIN, RMAX)  
            else: raise NotImplementedError


          #del gal
          #del voids
          gc.collect()
          if onlyrr: break
if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-njobs", "--njobs", dest="njobs", type=int, default=1)
  parser.add_argument("-jobid", "--jobid", dest="jobid", type=int, default=0)
  parser.add_argument("-nthreads", "--nthreads", dest="nthreads", type=int, default=32)
  args = parser.parse_args()

  pipeline_single(args.njobs, args.jobid, args.nthreads)

