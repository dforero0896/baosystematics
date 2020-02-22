#!/usr/bin/env python
import numpy as np
import sys
import os
#import matplotlib.pyplot as plt
if len(sys.argv)!=2:
	sys.exit('ERROR: Unexpecte number of arguments.\nUSAGE: %s INPUT_DIR\n'%sys.argv[0])
idir = sys.argv[1]
try:
	(_,_,ilist) = next(os.walk(idir))
except StopIteration:
	sys.exit('ERROR: Empty input directory %s\n'%idir)
s_bao = 102.5
s_dl_1 = 82.5
s_dl_2 = 87.5
s_dr_1 = 117.5
s_dr_2 = 122.5
s_vals = [s_bao, s_dl_1, s_dl_2, s_dr_1, s_dr_2]
signal_arr=[]
for ifile in ilist:
	ipath = os.path.join(idir, ifile)
	iarr = np.loadtxt(ipath)
	s = iarr[:,0]
	xi = iarr[:,1]
	s_vals_id = np.array([np.where(s==val)[0] for val in s_vals])
	xi_vals = xi[s_vals_id]
	signal_arr.append(xi_vals[0] - np.mean(xi_vals[1:]))
SNR = np.mean(signal_arr)/np.std(signal_arr)
print('SNR=%.5f'%SNR)
