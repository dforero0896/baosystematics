#!/usr/bin/env python3
import numpy as np
from astropy.table import Table, vstack
from astropy.io import fits
import os
import sys
import pandas as pd

if len(sys.argv) != 6:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH N_SLICES THIS_SLICE OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
n_slices = int(sys.argv[3])
this_slice = int(sys.argv[4])
overwrite = bool(int(sys.argv[5]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)

f1 = np.array_split(np.array(f), n_slices)
tables = []
if not os.path.isdir(outPath):
	os.mkdir(outPath)
if not os.path.isdir(os.path.join(inPath, '../dicts')):
	os.mkdir(os.path.join(inPath, '../dicts'))
dictionary = open(os.path.join(inPath,'../dicts/dictionary%i.dat'%this_slice), 'w')
for k, filename in enumerate(f1[this_slice]):
    key = 'k'+str(k)+'p'+str(this_slice)
    dictionary.write(filename+'\t'+str(key)+'\n')
    ascii_df = pd.read_csv(os.path.join(inPath,filename), sep = ' ', header = None, names = ['RAD', 'DEC', 'Z', 'R'])
    ascii_df['KEY'] = [key]*len(ascii_df['R'])
    tables.append(ascii_df)
    sys.stdout.write( '%i/%i Done\r'%(k, len(f)))
    sys.stdout.flush()
t_all = Table.from_pandas(pd.concat(tables, ignore_index=True))
t_all.write(os.path.join(outPath,'superCatalog%i.fits'%this_slice), format = 'fits', overwrite=True)
dictionary.close()

