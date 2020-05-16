#!/usr/bin/env python3
import os
import sys
import tempfile
import numpy as np
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/misc")
from plotfit import plotfit
import stats_center
if len(sys.argv)!=5:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} MOCK_DIR INPUT_2PCF OUT_PATH CAT_TYPE'.format(sys.argv[0]))

mockPath = sys.argv[1]
input2PCF = sys.argv[2]
outPath = sys.argv[3]
cat_type = sys.argv[4]
WORKDIR='/hpcstorage/dforero/projects/baosystematics/'
os.makedirs(outPath, exist_ok=True)
try:
	(_, _, mockList) = next(os.walk(mockPath))
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  
if not os.path.isdir(outPath):
	os.makedirs(outPath)
mockFile = tempfile.NamedTemporaryFile(mode='w+t')
mockFile_name = mockFile.name
r = os.path.join(outPath, 'cov.dat')
if cat_type=='void':
	run = os.path.join(WORKDIR,'bin/BAOfit_void/BAOfit')
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_void/bestfit')
elif cat_type=='gal':
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
	run_bestfit = os.path.join(WORKDIR,'bin/BAOfit_galaxy/bestfit')
else:
	sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
for m in mockList:
	f = os.path.join(mockPath, m+'\n')
	mockFile.writelines(f)
mockFile.seek(0)
#print(mockFile.read())
tpcf_fn = input2PCF

tpcf = os.path.basename(tpcf_fn)
tpcf_base, ext = os.path.splitext(tpcf)
if not os.path.isfile(r):
	c = os.path.join(WORKDIR,'src/baofit/baofit_covcomp.conf')
else:
	c = os.path.join(WORKDIR,'src/baofit/baofit.conf')
i = tpcf_fn
m = mockFile_name
o = os.path.join(outPath, tpcf_base+'_')
b = o+'bestfit.txt' 
# Check if the output of stats_center exists.
if not os.path.isfile(b.replace('bestfit', 'mystats')):
	os.system('%s -c %s -i %s -m %s -o %s -b %s -r %s'%(run, c, i, m, o, b, r))
	#os.system('python %s %s %s'%(os.path.join(WORKDIR, 'src/baofit/stats_center.py'), o, cat_type))
results = stats_center.stats_center(o, cat_type=cat_type, plot=True)
if not os.path.isfile(b):
	os.system('%s -c %s -i %s -m %s -o %s -b %s -r %s'%(run_bestfit, c, i, m, o, b, r))
	results = stats_center.stats_center(o, cat_type=cat_type, plot=True)
print(i, b)
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
f = plt.figure()
plotfit([i], b, outPath, r'$\chi^2$=%0.3f'%results[-3])

mockFile.close()


