#!/usr/bin/env python
import numpy as np
from astropy.table import Table, vstack
from astropy.io import fits
import sys
import pandas as pd
import os
if len(sys.argv) != 4:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
overwrite = bool(int(sys.argv[3]))
cat_masked_name = 'COMPMASKED' # or MASKED if only vetomask masks applied
filename=os.path.basename(inPath)
outFile = os.path.join(outPath, filename.replace(cat_masked_name, 'MASKED'))
if not os.path.isdir(outPath):
	os.mkdir(outPath)
if os.path.isfile(outFile) and not overwrite:
	sys.stdout.write('File already exists. Set OVERWRITE=1 if necessary.\n')
	sys.exit(0)
ascii_df = pd.read_csv(inPath, delim_whitespace=True, header=None)
print('Imported file %s'%filename)
ascii_df = ascii_df[ascii_df.iloc[:,-1]==1]	
ascii_df[[0,1,2,3]].to_csv(outFile, sep='\t', header = False, index=False)
print('Saved file %s'%outFile)


