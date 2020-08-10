#!/usr/bin/env python3
import os
import sys
import tempfile
import numpy as np
import stats_center
import re
from tqdm import tqdm
from dotenv import load_dotenv
WORKDIR=os.environ.get('WORKDIR')
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('INPUT_DIR', help='Directory containing the input 2pcfs')
parser.add_argument('OUT_DIR', help ='Diretory to save results')
parser.add_argument('CAT_TYPE', help='Must be "void".')
parser.add_argument('CAP', help='Cap to look for. ngc, sgc or none.')
parser.add_argument('-ow', '--overwrite', required=False,help='Whether to overwrite the existing fits. Default: 1')
parser.add_argument('-vt', '--void-temp', required=False, help='Void template to use in the fit. Defaault reads template from params.py file.')
parsed = parser.parse_args()
args=vars(parsed)
#print(args)

def trim_letters(name):
    name = name.replace('TwoPCF_','')
    new = re.sub('sigma.*R','R', name)
    return new

input2PCF = args['INPUT_DIR']
outPath = args['OUT_DIR']
cat_type = args['CAT_TYPE']
cap = args['CAP']
overwrite=False if args['overwrite'] is None else bool(int(args['overwrite']))
input_pvoid = os.path.realpath(args['void_temp']) or ""
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
	if not os.path.isfile(o+'.txt' ) or overwrite: #Check if chain file exists
		if overwrite and os.path.isfile(o+'resume.dat'): os.remove(o+"resume.dat")
		joblist.write(f"{run} {i} {m} {outPath} {r} {compute_cov} {o} --void-temp {input_pvoid} && python {stats_run} {o} 3\n")
	elif not os.path.isfile(b): #Check if mystats file has been created
		stats_center.stats_center(o, nparams=3, plot=True)
joblist.close()
mockFile.close()
