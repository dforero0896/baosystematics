#!/usr/bin/env python
import numpy as np
from scipy import stats
import sys
import os
from getdist import plots, MCSamples
import re
if len(sys.argv) != 2:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t%s BAOFIT_PATH\n'%sys.argv[0])
path = sys.argv[1]
files_all = os.listdir(path)
files = [f for f in files_all if 'mystats' in f]
def get_file_id(filename, delimiters = '_|\.'):
	try:
		id_ = [int(s) for s in re.split(delimiters, filename) if s.isdigit()][0]
	except IndexError as ie:
		id_=0
	return id_
def save_hist(cap = None):
	results = []
	if not cap:
		files_cap = [f for f in files]
	else:
		files_cap = [f for f in files if cap.upper() in f]
	files_ids = [get_file_id(f) for f in files_cap]
	sorted_files_cap = [f for _, f in sorted(zip(files_ids, files_cap))]
	for f in sorted_files_cap:
		results.append(np.loadtxt(os.path.join(path, f)))
	results = np.array(results)
	np.savetxt(os.path.join(path, 'alpha_samples_%s.dat'%cap), results)
#	kde = stats.gaussian_kde(dataset=results[:,0])
	samples = MCSamples(samples=results[:,0], names=['alpha'], labels=[r'\alpha'])
	kde = samples.get1DDensity('alpha')
	alpha_hist, bin_edges = np.histogram(results[:,0], density=True, bins=100) 
	bin_centers = bin_edges + 0.5 * (bin_edges[1]-bin_edges[0])
	bin_centers=bin_centers[:-1]
	hist_results = np.array([bin_centers, alpha_hist, kde.Prob(bin_centers)]).T
	header = '%i files taken into account in cap %s\nalpha p_of_alpha\nalpha_mean = %.5f\nalpha_std = %.5f\nalpha_meanstd = %.5f'%(len(files_cap), cap, np.mean(results[:,0]), np.std(results[:,0]), np.mean(results[:,1]))
	np.savetxt(os.path.join(path, 'alpha_hist_%s.dat'%cap), hist_results, header = header)
if __name__=='__main__':
	fail=0
	try:
		save_hist('ngc')
		print('Found NGC results in %s'%path)
	except IndexError as ie:
		fail+=1
		print('No NGC results in %s'%path)
	try:
		save_hist('sgc')
		print('Found SGC results in %s'%path)
	except IndexError as ie:
		fail+=1
		print('No SGC results in %s'%path)
	try:
		save_hist('cbz')
		print('Found CBZ (combined) results in %s'%path)
	except IndexError as ie:
		fail+=1
		print('No CBZ (combined) results in %s'%path)
	if fail==3:
		print('Using all existing files in %s'%path)
		save_hist(None)
		
