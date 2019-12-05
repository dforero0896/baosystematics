#!/usr/bin/env python3
#additional_mask.py
import os
import sys
from scipy import constants, in1d
import pymangle
import healpy
import numpy as np
from astropy.table import Table, Column
from astropy.io import fits, ascii

if len(sys.argv)!=3:
	sys.exit('ERROR:\tUnexpected number of arguments.\nUSAGE:\t{} INPUT OUTPUT'.format(sys.argv[0]))
infile = sys.argv[1]
ascii_incols = ['RA', 'DEC', 'Z', 'R', 'VETOMASK', 'MCHUNK']
outfile = infile.replace('MASKED', 'COMPMASKED')
mskbit_col = 'VETOMASK'
mskbit_col_new = 'newbit'

if '.fits' in infile:
        intable = Table.read(infile, format='fits', hdu=1)
else:
	sys.stdout.write('Assuming ascii file.\n')
	intable = Table.read(infile, format='ascii.no_header', names = ascii_incols)
ext=os.path.splitext(infile)
WORKDIR='/global/cscratch1/sd/dforero/baosystematics/'
MASKDIR=os.path.join(WORKDIR, 'data/ELG_masks')

mskbit = intable[mskbit_col].astype('int16')

# mskbits:
# 2**0: valid
# 2**1: grz-depth
# 2**2: xy-bug
# 2**3: anymask
# 2**4: tycho2blob
# 2**5: bright objects
# 2**6: gaia
# 2**7: mira

# adding 2**8 for discrepancy between mskbit and anymask
mskbitcheck = os.path.join(MASKDIR, 'ELG_allobj.mskbitcheck.hp1024.fits')
threshold = 0.1
nside = 1024; nest = False

data = Table.read(mskbitcheck, format='fits', hdu=1)
mask = np.zeros(len(data), dtype='bool')
for key in ['grz','xybug','any','t2b','bright']:
	notflag = data['{}_nnotflagok'.format(key)] + \
            data['{}_nnotflagfail'.format(key)]
	tmp = (notflag > 0) & \
        (data['{}_nnotflagfail'.format(key)] > threshold * notflag)
	mask |= tmp

mask_pixel = data['hpind'][mask]
assert set(mask_pixel) == set([2981667,3464728,3514005,3645255,4546075, \
    4685432,5867869,5933353,6031493,6072514,6080368,6092477,6301369,6408277, \
    6834661,2907700,3583785,3587880,4067035,4669088,6007074,6186688,6190785, \
    6199270,6371066,6547876,6551972,6645991,6711673,6735965,6744444,6744445, \
    6748540,6752636,6769023,6773119,6781133])

conversion = constants.degree
theta_rad = intable['DEC'] * conversion
phi_rad = intable['RA'] * conversion
theta_rad = constants.pi / 2. - theta_rad
phi_rad %= 2. * constants.pi
pix = healpy.ang2pix(nside, theta_rad, phi_rad, nest=nest)
mask = in1d(pix,mask_pixel)

mskbit += mask * 2**8

# adding 2**9 for centerpost masking
mask_centerpost = os.path.join(MASKDIR, 'ELG_centerpost.ply')
mask_mng = pymangle.Mangle(mask_centerpost)
mask = mask_mng.polyid(intable['RA'],intable['DEC']) != -1
mskbit += mask * 2**9

# adding 2**10 for tdss_fes masking
mask_tdss = os.path.join(MASKDIR, 'ELG_TDSSFES_62arcsec.pix.snap.balk.ply')
mask_mng = pymangle.Mangle(mask_tdss)
mask = mask_mng.polyid(intable['RA'],intable['DEC']) != -1
mskbit += mask * 2**10

# adding 2**11 for bad photometric calibration
mask_badexp = os.path.join(MASKDIR,'ebosselg_badphot.26Aug2019.ply')
mask_mng = pymangle.Mangle(mask_badexp)
mask = mask_mng.polyid(intable['RA'],intable['DEC']) != -1
mskbit += mask * 2**11

# saving output
mskcol = Column(name=mskbit_col_new, data=mskbit)
intable.add_column(mskcol)
if '.fits' in infile:
	intable.write(os.path.join(output,outfile), format='fits', overwrite=True)
elif iofmt == 'ascii':
	intable.write(os.path.join(output, outfile), format='ascii.no_header', overwrite=True)
