#!/usr/bin/env python
import numpy as np
from astropy.table import Table, vstack
from astropy.io import fits
import sys
import pandas as pd
import os
from mpi4py import MPI
nproc = MPI.COMM_WORLD.Get_size()  
iproc = MPI.COMM_WORLD.Get_rank()  
inode = MPI.Get_processor_name()   
if len(sys.argv) != 4:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
overwrite = bool(int(sys.argv[3]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.\n')
	sys.exit(1)
fs = np.array_split(f, nproc)[iproc]
for i, filename in enumerate(fs):
	outFile = os.path.join(outPath, filename)
	if os.path.isfile(outFile) and not overwrite:
		continue
	ascii_df = pd.read_csv(os.path.join(inPath,filename), delim_whitespace=True, header=None)
	print('Imported file %s'%filename)
	ascii_df = ascii_df[ascii_df[4]==1]	
	ascii_df[[0,1,2,3]].to_csv(outFile, sep='\t', header = False, index=False)
	print('Saved file %s'%outFile)
	print( 'Process %i Done %i/%i'%(iproc, i+1, len(fs)))
	
MPI.Finalize()

