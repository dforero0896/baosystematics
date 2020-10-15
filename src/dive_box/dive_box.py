#!/usr/bin/env python
import sys
import os
import numpy as np
WORKDIR="/global/homes/d/dforero/projects/baosystematics"
if len(sys.argv) != 4:
    sys.exit('ERROR: Unexpected number of arguments.\nUSAGE: {} INDIR OUTDIR BOX_SIZE'.format(sys.argv[0]))
# Parameters
box_size = sys.argv[3]
# Paths
RUN = os.path.join(WORKDIR, 'bin/DIVE_box/DIVE_box')
OUTDIR = os.path.abspath(sys.argv[2])
INDIR = os.path.abspath(sys.argv[1])
JOBLIST='joblist.sh'
os.makedirs(OUTDIR, exist_ok=True)
input_catalogs = os.listdir(INDIR)
joblist=open(JOBLIST, 'w')
for i in input_catalogs:
    input_catalog = os.path.join(INDIR, i)
    in_name, in_ext = os.path.splitext(i)
    if "ran" in in_name: continue
    output_catalog = os.path.join(OUTDIR, in_name+'.VOID'+in_ext)
    temp_output_catalog = output_catalog+".TMP"
    if os.path.isfile(output_catalog):
        continue
    command = 'srun -n1 -c1 --mem-per-cpu=9G %s %s %s %s %s %s && srun -n1 -c1 mv -v %s %s\n'%(RUN, input_catalog, temp_output_catalog, str(box_size), '0', '999', temp_output_catalog, output_catalog)
#    print(command)
    joblist.write(command)
joblist.close()

