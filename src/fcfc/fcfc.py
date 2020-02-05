#!/usr/bin/env python
import sys
import os
import numpy as np
if len(sys.argv) == 6:
	cat_type = 'gal'
	overwrite = bool(int(sys.argv[5]))
	r_min = None
	r_max = r_min
	subsample_size = None
	sys.stdout.write('Looking for gal catalogs\n')
if len(sys.argv) == 7:
	cat_type = 'gal'
	subsample_size = int(sys.argv[5])
	overwrite = bool(int(sys.argv[6]))
	r_min = None
	r_max = r_min
	sys.stdout.write('Looking for gal catalogs\n')
elif len(sys.argv) == 8:
	cat_type = 'void'
	r_min = sys.argv[5]
	r_max = sys.argv[6]
	overwrite = bool(int(sys.argv[7]))
	subsample_size = None
	sys.stdout.write('Looking for void catalogs\n')
elif len(sys.argv) == 9:
	cat_type = 'void'
	r_min = sys.argv[5]
	r_max = sys.argv[6]
	subsample_size = int(sys.argv[7])
	overwrite = bool(int(sys.argv[8]))
	sys.stdout.write('Looking for void catalogs\n')
else:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH JOB_LIST_ID CONF_FILE [R_MIN R_MAX] [SUBSAMPLE_SIZE] OVERWRITE\n'%os.path.basename(sys.argv[0]))
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = sys.argv[1]
outPath = sys.argv[2]
joblist_id = sys.argv[3]
conf_file = sys.argv[4]
WORKDIR="/global/cscratch1/sd/dforero/baosystematics"
RUN=os.path.join(WORKDIR, 'bin/2pcf')
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
if cat_type == 'void': bash_script_name = bash_script_name.replace('.sh', '_R-%s-%s.sh'%(r_min, r_max))
job_sub_name = os.path.join(joblist_dir, 'fcfcJob.sbatch')
fdat = [fn for fn in f if '.dat.' in fn]
if subsample_size != None:
	fdat_sub = [fn for fn in fdat if 'NGC' in fn]
	fdat_sub = fdat_sub[:subsample_size]
	[fdat_sub.append(fdat_sub[i].replace('NGC', 'SGC')) for i in range(subsample_size)]
	sys.stdout.write('Writing %i commands for a subsample of %i mocks.\n'%(len(fdat_sub), subsample_size))
	fdat = fdat_sub
	bash_script_name = bash_script_name.replace('.sh', '_sub-%i.sh'%subsample_size)
bash_script = open(bash_script_name, 'w')
for fileno, fileName in enumerate(fdat):
	dat_cat_file = os.path.join(inPath,fileName)
	if cat_type == 'void': fileName = fileName.replace('VOID', 'VOID.R-%s-%s'%(r_min, r_max))
	out_file = os.path.join(outPath,'TwoPCF_'+fileName)
	if os.path.isfile(out_file) and not overwrite:
		continue
	reg = get_region(fileName)
	dd_file = os.path.join(outPath,'DD_files/DD_'+fileName)
	dr_file = os.path.join(outPath,'DR_files/DR_'+fileName)
	if cat_type=='void':
		ran_cat_file = os.path.join(WORKDIR,'results/%s/void_ran/EZ_ELG_RDZ_void_ran_%s_R-%s-%s.ascii'%(joblist_id, reg, r_min, r_max))
		if not os.path.exists(ran_cat_file):
			sys.stdout.write('ERROR:\tRandom void catalog not found.\n')
			sys.exit(1)
		if regfirst[reg]:
			regfirst[reg]=False
			count_mode = 7
		else:
			count_mode = 3
		rr_file = os.path.join(outPath,'RR_files/RR_%s_R-%s-%s'%(reg, r_min, r_max))
	else:
		ran_cat_file = dat_cat_file.replace('.dat.', '.ran.')
		rr_file = os.path.join(outPath,'RR_files/RR_'+fileName)
		count_mode = 7
	if not os.path.isfile(ran_cat_file):
		continue
	bash_script.write('srun -n 1 -c 64 %s --conf=%s --data=%s --rand=%s --rand-convert=1 --data-convert=1 --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --data-aux-min=%s --data-aux-max=%s --rand-aux-min=%s --rand-aux-max=%s\n'%(RUN, conf_file, dat_cat_file, ran_cat_file, count_mode, dd_file, dr_file, rr_file, out_file, r_min, r_max, r_min, r_max))
bash_script.close()
dd_dir = os.path.join(outPath, 'DD_files')
dr_dir = os.path.join(outPath, 'DR_files')
rr_dir = os.path.join(outPath, 'RR_files')
paircount_dirs = [dd_dir, dr_dir, rr_dir]
for dir_ in paircount_dirs:
	if not os.path.isdir(dir_):
		os.mkdir(dir_)
