#!/usr/bin/env python
import sys
import os
import numpy as np
if len(sys.argv) != 8:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH JOB_LIST_ID CONF_FILE R_MIN R_MAX OVERWRITE\n'%sys.argv[0])
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
joblist_id = sys.argv[3]
conf_file = sys.argv[4]
r_min = sys.argv[5]
r_max = sys.argv[6]
overwrite = bool(int(sys.argv[7]))
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)
if not os.path.isdir(outPath):
	os.mkdir(outPath)
regions=['NGC', 'SGC']
def get_region(fn):
	for r in regions:
		if r in fn.upper():
			return r;break
	sys.stderr.write('ERROR: Could not identify region.\n')
	sys.exit(1)
cat_types=['gal', 'void']
def get_cat_type(fn):
	for t in cat_types:
		if t in fn.lower():
			return t;break
	sys.stderr.write('ERROR: Could not identify catalog type=(gal, void) from CONF_FILE.\n')
	sys.exit(1)
cat_type = get_cat_type(conf_file)			
regfirst = {r:True for r in regions}
bash_script_name = os.path.join(this_dir,'fcfc_%s_%s.sh'%(cat_type,joblist_id))
job_sub_name = os.path.join(this_dir, 'fcfcJob.sh')
bash_script = open(bash_script_name, 'w')
fdat = [fn for fn in f if '.dat.' in fn]
for fileName in fdat:
	print(fileName)
	out_file = os.path.join(outPath,'TwoPCF_'+fileName)
	if os.path.isfile(out_file) and not overwrite:
		continue
	reg = get_region(fileName)
	dat_cat_file = os.path.join(inPath,fileName)
	dd_file = os.path.join(outPath,'DD_files/DD_'+fileName)
	dr_file = os.path.join(outPath,'DR_files/DR_'+fileName)
	if cat_type=='void':
		ran_cat_file = '/home/epfl/dforero/zhao/void/baosystematics/results/%s/void_ran/EZ_ELG_RDZ_void_ran_%s.ascii'%(joblist_id, reg)
		if not os.path.exists(ran_cat_file):
			sys.stdout.write('ERROR:\tRandom void catalog not found.\n')
			sys.exit(1)
		if regfirst[reg]:
			regfirst[reg]=False
			count_mode = 7
		else:
			count_mode = 3
		rr_file = os.path.join(outPath,'RR_files/RR_%s'%reg)
	else:
		ran_cat_file = dat_cat_file.replace('.dat.', '.ran.')
		rr_file = os.path.join(outPath,'RR_files/RR_'+fileName)
		count_mode = 7
	if not os.path.isfile(ran_cat_file):
		continue
	bash_script.write('srun /home/epfl/dforero/scripts/FCFC --conf=%s --data=%s --rand=%s --rand-convert=1 --data-convert=1 --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --data-aux-min=%s --data-aux-max=%s --rand-aux-min=%s --rand-aux-max=%s\n'%(conf_file, dat_cat_file, ran_cat_file, count_mode, dd_file, dr_file, rr_file, out_file, r_min, r_max, r_min, r_max))
bash_script.close()
tmp_header = os.path.join(this_dir, 'fcfcJob_header.sh')
os.system('head -18 %s > %s'%(job_sub_name, tmp_header))
os.system('cat %s > %s'%(tmp_header, job_sub_name))
os.system('cat %s >> %s'%(bash_script_name, job_sub_name))
os.system('rm %s'%tmp_header)#TODO: Evaluate the necesity of having copies of submission scripts for different steps
os.system('mkdir %s'%os.path.join(outPath, 'DD_files'))
os.system('mkdir %s'%os.path.join(outPath, 'DR_files'))
os.system('mkdir %s'%os.path.join(outPath, 'RR_files'))

