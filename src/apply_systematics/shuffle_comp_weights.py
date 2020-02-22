#!/usr/bin/env python
import numpy as np
import os
import sys
if len(sys.argv) !=2:
    sys.exit('ERROR: Unexpected number of arguments\nUSAGE: %s INFILE OUTFILE\n'%sys.argv[0])

infile = sys.argv[1]
outfile = sys.argv[2]
indata = np.genfromtxt(infile, names = ['RA', 'DEC', 'Z', 'WEIGHT_ALL', 'WEIGHT_COMP', 'WEIGHT_FKP', 'NZ'], comments='#', dtype=np.float32)
old_w_comp = indata['WEIGHT_COMP']
old_eff_number_tracers = indata['WEIGHT_ALL'].sum()
new_w_comp = np.random.permutation(old_w_comp)
new_w_all = indata['WEIGHT_FKP'] * new_w_comp
new_eff_number_tracers = new_w_all.sum()
indata['WEIGHT_COMP'] = old_eff_number_tracers * new_w_comp / new_eff_number_tracers
indata['WEIGHT_ALL'] = indata['WEIGHT_FKP'] * indata['WEIGHT_COMP']
np.savetxt(outfile, indata, header = 'RA DEC Z WEIGHT_ALL WEIGHT_COMP WEIGHT_FKP NZ', fmt=('%.6f','%.6f', '%.6f', '%.6f', '%.6f', '%.6f', '%.6e'))
