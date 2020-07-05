#!/usr/bin/env python
import numpy as np
def print_config(args_dir):
  for arg, val in args_dir.items():
    print(f"{arg.upper()}:\t{val}")

def read_cnt(ifile, ds=5, isdd=False, ns=200, nmu=120):
  d = np.loadtxt(ifile, unpack=True)
  print(len(d[0]))
  if len(d[0]) != ns/ds * nmu:
    raise ValueError('wrong size of pair count file')

  if ns % ds != 0:
    raise ValueError('wrong bin size of separation')
  sbin = int(ns / ds)
  #cnt = np.sum(d[5].reshape([sbin, ds, nmu]), axis=1)
  cnt = np.sum(d[5].reshape([sbin, 1, nmu]), axis=1)

  if isdd:
    mu = (d[0] + d[1]) * 0.5
   # mu = np.median(mu.reshape([sbin, ds, nmu]), axis=1)
    mu = np.median(mu.reshape([sbin, 1, nmu]), axis=1)
    smin = d[2][0]
    smax = d[3][-1]
    se = np.linspace(smin, smax, sbin+1)
    s = (se[1:] + se[:-1]) * 0.5

    idx = d[5] != 0
    ndata = np.nanmean(np.sqrt(d[4][idx]/d[5][idx]))
    return s, mu, cnt, ndata

  return None, None, cnt, None


def read_xi(dd_file, dr_file, rr_file, ds=5, ns=200, nmu=120):
  dd = [None] * 3
  dr = [None] * 3
  rr = [None] * 3
  xi0 = [None] * 3
  xi2 = [None] * 3
  xi4 = [None] * 3
  num = [None] * 2

  ifile = dd_file
  s, mu, dd, num = read_cnt(ifile, ds=ds, isdd=True, ns=ns, nmu=nmu)
  ifile = dr_file
  _, _, dr, _ = read_cnt(ifile, ds=ds, isdd=False, ns=ns, nmu=nmu)

  ifile = rr_file 
  _, _, rr, _ = read_cnt(ifile, ds=ds, isdd=False, ns=ns, nmu=nmu)

  #nfac = num[1] / num[0]
  #dd[2] = (dd[0] + dd[1] * nfac**2) / (1 + nfac)**2
  #dr[2] = (dr[0] + dr[1] * nfac**2) / (1 + nfac)**2
  #rr[2] = (rr[0] + rr[1] * nfac**2) / (1 + nfac)**2

  #for i in range(3):
  mono = (dd - 2*dr + rr) / rr
  quad = mono * 2.5 * (3 * mu**2 - 1)
  hexa = mono * 1.125 * (35 * mu**4 - 30 * mu**2 + 3)

  xi0 = np.trapz(mono, dx=1./nmu, axis=1)
  xi2 = np.trapz(quad, dx=1./nmu, axis=1)
  xi4 = np.trapz(hexa, dx=1./nmu, axis=1)

  return s, xi0, xi2, xi4

if __name__ == '__main__':
    
    import sys
    import os
    import argparse
    parser = argparse.ArgumentParser(description="Compute 2PCF from DD and RR counts")
    parser.add_argument("-dd", "--dd-file", required=True, help="DD pair counts file.")
    parser.add_argument("-dr", "--dr-file", required=True, help="DR pair counts file.")
    parser.add_argument("-rr", "--rr-file", required=True, help="RR pair counts file.")
    parser.add_argument("-o", "--out-file", required=True, help="Output filename for 2pcf.")
    parsed = parser.parse_args()
    args = vars(parsed)
    print_config(args)
    dd_fn = args['dd_file']
    rr_fn = args['rr_file']
    dr_fn = args['dr_file'] 
    out_fn = args['out_file'] 
    out = np.array(read_xi(dd_fn, dr_fn, rr_fn))
    print(out.shape)
    np.savetxt(out_fn, out.T)
    print(f"==> Saved correlation function in {out_fn}")


