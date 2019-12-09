#!/usr/bin/env python
import numpy as np
import sys
import os
if len(sys.argv) != 2:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t%s BAOFIT_PATH\n'%sys.argv[0])
path = sys.argv[1]
files_all = os.listdir(path)
files = [f for f in files_all if 'mystats' in f]
def save_hist(cap = 'ngc'):
	results = []
	files_cap = [f for f in files if cap.upper() in f]
	for f in files_cap:
		results.append(np.loadtxt(os.path.join(path, f)))
	results = np.array(results)
	alpha_hist, bin_edges = np.histogram(results[:,0], density=True, bins=100) 
	bin_centers = bin_edges + 0.5 * (bin_edges[1]-bin_edges[0])
	bin_centers=bin_centers[:-1]
	hist_results = np.array([bin_centers, alpha_hist]).T
	header = '%i files taken into account in cap %s\nalpha p_of_alpha\nalpha_mean = %.5f\nalpha_std = %.5f\nalpha_meanstd = %.5f'%(len(files_cap), cap, np.mean(results[:,0]), np.std(results[:,0])/np.sqrt(len(files_cap)), np.mean(results[:,1]))
	np.savetxt(os.path.join(path, 'alpha_hist_%s.dat'%cap), hist_results, header = header)
save_hist('ngc')
save_hist('sgc')
