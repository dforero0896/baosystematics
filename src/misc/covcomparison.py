# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import os
from astropy.visualization import AsymmetricPercentileInterval, LogStretch, MinMaxInterval
DIR='/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/nosyst/'
files = [DIR+'tpcf_gal_mock/'+f for f in os.listdir(DIR+'tpcf_gal_mock/') if os.path.isfile(DIR+'tpcf_gal_mock/'+f)]
files_extra = [DIR+'tpcf_gal_mock_extra/'+f for f in os.listdir(DIR+'tpcf_gal_mock_extra/') if os.path.isfile(DIR+'tpcf_gal_mock_extra/'+f)]
s = np.loadtxt(files[0], usecols=0)
data = [s**2*np.loadtxt(f, usecols=1) for f in files]
data_extra = [s**2*np.loadtxt(f, usecols=1) for f in files_extra]
data_more = np.array(data)
data = data_more[:250]
print(data.shape, data_more.shape)
cov_data = np.corrcoef(data.T)
cov_data_more = np.corrcoef(data_more.T)
diff = 100 * (cov_data - cov_data_more) / cov_data 
from matplotlib.colors import LogNorm
fig, ax = plt.subplots(1, 3, figsize=(30,10))
ax[0].set_title('%s mocks'%(data.shape[0]));ax[1].set_title('%s mocks'%(data_more.shape[0]));ax[2].set_title(r'% error')
interval = AsymmetricPercentileInterval(50-20, 50+20, n_samples=40*40)
vmin, vmax = interval.get_limits(diff)
ax[0].imshow(cov_data); ax[1].imshow(cov_data_more);dax=ax[2].imshow(np.clip(diff, vmin, vmax))
plt.colorbar(dax)
plt.show()
