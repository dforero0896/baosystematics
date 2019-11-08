#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
if len(sys.argv)!=5:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{0} MOCK_DIR INPUT_2PCF OUT_FILE BEST_FIT_FILE'.format(sys.argv[0]))
mockPath = sys.argv[0]
def saveMockList(path, name='mocklist.dat'):
	mockList = os.listdir(path)
	mockFile = open(name, 'w')
	for m in mockList:
		mockFile.write('%s%s\n'%(path, m))
	mockFile.close()
mockFile='mocklist.dat'
saveMockList(mockPath, mockFile)
input2PCF = '/home/epfl/dforero/comb2pcf/data_comb_2pcf/TwoPCF_eBOSS_ELG_clustering_CGV_v4.dat.ascii'
outFile = 'ELG_baofit.dat'
bestFitFile = 'ELG_bestfit.dat'
#os.system('/home/epfl/zhaoc/work/codes/BAOfit/code_nest/bestfit -c baofit.conf -i %s -m %s -o %s -b %s'%(input2PCF, mockFile, outFile, bestFitFile))

os.system('/home/epfl/zhaoc/work/codes/BAOfit/code_nest/BAOfit -c baofit.conf -i %s -m %s -o %s -b %s'%(input2PCF, mockFile, outFile, bestFitFile))

