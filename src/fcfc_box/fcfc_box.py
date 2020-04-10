#!/usr/bin/env python
import sys
import os
import numpy as np
if len(sys.argv) == 7:
	cat_type = 'gal'
	ran_cat_file=sys.argv[5]
	overwrite = bool(int(sys.argv[6]))
	r_min = None
	r_max = r_min
	subsample_size = None
	sys.stdout.write('Looking for gal catalogs\n')
elif len(sys.argv) == 8:
	cat_type = 'gal'
	subsample_size = int(sys.argv[5])
	ran_cat_file=sys.argv[6]
	overwrite = bool(int(sys.argv[7]))
	r_min = None
	r_max = r_min
	sys.stdout.write('Looking for gal catalogs\n')
elif len(sys.argv) == 9:
	cat_type = 'void'
	r_min = sys.argv[6]
	r_max = sys.argv[7]
	ran_cat_file=sys.argv[5]
	overwrite = bool(int(sys.argv[8]))
	subsample_size = None
	sys.stdout.write('Looking for void catalogs\n')
elif len(sys.argv) == 10:
	cat_type = 'void'
	r_min = sys.argv[6]
	r_max = sys.argv[7]
	subsample_size = int(sys.argv[8])
	ran_cat_file=sys.argv[5]
	overwrite = bool(int(sys.argv[9]))
	sys.stdout.write('Looking for void catalogs\n')
else:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\nUSAGE:\tpython %s INPUT_PATH OUTPUT_PATH JOB_LIST_ID CONF_FILE RAN_CAT_FILE [R_MIN R_MAX] [SUBSAMPLE_SIZE] OVERWRITE\n'%os.path.basename(sys.argv[0]))
	sys.exit(1)
this_dir = os.path.dirname(sys.argv[0])
inPath = os.path.abspath(sys.argv[1])
outPath = os.path.abspath(sys.argv[2])
joblist_id = sys.argv[3]
conf_file = os.path.realpath(sys.argv[4])
WORKDIR="/hpcstorage/dforero/projects/baosystematics"
RUN=os.path.join(WORKDIR, 'bin/FCFC_box/2pcf')
ran_cat_file = os.path.abspath(ran_cat_file)
try:
	(_, _, f) = next(os.walk(inPath))
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)
if not os.path.isdir(outPath):
	os.mkdir(outPath)
if not 'none' in ran_cat_file and not os.path.exists(ran_cat_file): 
	sys.stdout.write('ERROR:\tRandom void catalog not found.\n')
	sys.exit(1)
	
joblist_dir = os.path.join(this_dir, 'joblist')
if not os.path.isdir(joblist_dir):
	os.mkdir(joblist_dir)
bash_script_name = os.path.join(joblist_dir,'fcfc_%s_%s.sh'%(cat_type,joblist_id))
if cat_type == 'void': bash_script_name = bash_script_name.replace('.sh', '_R-%s-%s.sh'%(r_min, r_max))
if subsample_size != None:
	fdat_sub = f[:subsample_size]
	sys.stdout.write('Writing %i commands for a subsample of %i mocks.\n'%(len(fdat_sub), subsample_size))
	fdat = fdat_sub
	bash_script_name = bash_script_name.replace('.sh', '_sub-%i.sh'%subsample_size)
else: fdat=f
bash_script = open(bash_script_name, 'w')
first=True
counter=0
for fileno, fileName in enumerate(fdat):
	dat_cat_file = os.path.join(inPath,fileName)
	if cat_type == 'void': fileName = fileName.replace('VOID', 'VOID.R-%s-%s'%(r_min, r_max))
	out_file = os.path.join(outPath,'TwoPCF_'+fileName)
	if os.path.isfile(out_file) and not overwrite:
		continue
	counter+=1
	dd_file = os.path.join(outPath,'DD_files/DD_'+fileName)
	dr_file = os.path.join(outPath,'DR_files/DR_'+fileName)
	rr_file = os.path.join(WORKDIR,'patchy_results/randoms/RR_%s'%os.path.basename(ran_cat_file))
#	if cat_type == 'void':
#		rr_file=os.path.join(WORKDIR, 'patchy_results/randoms/RR_box_uniform_random_seed1_0-2500.dat')
#	elif cat_type == 'gal':
#		rr_file=os.path.join(WORKDIR, 'patchy_results/randoms/RR_box_uniform_random_seed2_0-2500_BIG.dat')
	if first and not os.path.exists(rr_file):
		first=False
		count_mode = 7
	else:
		count_mode = 3
	if 'none' in ran_cat_file: count_mode=1
	bash_script.write('srun -n 1 -c 16 %s --conf=%s --data=%s --rand=%s --count-mode=%s --dd=%s --dr=%s --rr=%s --output=%s --data-aux-min=%s --data-aux-max=%s --rand-aux-min=%s --rand-aux-max=%s \n'%(RUN, conf_file, dat_cat_file, ran_cat_file, count_mode, dd_file, dr_file, rr_file, out_file, r_min, r_max, r_min, r_max))
bash_script.close()
print("Wrote %s commands in job list: %s"%(counter, bash_script_name))
dd_dir = os.path.join(outPath, 'DD_files')
dr_dir = os.path.join(outPath, 'DR_files')
rr_dir = os.path.join(outPath, 'RR_files')
paircount_dirs = [dd_dir, dr_dir, rr_dir]
for dir_ in paircount_dirs:
	if not os.path.isdir(dir_):
		os.mkdir(dir_)
