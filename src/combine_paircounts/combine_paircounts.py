#!/usr/bin/env python3
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
if len(sys.argv) == 3:
	path = sys.argv[1]
	outpath = sys.argv[2]
else:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUsage {0} IN_PATH OUT_PATH\n'.format(sys.argv[0]))
	sys.exit(1)
savefiles = 1
regions = ['NGC', 'SGC']
try:
	(_, _, filenames_RR) = next(os.walk(os.path.join(path,'RR_files')))
	(_, _, filenames_DD) = next(os.walk(os.path.join(path,'DD_files')))
except:
	sys.stdout.write('ERROR: Empty input RR or DD directory.\n')
	sys.exit(1)
RRfn = [f for f in filenames_RR if 'NGC' in f]
DDfn = [f for f in filenames_DD if 'NGC' in f]
#No DR because using replace on DD files 

rr = [None]*2
dd = [None]*2
dr = [None]*2	
qrr = [None]*2
qdd = [None]*2
qdr = [None]*2
nd = [None]*2

for i, r in enumerate(regions):
	d = np.loadtxt(os.path.join(path,'RR_files',RRfn[0].replace('NGC', r)), unpack=True)
	rr[i] = d[3] #normalised counts
	qrr[i] = d[5]

x = (d[0] + d[1]) * 0.5 #bin center
smin, smax = d[0], d[1]

for f in DDfn:
	for i, r in enumerate(regions):
		fn = f.replace('NGC', r)
		ddfn = os.path.join(path,'DD_files',fn)
		drfn = os.path.join(path,'DR_files',fn.replace('DD', 'DR'))
		# Import DD file. Cols: count, norm_count, quad_norm_count
		d = np.loadtxt(ddfn, unpack=True, usecols=(2,3,5))
		nd[i] = np.mean(np.sqrt(d[0]/d[1]), axis=0)
		dd[i] = d[1]
		qdd[i] = d[2]
		# Import DR file. Cols: norm_count, quad_norm_count
		d = np.loadtxt(drfn, unpack=True, usecols=(3,5))
		dr[i] = d[0]
		qdr[i] = d[1]
		#Import RR file if dealing with mocks.
		if 'EZ' in f and 'VOID' not in f:
			rrfn = os.path.join(path,'RR_files',fn.replace('DD', 'RR'))
			d = np.loadtxt(rrfn, unpack=True, usecols=(3,5))
			rr[i] = d[0]
			qrr[i] = d[1]
	nfac = nd[1] / nd[0] #nt1/nt2
	ndd = (dd[0] + dd[1] * nfac**2) / (1 + nfac)**2
	ndr = (dr[0] + dr[1] * nfac**2) / (1 + nfac)**2
	nrr = (rr[0] + rr[1] * nfac**2) / (1 + nfac)**2
	countTotDD = dd[0]*nd[0]**2 + dd[1]*nd[1]**2
	countTotDR = dr[0]*nd[0]**2 + dr[1]*nd[1]**2
	countTotRR = rr[0]*nd[0]**2 + rr[1]*nd[1]**2

	nqdd = (qdd[0] + qdd[1] * nfac**2) / (1 + nfac)**2
	nqdr = (qdr[0] + qdr[1] * nfac**2) / (1 + nfac)**2
	nqrr = (qrr[0] + qrr[1] * nfac**2) / (1 + nfac)**2
	countTotQDD = qdd[0]*nd[0]**2 + qdd[1]*nd[1]**2
	countTotQDR = qdr[0]*nd[0]**2 + qdr[1]*nd[1]**2
	countTotQRR = qrr[0]*nd[0]**2 + qrr[1]*nd[1]**2
	# Compute 2PCF
	y = (ndd - 2*ndr + nrr) / nrr
	qy = (nqdd - 2*nqdr + nqrr) / nrr
	outfile = os.path.join(outpath, f.replace('DD', 'TwoPCF').replace('NGC', 'CBZ'))
	print(outfile)
	if savefiles:
		np.savetxt(os.path.join(outpath,'RR_files',f.replace('DD', 'RR').replace('NGC', 'CBZ')), np.transpose([smin, smax, countTotRR, nrr, countTotQRR, nqrr]),  fmt='%.8g')
		np.savetxt(os.path.join(outpath,'DR_files',f.replace('DD', 'DR').replace('NGC', 'CBZ')), np.transpose([smin, smax, countTotDR, ndr, countTotQDR, nqdr]),  fmt='%.8g')
		np.savetxt(os.path.join(outpath,'DD_files',f.replace('DD', 'DD').replace('NGC', 'CBZ')), np.transpose([smin, smax, countTotDD, ndd, countTotQDD, nqdd]),  fmt='%.8g')
	np.savetxt(outfile, np.transpose([x, y, qy]), fmt='%.8g')

  
  
  
  
  
  
  
  
  
  
