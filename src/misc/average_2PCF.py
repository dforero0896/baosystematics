#!/usr/bin/env python
import numpy as np
import pandas as pd
import sys
import os
def read_input(path):
	try:
		(_, _, l) = next(os.walk(path))
		return l
	except StopIteration:
		sys.stdout.write('ERROR: Empty input directory.')
		sys.exit(1)
if len(sys.argv)== 4:
	path = sys.argv[1]
	name = sys.argv[3]
	l = read_input(path)
	gen = (np.loadtxt(os.path.join(path,f), dtype=float) for f in l)
	outname = name
elif len(sys.argv)==6:
	path = sys.argv[1]
	cat_type = sys.argv[3]
	reg = sys.argv[4].lower()
	joblist_id = sys.argv[5]
	l = read_input(path)
	gen = (np.loadtxt(os.path.join(path,f), dtype=float) for f in l if reg in f.lower())
	outname = '%s_%s_%s'%(joblist_id, cat_type, reg)
else:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUsage {0} IN_PATH OUT_PATH NAME\nor\nUsage {0} IN_PATH OUT_PATH CAT_TYPE ZONE ID\n'.format(sys.argv[0]))
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
out = sys.argv[2]
if not os.path.isdir(out):
	os.makedirs(out)
data = np.array(list(gen))
if len(data) == 0:
	sys.exit('ERROR: No files found.')
mocks_mean = data.mean(axis=0)
mocks_std = data.std(axis=0)
mean_data_0, mean_data_1 = mocks_mean[:,1], mocks_mean[:,2]
std_data_0, std_data_1 = mocks_std[:,1], mocks_std[:,2]
xdata = data[0, :, 0]
if mocks_mean.shape[1]>3:
	mean_data_2 = mocks_mean[:,3]
	std_data_2 = mocks_std[:,3]
else:
	mean_data_2 = np.zeros_like(mean_data_1)
	std_data_2 = np.zeros_like(std_data_1)
out_dict = dict(zip([0,1,2,3,4, 5, 6],[xdata, mean_data_0, std_data_0, mean_data_1, std_data_1, mean_data_2, std_data_2]))

all_mocks = pd.DataFrame.from_dict(out_dict)
all_mocks.to_csv(os.path.join(out,'TwoPCF_mockavg_%s.ascii'%outname), sep='\t', index=False, header = False)
