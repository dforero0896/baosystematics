#!/usr/bin/env python
import os
import sys
import re
import pandas as pd
import numpy as np
import matplotlib as mpl
import concurrent.futures
mpl.use("Agg")
import matplotlib.pyplot as plt
import glob
from dotenv import load_dotenv
load_dotenv()
WORKDIR = os.getenv("WORKDIR")
used_seeds=np.loadtxt("/hpcstorage/dforero/projects/baosystematics/data/patchy_boxes/used_patchy.dat", dtype=str)
from pipeline_uniform import pipeline_single_uniform
if os.path.isfile("mocks_to_correct.dat"):
  ifile = open("mocks_to_correct.dat", "r")
  file_list = sorted(ifile.readlines())
  ifile.close() 
  for f in file_list:
    f = f.replace("\n", "")
    if "void_xyz" in f: continue
    SEED = re.sub("_zspace.*$", "",re.sub(r"^.*S","", f))
    COMP = float(re.sub("/mocks_gal_xyz.*$", "",re.sub("^.*flat_", "", f)))
    filename = glob.glob(f"{WORKDIR}/patchy_results/box1/redshift/nosyst/mocks_gal_xyz/*{SEED}*")[0]
    print(COMP)
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
      result = executor.submit(pipeline_single_uniform, filename, COMP).result()
#    pipeline_single_uniform(filename, cmin=COMP)

  sys.exit(0)




#dimless_radii = [0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
dimless_radii = [0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
spaces = ['redshift']
boxes = ['1']
completeness = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
def threshold(c):
  if c==0.1: return 1e4
  elif c<=0.2: return 5e3
  else: return 2e2
faulty_catalogs = []
ofile = open("faulty_2pcf.dat", "w")
for c in completeness:
  for d in dimless_radii:
  
    DIR=f"{WORKDIR}/patchy_results/box1/redshift/smooth/flat_{c}"
    VOID_DIR=f"{DIR}/mocks_void_xyz"
    MOCK_DIR=f"{DIR}/mocks_gal_xyz"
    TPCF_DIR=f"{DIR}/tpcf_void_mock_nowt_R-scaled{d}-50"
    if not os.path.isdir(TPCF_DIR): continue
    print(f"==> Searching dir {TPCF_DIR}.") 
    tpcf_list = glob.glob(f"{TPCF_DIR}/T*")
    data = np.empty((len(tpcf_list), 40))
    residuals = np.copy(data)
    s = np.empty(40)
    counter = 0
    for i, tpcf_fn in enumerate(tpcf_list):
      if i==0: s = pd.read_csv(tpcf_fn, delim_whitespace=True, engine='c', usecols=[0], names=['s']).values[:,0]
      data[i, :] = pd.read_csv(tpcf_fn, delim_whitespace=True, engine='c', usecols=[1], names=['xi0']).values[:,0]
    data *= s[None,:]**2
    #mask = np.any(data[:,-6:] > threshold(c), axis = 1)
    mask = data[:,-6:].mean(axis=1) > threshold(c)
    print(f"==> N outliers: {(mask).sum()} out of {len(mask)} files.")
    tpcf_out = np.asarray(tpcf_list)[mask]
    print(f"==> Before missing tpcf {len(tpcf_out)}")
    if data.shape[0] < 500:
      print(f"==> {data.shape[0]} files found")
      for seed in used_seeds:
        if not any([seed in fn for fn in tpcf_list]):
          #print(os.path.isfile(f"{TPCF_DIR}/TwoPCF_CATALPTCICz0.466G960S{seed}_zspace.flat.sigma0.0_pos_shift.VOID.dat"))
          #tpcf_out = np.append(tpcf_out, f"{TPCF_DIR}/TwoPCF_CATALPTCICz0.466G960S{seed}_zspace.flat.sigma0.0_pos_shift.VOID.dat")
          print(os.path.isfile(f"{TPCF_DIR}/TwoPCF_CATALPTCICz0.466G960S{seed}_zspace.flat.sigma0.0_pos_shift.VOID.R-scaled{d}-50.dat"))
          tpcf_out = np.append(tpcf_out, f"{TPCF_DIR}/TwoPCF_CATALPTCICz0.466G960S{seed}_zspace.flat.sigma0.0_pos_shift.VOID.R-scaled{d}-50.dat")
    print(f"==> After missing tpcf {len(tpcf_out)}")
    for tpcf_fn in tpcf_out:
      ofile.write(f"{tpcf_fn}\n")
      catalog_name = os.path.basename(tpcf_fn).replace("TwoPCF_","").replace(f"R-scaled{d}-50.", "")
      catalog_path=f"{VOID_DIR}/{catalog_name}"
      faulty_catalogs.append(catalog_path)
      catalog_name = os.path.basename(tpcf_fn).replace("TwoPCF_","").replace(f"R-scaled{d}-50.", "").replace(".VOID", "")
      catalog_path=f"{MOCK_DIR}/{catalog_name}"
      faulty_catalogs.append(catalog_path)

      print(tpcf_fn)
    #mean = data[~mask, :].mean(axis=0)
    #std = data[~mask,:].std(axis=0)
    #plt.errorbar(s, mean, yerr=std)
    #[plt.plot(s, y) for y in data[mask,:]]
    #plt.savefig(f"plots/tpcf_plots_c{c}_dr{d}.pdf")
    #plt.cla()
ofile.close()
print(len(faulty_catalogs), len(set(faulty_catalogs)))
ofile = open("mocks_to_correct.dat", "w")
for f in set(faulty_catalogs):
  ofile.write(f"{f}\n")
  SEED = re.sub("_zspace.*$", "",re.sub(r"^.*S","", f))
  print(SEED)
ofile.close()
