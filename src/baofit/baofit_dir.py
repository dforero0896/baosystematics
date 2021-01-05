#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import numpy as np
import stats_center
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
from tqdm import tqdm
from mpi4py import MPI
from dotenv import load_dotenv
load_dotenv()
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/misc")
from plotfit import plotfit
comm = MPI.COMM_WORLD
nproc = comm.Get_size()   # Size of communicator
iproc = comm.Get_rank()   # Ranks in communicator
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
		cap=''
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  

os.makedirs(outPath, exist_ok=True)
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
mockFile.seek(0)
def run_fit(idx, tpcf):
	tpcf_fn = os.path.join(input2PCF, tpcf)
	tpcf_base, ext = os.path.splitext(tpcf)
	if idx==0 and not os.path.isfile(r):
		c = os.path.join(WORKDIR,'src/baofit/baofit_covcomp.conf')
	else:
		c = os.path.join(WORKDIR,'src/baofit/baofit.conf')
	c_bestfit = os.path.join(WORKDIR,'src/baofit/baofit.conf')
	#if os.path.isfile(tpcf_fn):
	#	if os.path.getmtime(tpcf_fn) < 1609848144:
	#	    print("==> tpcf has not been recomputed", flush=True)
	#	    return
	#	else:
	#	    os.remove(os.path.join(outPath, tpcf_base+'_')+"resume.dat")
	#	    os.remove(os.path.join(outPath, tpcf_base+'_')+"mystats.txt")

	i = tpcf_fn
	m = mockFile_name
	o = os.path.join(outPath, tpcf_base+'_')
	b = o+'bestfit.txt' 
	# Check if the output of stats_center exists.
	print(idx,'ok')
	if not os.path.isfile(b.replace('bestfit', 'mystats')):
		fit_exit = subprocess.call([run, '-c', c, '-i', i, '-m', m, '-o', o, '-b', b, '-r', r])
		if fit_exit==0: results = stats_center.stats_center(o, cat_type=cat_type, plot=True)
		else: raise Exception("Fit failed")
	if not os.path.isfile(b):
		bestfit_exit = subprocess.call([run_bestfit, '-c', c_bestfit, '-i', i, '-m', m, '-o', o, '-b', b, '-r', r])
	results = stats_center.stats_center(o, cat_type=cat_type, plot=False)
	f = plt.figure()
#	plotfit([i], b, outPath, r'$\chi^2$=%0.3f'%results[-2])
print(in2pcf[0])
if iproc==0: run_fit(idx=0, tpcf=in2pcf[0])
comm.barrier()
files = np.array_split(in2pcf[1:], nproc)
for tpcf in tqdm(files[iproc]):
	run_fit(999, tpcf) #Avoid recomputing covmat
mockFile.close()
MPI.Finalize()
