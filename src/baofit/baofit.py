#!/usr/bin/env python3
import os
import sys
if len(sys.argv)!=5:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} MOCK_DIR INPUT_2PCF OUT_FILE BEST_FIT_FILE'.format(sys.argv[0]))
mockPath = sys.argv[1]
input2PCF = sys.argv[2]
outFile = sys.argv[3]
bestFitFile = sys.argv[4]
def saveMockList(path, name='mocklist.dat'):
	mockList = os.listdir(path)
	mockFile = open(name, 'w')
	for m in mockList:
		mockFile.write(os.path.join(path, m+'\n'))
	mockFile.close()
mockFile='mocklist.dat'
saveMockList(mockPath, mockFile)
#os.system('/home/epfl/zhaoc/work/codes/BAOfit/code_nest/bestfit -c baofit.conf -i %s -m %s -o %s -b %s'%(input2PCF, mockFile, outFile, bestFitFile))

os.system('/global/cscratch1/sd/dforero/baosystematics/bin/BAOfit_galaxy/BAOfit -c baofit.conf -i %s -m %s -o %s -b %s'%(input2PCF, mockFile, outFile, bestFitFile))

