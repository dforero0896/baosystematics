#!/usr/bin/env python3
from astropy.table import Table, Column
from scipy import constants, in1d
import pymangle
import healpy
import numpy as np

#iofmt = 'fits'
#ifile = '/global/homes/z/zhaoc/work/EZmock/ELG_veto/input/EZ_ELG_clustering_NGC_v7.dat.1.brickmask.fits'
#ofile = '/global/homes/z/zhaoc/work/EZmock/ELG_veto/input/EZ_ELG_clustering_NGC_v7.dat.1.newmask.fits

iofmt = 'ascii'
ifile = '/global/homes/z/zhaoc/work/EZmock/ELG_veto/input/EZmock_eBOSS_ELG_v5_0001.dat'
ofile = '/global/homes/z/zhaoc/work/EZmock/ELG_veto/input/EZmock_eBOSS_ELG_v5_0001.dat.more'
icols = ['RA','DEC','Z','VETOMASK','MCHUNK']

mdir = '/global/homes/z/zhaoc/work/EZmock/ELG_veto/masks'
mskbit_col = 'VETOMASK'
mskbit_col_new = 'newbit'

if iofmt == 'fits':
  catalog = Table.read(ifile, format='fits', hdu=1)
elif iofmt == 'ascii':
  catalog = Table.read(ifile, format='ascii.no_header', names=icols)
else:
  raise ValueError('Unrecognized IO fmt!')

mskbit = catalog[mskbit_col].astype('int16')

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
mskbitcheck = '{}/ELG_allobj.mskbitcheck.hp1024.fits'.format(mdir)
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
theta_rad = catalog['DEC'] * conversion
phi_rad = catalog['RA'] * conversion
theta_rad = constants.pi / 2. - theta_rad
phi_rad %= 2. * constants.pi
pix = healpy.ang2pix(nside, theta_rad, phi_rad, nest=nest)
mask = in1d(pix,mask_pixel)

mskbit += mask * 2**8

# adding 2**9 for centerpost masking
mask_centerpost = '{}/ELG_centerpost.ply'.format(mdir)
mask_mng = pymangle.Mangle(mask_centerpost)
mask = mask_mng.polyid(catalog['RA'],catalog['DEC']) != -1
mskbit += mask * 2**9

# adding 2**10 for tdss_fes masking
mask_tdss = '{}/ELG_TDSSFES_62arcsec.pix.snap.balk.ply'.format(mdir)
mask_mng = pymangle.Mangle(mask_tdss)
mask = mask_mng.polyid(catalog['RA'],catalog['DEC']) != -1
mskbit += mask * 2**10

# adding 2**11 for bad photometric calibration
mask_badexp = '{}/ebosselg_badphot.26Aug2019.ply'.format(mdir)
mask_mng = pymangle.Mangle(mask_badexp)
mask = mask_mng.polyid(catalog['RA'],catalog['DEC']) != -1
mskbit += mask * 2**11

# saving output
mskcol = Column(name=mskbit_col_new, data=mskbit)
catalog.add_column(mskcol)
if iofmt == 'fits':
  catalog.write(ofile, format='fits', overwrite=True)
elif iofmt == 'ascii':
  catalog.write(ofile, format='ascii.no_header', overwrite=True)
