#!/usr/bin/env python
from astropy.io import ascii, fits
from astropy.table import Table
from os import walk
import numpy as np
import pandas as pd
import os
import sys

from mpi4py import MPI
nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
inode = MPI.Get_processor_name()    # Node where this MPI process runs
if len(sys.argv) != 4:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
inPath = sys.argv[1]
outPath = sys.argv[2]
overwrite = bool(int(sys.argv[3]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.')
	sys.exit(1)

SGC22 = sorted([name.replace('eboss22', 'ebossXX') for name in f if 'eboss22' in name])
NGC23 = sorted([name.replace('eboss23', 'ebossXX') for name in f if 'eboss23' in name])
SGC_list = np.array_split(np.array(SGC22), nproc)[iproc]
NGC_list = np.array_split(np.array(NGC23), nproc)[iproc]
for i,m in enumerate(SGC_list):
	outName = os.path.join(outPath,m.replace('ebossXX','ebossSGC').replace('fits', 'ascii'))
	if os.path.isfile(outName) and not overwrite:
		continue
	t1 = Table.read(os.path.join(inPath,m.replace('XX','21')), format='fits', hdu=1)
	t2 = Table.read(os.path.join(inPath,m.replace('XX','22')), format='fits', hdu=1)
	t1['WEIGHT_COMP'] = t1['WEIGHT_SYSTOT'] * t1['WEIGHT_CP'] * t1['WEIGHT_NOZ']
	t1['WEIGHT_ALL'] = t1['WEIGHT_COMP'] * t1['WEIGHT_FKP']
	t2['WEIGHT_COMP'] = t2['WEIGHT_SYSTOT'] * t2['WEIGHT_CP'] * t2['WEIGHT_NOZ']
	t2['WEIGHT_ALL'] = t2['WEIGHT_COMP'] * t2['WEIGHT_FKP']
	d1 = t1['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	d2 = t2['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	dout = pd.concat([d1, d2])
	dout=dout[dout['WEIGHT_ALL']!=0]
	dout.to_csv(outName, sep='\t', header = False, index=False)
	sys.stdout.write("Process %i Done %i/%i\r"%(iproc,i+1,len(SGC_list)))
	sys.stdout.flush()


for i,m in enumerate(NGC_list):
	outName = os.path.join(outPath,m.replace('ebossXX','ebossNGC').replace('fits', 'ascii'))
	if os.path.isfile(outName) and not overwrite:
		continue
	t1 = Table.read(os.path.join(inPath,m.replace('XX','23')), format='fits', hdu=1)
	t2 = Table.read(os.path.join(inPath,m.replace('XX','25')), format='fits', hdu=1)
	t1['WEIGHT_COMP'] = t1['WEIGHT_SYSTOT'] * t1['WEIGHT_CP'] * t1['WEIGHT_NOZ']
	t1['WEIGHT_ALL'] = t1['WEIGHT_COMP'] * t1['WEIGHT_FKP']
	t2['WEIGHT_COMP'] = t2['WEIGHT_SYSTOT'] * t2['WEIGHT_CP'] * t2['WEIGHT_NOZ']
	t2['WEIGHT_ALL'] = t2['WEIGHT_COMP'] * t2['WEIGHT_FKP']
	d1 = t1['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	d2 = t2['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	dout = pd.concat([d1, d2])
	dout=dout[dout['WEIGHT_ALL']!=0]
	dout.to_csv(outName, sep='\t', header = False, index=False)
	sys.stdout.write("Process %i Done %i/%i\r"%(iproc, i+1,len(NGC_list)))
	sys.stdout.flush()
	
MPI.Finalize()
