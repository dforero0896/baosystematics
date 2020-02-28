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
	if cap != 'none':
		in2pcf = [f for f in in2pcfall if cap.lower() in f.lower()]
	else:
		in2pcf = in2pcfall
		cap='\b'
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  
if not os.path.isdir(outPath):
	os.makedirs(outPath)
mockFile = tempfile.NamedTemporaryFile(mode='w+t')
mockFile_name = mockFile.name
r = os.path.join(outPath, 'cov_%s.dat'%cap)
if cat_type=='void':
	run = os.path.join(WORKDIR,'bin/BAOfit_void/BAOfit')
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_void/bestfit')
elif cat_type=='gal':
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_galaxy/bestfit')
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
		c = os.path.join(WORKDIR,'src/baofit/baofit_covcomp.conf')
	else:
		c = os.path.join(WORKDIR,'src/baofit/baofit.conf')
	c_bestfit = os.path.join(WORKDIR,'src/baofit/baofit.conf')
	i = tpcf_fn
	m = mockFile_name
	o = os.path.join(outPath, tpcf_base+'_')
	b = o+'bestfit.txt' 
	# Check if the output of stats_center exists.
	if not os.path.isfile(b.replace('bestfit', 'mystats')):
		os.system('%s -c %s -i %s -m %s -o %s -b %s -r %s'%(run, c, i, m, o, b, r))
		stats_center.stats_center(o, cat_type, plot=False)
	if not os.path.isfile(b):
		os.system('%s -c %s -i %s -m %s -o %s -b %s -r %s'%(run_bestfit, c_bestfit, i, m, o, b, r))
mockFile.close()
MPI.Finalize()
