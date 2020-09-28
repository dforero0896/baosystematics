#!/usr/bin/env python
import pandas as pd
import sys
import os

infile = sys.argv[1]

names = pd.read_csv(infile, engine='c', usecols=[0], names=['tpcf'])
ofile = open("missing_void_2pcf.dat", "w")
for n in names.values:
  tpcf_fn = n[0].split(" ")[12].replace("--output=", "")
  if not os.path.isfile(tpcf_fn):
    ofile.write(f"{n[0].replace('-c 16', '-c 32').replace('/home/epfl/', '/home/astro/')}\n")
ofile.close()
