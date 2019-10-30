#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys 
comb = sys.argv[1]
mocks100 = pd.read_csv(comb, delim_whitespace=True, dtype=float, header = None)
print 'The file was loaded'
#print mocks100[3].min(), mocks100[3].max()
Z_bins = np.linspace(0.6, 1.1, 6)
z_binned = []
R_bins = range(1, 21)
R_bins.append(25)
R_bins.append(30)
R_bins.append(50)
#R_bins = [14, 15, 16, 17, 18, 19, 20, 25, 30, 50]
#R_bins = np.linspace(0, 50, 50)
#R_bins[-1] = 9999
for i in range(len(Z_bins)-1):
	bin_ = mocks100[(mocks100[2]>=Z_bins[i]) & (mocks100[2]<Z_bins[i+1])]
	r_binned = []
	for k in range(len(R_bins)-1):
		this_slice = bin_[(bin_[3]>=R_bins[k]) & (bin_[3]<R_bins[k+1])]
		this_slice[[2,3]].to_csv('./binned_catalogs_R/slice_Z%i_R%i.ascii'%(i,k), sep='\t', header = False, index=False)		
		this_slice[[0,1]].to_csv('./binned_catalogs_L/slice_Z%i_R%i.ascii'%(i,k), sep='\t', header = False, index=False)
		sys.stdout.write('Done with bin %i/%i %i/%i\r'%(i+1,len(Z_bins)-1 ,k+1, len(R_bins)-1))
	        sys.stdout.flush()
		r_binned.append(this_slice)

	z_binned.append(r_binned)




print 'ok'

