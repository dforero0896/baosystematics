#!/usr/bin/env python3
import os
import sys
import tempfile
if len(sys.argv)!=4:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} INPUT_DIR OUT_DIR CAT_TYPE'.format(sys.argv[0]))
input2PCF = sys.argv[1]
outPath = sys.argv[2]
cat_type = sys.argv[3]
WORKDIR='/global/cscratch1/sd/dforero/baosystematics/'
try:
	(_, _, in2pcf) = next(os.walk(input2PCF))
except StopIteration:
	sys.stderr.write('ERROR: Empty input directory.\n')
	sys.exit(1)  
if not os.path.isdir(outPath):
	os.mkdir(outPath)
mockFile = tempfile.NamedTemporaryFile(mode='w+t')
mockFile_name = mockFile.name
r = os.path.join(outPath, 'cov.dat')
if cat_type=='void':
	run = os.path.join(WORKDIR,'bin/BAOfit_void/BAOfit')
elif cat_type=='gal':
	run = os.path.join(WORKDIR,'bin/BAOfit_galaxy/BAOfit')
else:
	sys.exit('ERROR:\tCatalog type not understood.\nCAT_TYPE=void, gal\n')
for m in in2pcf:
	mockFile.writelines(os.path.join(input2PCF, m+'\n'))
print(mockFile.read())
for idx, tpcf in enumerate(in2pcf):
	tpcf_fn = os.path.join(input2PCF, tpcf)
	print(tpcf_fn)
	tpcf_base, ext = os.path.splitext(tpcf)
	if idx==0:
		c = os.path.join(WORKDIR,'src/baofit/baofit_covcomp.conf')
	else:
		c = os.path.join(WORKDIR,'src/baofit/baofit.conf')
	i = tpcf_fn
	m = mockFile_name
	o = os.path.join(outPath, tpcf_base+'_')
	b = o+'mystats.txt' # Check if the output of stats_center exists.
	if os.path.isfile(b):
		continue
	os.system('%s -c %s -i %s -m %s -o %s -b %s -r %s'%(run, c, i, m, o, b, r))
	os.system('python %s %s %s'%(os.path.join(WORKDIR, 'src/baofit/stats_center.py'), o, cat_type))
mockFile.close()
