#!/usr/bin/env python3
import numpy as np
from astropy.table import Table, vstack
from astropy.io import fits
from os import walk
import sys
import pandas as pd
import os
if len(sys.argv) != 6:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH N_SLICES THIS_SLICE OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
n_slices = int(sys.argv[3])
this_slice = int(sys.argv[4])
overwrite = bool(int(sys.argv[5]))
mskcol = 'newbit' # or VETOMASK if only vetomask masks applied.
supercat_name = 'COMPMASKED' # or MASKED if only vetomask masks applied.
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.\n')
	sys.exit(1)
if not os.path.isdir(outPath):
	os.mkdir(outPath)
sys.stdout.write('Loading dictionary...\t\t\t\t')
dictionary = np.loadtxt(os.path.join(outPath,'../dicts/dictionary%i.dat'%this_slice), delimiter='\t', dtype=str)
sys.stdout.write('DONE\nLoading catalog...\t\t\t\t')
fits_df = Table.read(os.path.join(inPath,'superCatalog.%s%i.fits'%(supercat_name,this_slice)), format='fits').to_pandas()
fits_df['KEY'] = fits_df['KEY'].str.decode('utf-8')
sys.stdout.write('DONE\n')
fits_df = fits_df[fits_df[mskcol]==1]
for filename, key in dictionary:
	outFile = os.path.join(outPath,filename.replace('VOID', 'VOID.MASKED'))
	if os.path.isfile(outFile) and not overwrite:
		continue
	sys.stdout.write('Splitting %s\t\t\t\t'%filename)
	this_mock = fits_df[fits_df['KEY']==key]
	this_mock[['RA', 'DEC', 'Z', 'R']].to_csv(outFile, sep='\t', header = False, index=False)
	sys.stdout.write('DONE\n')
