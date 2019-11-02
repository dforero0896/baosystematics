#!/usr/bin/env python
import sys
import os
import numpy as np
if len(sys.argv) == 6:
	cat_type = 'gal'
	overwrite = bool(int(sys.argv[5]))
	r_min = None
	r_max = r_min
elif len(sys.argv) == 9:
	cat_type = 'void'
	r_min = sys.argv[5]
	r_max = sys.argv[6]
	ran_void_cat = sys.argv[7]
	overwrite = bool(int(sys.argv[8]))
else:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH JOB_LIST_ID CONF_FILE [R_MIN R_MAX VOID_RAN_DIR] OVERWRITE\n'%os.path.basename(sys.argv[0]))
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
joblist_id = sys.argv[3]
conf_file = sys.argv[4]
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
regfirst = {r:True for r in regions}
joblist_dir = os.path.join(this_dir, 'joblist')
if not os.path.isdir(joblist_dir):
	os.mkdir(joblist_dir)
bash_script_name = os.path.join(joblist_dir,'fcfc_%s_%s.sh'%(cat_type,joblist_id))
job_sub_name = os.path.join(joblist_dir, 'fcfcJob.sbatch')
bash_script = open(bash_script_name, 'w')
fdat = [fn for fn in f if '.dat.' in fn]
for fileno, fileName in enumerate(fdat):
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
	bash_script.write('srun -n 1 -c 64 /global/cscratch1/sd/dforero/baosystematics/bin/2pcf --conf=%s --data=%s --rand=%s --rand-convert=1 --data-convert=1 --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --data-aux-min=%s --data-aux-max=%s --rand-aux-min=%s --rand-aux-max=%s\n'%(conf_file, dat_cat_file, ran_cat_file, count_mode, dd_file, dr_file, rr_file, out_file, r_min, r_max, r_min, r_max))
bash_script.close()
dd_dir = os.path.join(outPath, 'DD_files')
dr_dir = os.path.join(outPath, 'DR_files')
rr_dir = os.path.join(outPath, 'RR_files')
paircount_dirs = [dd_dir, dr_dir, rr_dir]
for dir_ in paircount_dirs:
	if not os.path.isdir(dir_):
		os.mkdir(dir_)
