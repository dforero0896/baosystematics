#!/usr/bin/env python3
from astropy.io import ascii, fits
from astropy.table import Table
from os import walk
import numpy as np
import pandas as pd
import os
import sys

if len(sys.argv) != 4:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_FILE OUT_DIR OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
inPath = sys.argv[1]
outPath = sys.argv[2]
overwrite = bool(int(sys.argv[3]))
if not os.path.isfile(inPath):
	sys.stderr.write('ERROR:\tInput file not found')
	sys.exit(1)
if not os.path.isdir(outPath):
	sys.stderr.write('ERROR:\tOutput directory not found')
	sys.exit(1)
zone_pairs = {'22':'21', '21':'22', '23':'25', '25':'23'}
number_to_region = {'21':'SGC', '22':'SGC', '23':'NGC', '25':'NGC'}
this_zone = [key for key in list(zone_pairs.values()) if 'eboss'+key in inPath][0]
inPairFile = inPath.replace('eboss'+this_zone, 'eboss'+zone_pairs[this_zone])
outName = os.path.join(outPath,os.path.basename(inPath).replace('eboss'+this_zone,'eboss'+number_to_region[this_zone]).replace('fits', 'ascii'))
if not os.path.isfile(outName) or overwrite:
	t1 = Table.read(inPath, format='fits', hdu=1)
	t2 = Table.read(inPairFile, format='fits', hdu=1)
	t1['WEIGHT_COMP'] = t1['WEIGHT_SYSTOT'] * t1['WEIGHT_CP'] * t1['WEIGHT_NOZ']
	t1['WEIGHT_ALL'] = t1['WEIGHT_COMP'] * t1['WEIGHT_FKP']
	t2['WEIGHT_COMP'] = t2['WEIGHT_SYSTOT'] * t2['WEIGHT_CP'] * t2['WEIGHT_NOZ']
	t2['WEIGHT_ALL'] = t2['WEIGHT_COMP'] * t2['WEIGHT_FKP']
	d1 = t1['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	d2 = t2['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].to_pandas()
	dout = pd.concat([d1, d2])
	dout=dout[dout['WEIGHT_ALL']!=0]
	dout.to_csv(outName, sep='\t', header = False, index=False)
sys.stdout.write(outName)
