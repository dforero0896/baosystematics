#!/usr/bin/env python3
import os
import sys
import tempfile
import numpy as np
import stats_center
if len(sys.argv)!=5:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} MOCK_DIR INPUT_2PCF OUT_PATH CAT_TYPE'.format(sys.argv[0]))

mockPath = sys.argv[1]
input2PCF = sys.argv[2]
outPath = sys.argv[3]
cat_type = sys.argv[4]
WORKDIR='/hpcstorage/dforero/projects/baosystematics/'
try:
	(_, _, mockList) = next(os.walk(mockPath))
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
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_void/bestfit')
	stats_run = os.path.join(WORKDIR, 'src/baofit/stats_center.py')
elif cat_type=='gal':
	raise(ValueError("This code works with voids!"))
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_galaxy/bestfit')
else:
	sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
for m in mockList:
	mockFile.writelines(os.path.join(mockPath, m+'\n'))
print(mockFile.read())
tpcf_fn = input2PCF
tpcf = os.path.basename(tpcf_fn)
print(tpcf_fn)
tpcf_base, ext = os.path.splitext(tpcf)
if not os.path.isfile(r):
	compute_cov = 1
else:
	compute_cov = 0
i = tpcf_fn
m = mockFile_name
o = os.path.join(outPath, 'BAOfit_'+tpcf)
b = o+'mystats.txt' 
# Check if the output of stats_center exists.
if not os.path.isfile(o+'.txt' ): #Check if chain file exists
	os.system(f"{run} {i} {m} {outPath} {r} {compute_cov} {o} && python {stats_run} {o} 3\n")
elif not os.path.isfile(b): #Check if mystats file has been created
	stats_center.stats_center(o, nparams=3, plot=True)
mockFile.close()


