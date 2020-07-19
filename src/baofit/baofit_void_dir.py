#!/usr/bin/env python3
import os
import sys
import tempfile
import numpy as np
import stats_center
import re
from tqdm import tqdm

def trim_letters(name):
    name = name.replace('TwoPCF_','')
    new = re.sub('sigma.*R','R', name)
    return new

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
	if len(in2pcf)<1:
		in2pcf=in2pcfall
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  
if not os.path.isdir(outPath):
	os.mkdir(outPath)
#mockFile = tempfile.NamedTemporaryFile(mode='w+t')
#mockFile_name = mockFile.name
mockFile_name = 'mockfile.dat'
mockFile=open(mockFile_name, 'w')
r = os.path.join(outPath, 'cov.dat')
if cat_type=='void':
	run = os.path.join(WORKDIR,'src/baofit/BAOfit_void_new/baofit.py')
elif cat_type=='gal':
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
	sys.exit("The name says this file is for voids!\n")
else:
	sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void\n')
stats_run = os.path.join(WORKDIR, 'src/baofit/stats_center.py')
for m in in2pcf:
	mockFile.writelines(os.path.join(input2PCF, m+'\n'))

joblist = open('void_dir_joblist.sh', 'w')
for idx, tpcf in tqdm(enumerate(in2pcf)):
	tpcf_fn = os.path.join(input2PCF, tpcf)
	tpcf_base, ext = os.path.splitext(tpcf)
	if idx==0 and not os.path.isfile(r):
		compute_cov = 1
	else:
		compute_cov = 0 
	i = tpcf_fn
	m = mockFile_name
	o = os.path.join(outPath, "BAOfit_"+trim_letters(tpcf))
	b = o+'mystats.txt' 
	# Check if the output of stats_center exists.
	if not os.path.isfile(o+'.txt' ): #Check if chain file exists
		joblist.write(f"{run} {i} {m} {outPath} {r} {compute_cov} {o} && python {stats_run} {o} 3\n")
	elif not os.path.isfile(b): #Check if mystats file has been created
		stats_center.stats_center(o, nparams=3, plot=True)
joblist.close()
mockFile.close()
