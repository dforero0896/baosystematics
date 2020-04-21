#!/usr/bin/env python
import numpy as np
import sys
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv
SRC = os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
#from params import *

if len(sys.argv) != 4:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
overwrite = bool(int(sys.argv[3]))
zbin_bounds = np.linspace(0, 2500, 2500//10 + 1) 
rbin_bounds = np.append(np.linspace(0, 21, 22), [25, 30, 50])
names = ['x', 'y', 'z', 'r', 'scaled_r']
raw_df = pd.read_csv(inPath, delim_whitespace=True, header=None, names = names)
print(f"==> Read {inPath}")
zbinned_df = [raw_df[(raw_df['z'] >= zbin_bounds[i]) & (raw_df['z'] < zbin_bounds[i+1])] for i in range(len(zbin_bounds)-1)]
zbinned_all = []
for df in zbinned_df:
	rzbinned_all =[]
	for i in range(len(rbin_bounds)-1):
		rzbinned_df = df[(df['r']>=rbin_bounds[i]) & (df['r']<rbin_bounds[i+1])]
		if rzbinned_df.empty:
			continue
		rzbinned_radec = rzbinned_df[names[:2]].copy()
		rzbinned_zr = rzbinned_df[names[2:]].copy()
		rzbinned_radec = rzbinned_radec.sample(frac=1).reset_index(drop=True)
		rzbinned_zr = rzbinned_zr.sample(frac=1).reset_index(drop=True)
		rzbinned_all.append(pd.concat([rzbinned_radec, rzbinned_zr], axis = 1, ignore_index=True,names = names))
	zbinned_all.append(pd.concat(rzbinned_all, axis = 0, ignore_index=True, names = names))
out_df = pd.concat(zbinned_all, axis=0, ignore_index=True)
print("Saving output.")
out_df.to_csv(outPath, sep=' ', header = False, index=False)
