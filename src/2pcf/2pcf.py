#!/usr/bin/env python
import numpy as np
def rr_analytic(bin_low_bound, bin_high_bound, box_size):
    volume = 4 * np.pi * (bin_high_bound**3 - bin_low_bound**3) / 3
    normed_volume = volume / box_size **3
    return normed_volume
def tpcf(dd, box_size=2500):
    """ Compute the analytic two-point correlation function from the DD pair-counts.

    dd (ndarray): left_bin_edge, right_bin_edge, mono_pair_count, mono_normed_pair_count\
                  quad_pair_count, quad_normed_pair_count, hexa_pair_count, hexa_normed_pair_count.
    box_size (float, optional): Size of the side of the box to consider, in Mpc.
		Default: box_size = 2500"""
    
    rr = rr_analytic(dd[:,0], dd[:,1], box_size)
    delta_s = dd[:,1] - dd[:,0]
    s = dd[:,0] + 0.5 * delta_s
    monopole = ( dd[:,3] / rr ) - 1
    quadrupole =  dd[:,5] / rr 
    hexadecapole = dd[:,7] / rr * 2 
    out = np.c_[s, monopole, quadrupole, hexadecapole].astype(np.float32)
    return out


if __name__ == '__main__':
    
    import sys
    import os
    
    if len(sys.argv) < 2:
        sys.exit(f"ERROR: Unexpected number of arguments.\nUSAGE: {sys.argv[0]} DD_COUNT OUT_2PCF")
    dd_file = np.loadtxt(sys.argv[1])
    np.savetxt(sys.argv[2], tpcf(dd_file))
    print(f"==> Saved correlation function in {sys.argv[2]}.")
