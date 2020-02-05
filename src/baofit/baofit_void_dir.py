#!/usr/bin/env python3
import os
import sys
import tempfile
import numpy as np
import stats_center
from mpi4py import MPI
nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
inode = MPI.Get_processor_name()    # Node where this MPI process runs

if len(sys.argv)!=5:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} INPUT_DIR OUT_DIR CAT_TYPE CAP'.format(sys.argv[0]))
input2PCF = sys.argv[1]
outPath = sys.argv[2]
cat_type = sys.argv[3]
cap = sys.argv[4]
WORKDIR='/hpcstorage/dforero/projects/baosystematics/'
try:
	(_, _, in2pcfall) = next(os.walk(input2PCF))
	in2pcf = [f for f in in2pcfall if cap.lower() in f.lower()]
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  
if not os.path.isdir(outPath):
	os.mkdir(outPath)
mockFile = tempfile.NamedTemporaryFile(mode='w+t')
mockFile_name = mockFile.name
r = os.path.join(outPath, 'cov.dat')
if cat_type=='void':
	run = os.path.join(WORKDIR,'src/baofit/BAOfit_void_new/baofit.py')
elif cat_type=='gal':
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
else:
	sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
for m in in2pcf:
	mockFile.writelines(os.path.join(input2PCF, m+'\n'))
print(mockFile.read())
files = np.array_split(in2pcf, nproc)
for idx, tpcf in enumerate(files[iproc]):
	tpcf_fn = os.path.join(input2PCF, tpcf)
	print(tpcf_fn)
	tpcf_base, ext = os.path.splitext(tpcf)
	if idx==0 and not os.path.isfile(r):
		compute_cov = 1
	else:
		compute_cov = 0 
	i = tpcf_fn
	m = mockFile_name
	o = os.path.join(outPath, 'BAOfit_'+tpcf)
	b = o+'bestfit.txt' 
	# Check if the output of stats_center exists.
	if not os.path.isfile(b.replace('bestfit', 'mystats')):
		os.system('%s %s %s %s %s %s'%(run, i, m, outPath, r, compute_cov))
		stats_center.stats_center(o, cat_type='gal', plot=False)
mockFile.close()
MPI.Finalize()
