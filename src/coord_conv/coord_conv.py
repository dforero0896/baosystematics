#!/usr/bin/env python
import numpy as np
import sys
import os
if len(sys.argv) != 6:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH CONFIG_FILE JOB_LIST_ID OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
config_file = sys.argv[3]
joblist_out = sys.argv[4]
overwrite = bool(int(sys.argv[5]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.\n')
	sys.exit(1)
if len(f)==0:
	sys.stdout.write('ERROR: Empty input directory.\n')
	sys.exit(1)
directions = ['rdz2xyz', 'xyz2rdz']
config_basename = os.path.basename(config_file)
config_ok = False
for direction in directions:
	if direction in config_basename:
		exe = direction
		config_ok = True
if not config_ok:
	sys.stdout.write('ERROR:\tThe CONFIG_FILE must contain either \'rdx2xyz\' or \'xyz2rdz\'.\n')
	sys.exit(1)
bash_script = open(os.path.join(this_dir,'%sJobList_%s.sh'%(exe, joblist_out)), 'w')
for fileName in f:
	in_file = os.path.join(inPath,fileName)
	out_file = os.path.join(outPath,fileName.replace('ELG', 'ELG_%s'%exe[-3:].upper()))
	if os.path.isfile(out_file) and not overwrite:
		continue
	bash_script.write('/home/epfl/dforero/zhao/void/baosystematics/bin/%s -c %s -i %s -o %s\n'%(exe, config_file, in_file, out_file))



bash_script.close()
