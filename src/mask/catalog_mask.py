#!/usr/bin/env python
import sys
import os
if len(sys.argv) != 6:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH CONFIG_FILE JOB_LIST_ID OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
config_file = sys.argv[3]
joblist_id = sys.argv[4]
overwrite = bool(int(sys.argv[5]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.\n')
	sys.exit(1)
if not os.path.isdir(outPath):
	os.system('mkdir %s'%outPath)
outdir=os.path.join(this_dir, 'joblist')
if not os.path.isdir(outdir):
	os.mkdir(outdir)
bash_script = open(os.path.join(outdir,'catalog_mask_%s.sh'%joblist_id), 'w')
add_bash_script = open(os.path.join(outdir,'catalog_addmask_%s.sh'%joblist_id), 'w')
for i, fileName in enumerate(f):
	_, infile_ext = os.path.splitext(fileName)
	infile = os.path.join(inPath, fileName)
	if infile_ext == '.ascii':
		outfile=os.path.join(outPath,fileName.replace('VOID', 'VOID.MASKED'))
		fmt = 0
	elif infile_ext == '.fits':
		outfile=os.path.join(outPath,fileName.replace('Catalog', 'Catalog.MASKED'))
		fmt = 1
	# Create job list for the additional masks
	additional_outpath = outPath.replace('vetomask', 'addmask')
	if not os.path.isfile(additional_outpath):
		add_bash_script.write('/global/cscratch1/sd/dforero/baosystematics/src/mask/additional_mask.py %s %s\n'%(outfile, additional_outpath))
	if os.path.isfile(outfile) and not overwrite:
		continue 
	bash_script.write('/global/cscratch1/sd/dforero/baosystematics/bin/vetomask --input=%s --output=%s --format=%i --conf=%s\n'%(infile, outfile, fmt, config_file))
	sys.stdout.write("Done %i/%i\r"%(i,len(f)))


bash_script.close()
add_bash_script.close()
