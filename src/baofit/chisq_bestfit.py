#!/usr/bin/env python
import numpy as np
from scipy import interpolate
from python_dewiggle.params import *
def cov_mat(mock_list):
	mock_matrix = np.array([np.loadtxt(mock, usecols=1) for mock in mock_list])
	mock_mean = np.mean(mock_matrix, axis=0)
	mock_matrix -= mock_mean[None,:]
	n_mocks , n_bins = mock_matrix.shape
	cov_sample = mock_matrix.T.dot(mock_matrix)
	cov_unbiased = cov_sample / (n_mocks - n_bins - 2) 
	return cov_unbiased, mock_mean
def chisq(data, prediction, cov):
	error = data - prediction
	inv_cov = np.linalg.inv(cov)
	n_points = len(data)
	chisq = error.dot(inv_cov.dot(error))
	return chisq, n_points
def dof_dict(n_points, cat_type='void'):
	n_param_dict = {'void':7, 'gal':6}
	return n_points - n_param_dict[cat_type]
def dof(n_points, n_params):
	return n_points - n_params
def main():
	import sys
	import os
	if len(sys.argv) < 4:
		sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: %s MOCK_DIR BESTFIT_2PCF_1 [ ... BESTFIT_2PCF_N] N_FIT_PARAMS'%sys.argv[0])
	try:
		n_params = int(sys.argv[-1])
	except:
		raise ValueError("ERROR: Last argument must be integer number of fit parameters.")
	mock_dir = sys.argv[1]
	bestfit_filenames = sys.argv[2:-1]
	_,_,mock_files = next(os.walk(mock_dir))
	n_mocks = len(mock_files)
	tpcf_cov, tpcf_data = cov_mat([os.path.join(mock_dir, f) for f in mock_files]) 
	for bestfit_filename in bestfit_filenames:
		bestfit_data = np.loadtxt(bestfit_filename)
		s_bins = np.loadtxt(os.path.join(mock_dir,mock_files[0]), usecols=0)
		fit_range_mask = (s_bins >= fit_smin) & (s_bins <= fit_smax)
		tpcf_mean = tpcf_data[fit_range_mask]
		tpcf_bestfit_spline = interpolate.interp1d(bestfit_data[:,0], bestfit_data[:,-1], kind='cubic')
		tpcf_bestfit = tpcf_bestfit_spline(s_bins[fit_range_mask])
		chsq, n_points = chisq(tpcf_mean, tpcf_bestfit, tpcf_cov[fit_range_mask,:][:,fit_range_mask])
		dof_  = dof(n_points, n_params)
		#print(dof_)
	#	n_mocks = 1 #Overwrite number of mocks when dealing with the fit to a single realization
		red_chsq = n_mocks*chsq/dof_
		print('Reduced chisq for %s: %i * %.3f / %i = %.5f'%(os.path.basename(bestfit_filename),n_mocks, chsq, dof_, red_chsq))
		print(red_chsq)
if __name__=='__main__':
	main()
