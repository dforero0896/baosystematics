#!/usr/bin/env python

import os
import sys
import shutil
#originaldirno = '/home/epfl/atamone/old/LastClaudio/Covariance/shuffle/outputnormalv7b/v7wosys/no_RIC'
#originaldirall = '/home/epfl/atamone/old/LastClaudio/Covariance/shuffle/outputnormalv7b/v7wsys/RIC'
originaldirno='/home/epfl/dforero/scratch/projects/baosystematics/results/nosyst_v7/tpcf_void_mock_R-15.5-50'
originaldirall='/home/epfl/dforero/scratch/projects/baosystematics/results/allsyst_v7/tpcf_void_mock_R-15.5-50'
originaldirs = [originaldirno, originaldirall]
mydirall = '/home/epfl/dforero/scratch/projects/baosystematics/results/allsyst_v7/tpcf_gal_mock_nowt'
mydirno = '/home/epfl/dforero/scratch/projects/baosystematics/results/nosyst_v7/tpcf_gal_mock_nowt'
mydirs = [mydirno, mydirall]
#targetdirall='/home/epfl/dforero/scratch/projects/baosystematics/results/allsyst_v7/tpcf_gal_mock'
#targetdirno='/home/epfl/dforero/scratch/projects/baosystematics/results/nosyst_v7/tpcf_gal_mock'
targetdirall='/home/epfl/dforero/scratch/projects/baosystematics/results/allsyst_v7/tpcf_void_mock_R-15.5-50_SUBSET'
targetdirno='/home/epfl/dforero/scratch/projects/baosystematics/results/nosyst_v7/tpcf_void_mock_R-15.5-50_SUBSET'
os.makedirs(targetdirall, exist_ok=True)
os.makedirs(targetdirno, exist_ok=True)
targetdirs=[targetdirno, targetdirall]
regions = ['NGC', 'SGC']
for r in regions:
    for i in range(2):
#        original = os.listdir(os.path.join(originaldirs[i], r))
        original = [f for f in os.listdir(originaldirs[i]) if r in f]
        my = [f for f in os.listdir(mydirs[i]) if r in f]
#        tocopy = ['xi0_%04d.dat'%int(f.replace('TwoPCF_EZ_ELG_clustering_%s_v7.dat.'%r,'').replace('.ascii', '')) for f in my]
        tocopy = [f.replace('TwoPCF_EZ_ELG_clustering_%s_v7.dat.'%r,'TwoPCF_EZ_ELG_RDZ_XYZ_clustering_%s_v7.VOID.R-15.5-50.MASKED.dat.'%r) for f in my]
	
#        [os.system('cp %s %s'%(os.path.join(originaldirs[i], r, f), os.path.join(targetdirs[i], f.replace('.dat', '_%s.dat'%r)))) for f in tocopy]
        [os.system('cp %s %s'%(os.path.join(originaldirs[i], f), os.path.join(targetdirs[i], f))) for f in tocopy]
