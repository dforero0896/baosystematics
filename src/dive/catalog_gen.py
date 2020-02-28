#!/usr/bin/env python
import sys
import os
WORKDIR = "/hpcstorage/dforero/projects/baosystematics"
if len(sys.argv) != 5:
	sys.stdout.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH JOB_LIST_ID OVERWRITE(int)\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
joblist_out = sys.argv[3]
overwrite = bool(int(sys.argv[4]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stdout.write('ERROR: Empty input directory.')
	sys.exit(1)
bash_script_name = os.path.join(this_dir,'catalog_gen_%s.sh'%joblist_out)
job_sub_name = os.path.join(this_dir, 'diveJob.sh')
bash_script = open(bash_script_name, 'w')
for i, fileName in enumerate(f):
	if 'dat' in fileName:
		outfile = os.path.join(outPath,fileName.replace('dat', 'VOID.dat'))
		infile = os.path.join(inPath, fileName)
		if os.path.isfile(outfile) and not overwrite:
			continue
		bash_script.write(os.path.join(WORKDIR,'bin/DIVE/DIVE %s %s\n'%(infile, outfile)))
	sys.stdout.write("Done %i/%i\r"%(i,len(f)))
	sys.stdout.flush()
bash_script.close()
tmp_header = os.path.join(this_dir, 'diveJob_header.sh')
os.system('head -19 %s > %s'%(job_sub_name, tmp_header))
os.system('cat %s > %s'%(tmp_header, job_sub_name))
os.system('cat %s >> %s'%(bash_script_name, job_sub_name))
os.system('rm %s'%tmp_header)#TODO: Evaluate the necesity of having copies of submission scripts for different steps
