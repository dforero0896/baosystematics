#!/usr/bin/env python
import numpy as np
def rr_analytic(bin_low_bound, bin_high_bound, box_size):
    volume = 4 * np.pi * (bin_high_bound**3 - bin_low_bound**3) / 3
    normed_volume = volume / box_size **3
    return normed_volume

def tpcf(dd, rr=None, box_size=2500):
    """ Compute the analytic two-point correlation function from the DD pair-counts.

    dd (ndarray): left_bin_edge, right_bin_edge, mono_pair_count, mono_normed_pair_count\
                  quad_pair_count, quad_normed_pair_count, hexa_pair_count, hexa_normed_pair_count.
    box_size (float, optional): Size of the side of the box to consider, in Mpc.
		Default: box_size = 2500"""
    
    if rr is None:    
        rr = rr_analytic(dd[:,0], dd[:,1], box_size)
    else:
        rr = rr[:,2]
        
    delta_s = dd[:,1] - dd[:,0]
    s = dd[:,0] + 0.5 * delta_s
    monopole = ( dd[:,2] / rr ) - 1
    quadrupole =  dd[:,3] / rr 
    hexadecapole = dd[:,4] / rr * 2 
    out = np.c_[s, monopole, quadrupole, hexadecapole].astype(np.float32)
    return out
def read_pair_counts(filename):

    data = np.loadtxt(filename, usecols=(0, 1, 3, 5, 7))
    return data

if __name__ == '__main__':
    
    import sys
    import os
    import argparse
    parser = argparse.ArgumentParser(description="Compute 2PCF from DD and RR counts")
    parser.add_argument("-dd", "--dd-file", required=True, help="DD pair counts file.")
    parser.add_argument("-rr", "--rr-file", required=False, help="RR pair counts file.")
    parser.add_argument("-o", "--out-file", required=True, help="Output filename for 2pcf.")
    parsed = parser.parse_args()
    args = vars(parsed)
    print(args)
    dd_fn = args['dd_file']
    rr_fn = args['rr_file'] or None
    out_fn = args['out_file'] or None
    dd_file = read_pair_counts(dd_fn)
    if rr_fn is not None:
        rr_file = read_pair_counts(rr_fn)
    else: rr_file=None
    np.savetxt(out_fn, tpcf(dd_file, rr_file))
    print(f"==> Saved correlation function in {out_fn}")
