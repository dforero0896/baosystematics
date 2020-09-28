#!/usr/bin/env python
import argparse
import glob
#from nbodykit.source.catalog import CSVCatalog
#from nbodykit import cosmology
from nbodykit.lab import *
from nbodykit import setup_logging
import dask.array as da
from nbodykit import CurrentMPIComm
comm = CurrentMPIComm.get()
from dotenv import load_dotenv
load_dotenv()
import os
WORKDIR=os.getenv('WORKDIR')
import matplotlib.pyplot as plt
import numpy as np


if __name__=='__main__':  
    setup_logging()
#    nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
#    iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
#    inode = MPI.Get_processor_name()    # Node where this MPI process runs
    test_filename = glob.glob(f"{WORKDIR}/patchy_results/box1/redshift/nosyst/mocks_gal_xyz/CATALPTCICz*S1005638091*")[0]
    max_names = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'vmax']
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help="Catalog to compute the power spectrum with.", default=test_filename)
    parser.add_argument('-n', '--num-cols', help="Number of columns. First three columns are assumed to be position. Default=7.", default=7, type=int)
    parser.add_argument('-z', '--redshift', help="Redshift", default=0.466, type=float)
    parser.add_argument('-hub', '--hubble', help="Dimensionless Hubble. Default is h=0.6777", default=0.6777, type=float)
    parser.add_argument('-om', '--Omega0_cdm', help="Current matter abundance. Default is 0.307115", default = 0.307115, type=float)
    parser.add_argument('-ob', '--Omega0_b', help="Current baryon abundance. Default 0.048206.", default = 0.048206, type=float)
    parser.add_argument('-t', '--T0_cmb', help="Current CMB temperature. Default 2.7255 K.", default=2.7255, type=float)
    parser.add_argument('-nnu', '--N_ur', help="Number of massless neutrino species. Default 2.046.", default=2.046, type=float)
    parser.add_argument('-ns', '--n_s', help="Tilt of primordial power spectrum. Default 0.96", default = 0.96, type=float)
    parser.add_argument('-rsd', '--rsd', help="Whether to compute the redshift space catalog. Default 0.", default=0)
    parser.add_argument('-bs', '--box-size', help="Box size of the simulation box. Default 2500 Mpc/h.", default=2500, type=float)
    parser.add_argument('-o', '--out', help="Output directory. Default: . ", default='.')
    parsed=parser.parse_args()
    args = vars(parsed)
    print(args)
    cosmo = cosmology.cosmology.Cosmology(h=args['hubble'], T0_cmb=args['T0_cmb'], Omega0_cdm=args['Omega0_cdm'], Omega0_b=args['Omega0_b'], N_ur=args['N_ur'], n_s=args['n_s'])
    names = max_names[:args['num_cols']]
    line_of_sight=[0,0,1]
    catalog=CSVCatalog(args['filename'], names, delim_whitespace=True, dtype='float')
    redshift = args['redshift']
    Plin = cosmology.LinearPower(cosmo, redshift, transfer='EisensteinHu')
    catalog['Position'] = da.stack([catalog[s] for s in names[:3]], axis=-1)
    if args['num_cols']>3:
        catalog['Velocity'] = da.stack([catalog[s] for s in names[3:-1]], axis=-1)
        catalog['VelocityOffset'] = (1 + redshift) / (100 * cosmo.efunc(redshift))
        if bool(int(args['rsd'])): catalog['RSDPosition'] = catalog['Position'] + catalog['VelocityOffset'] * line_of_sight
    mesh = catalog.to_mesh(resampler='cic', Nmesh=256, compensated=True, position='Position', BoxSize=args['box_size'])
    r = FFTPower(mesh, mode='1d', dk=0.005, kmin=0.01) 
    Pk = r.power
    print(Pk)
    for k in Pk.attrs:
        print("%s = %s" %(k, str(Pk.attrs[k])))
    
    # print the shot noise subtracted P(k)
    plt.loglog(Pk['k'], Pk['power'].real - Pk.attrs['shotnoise'], label="1D")

    r = FFTPower(mesh, mode='2d', dk=0.005, kmin=0.01, Nmu=5, los=[0,0,1], poles=[0])
    poles = r.poles
    for ell in [0]:
        label = r'$\ell=%d$' % (ell)
        P = poles['power_%d' %ell].real
        if ell == 0: P = P - poles.attrs['shotnoise']
        plt.loglog(poles['k'], P, label=label)    
    plt.legend(loc=0)
    plt.xlabel(r"$k$ [$h \ \mathrm{Mpc}^{-1}$]")
    plt.ylabel(r"$k \ P_\ell$ [$h^{-2} \mathrm{Mpc}^2$]")
    plt.xlim(0.01, 0.6)


    Pk1d=np.c_[Pk['k'], Pk['power'].real-Pk.attrs['shotnoise']]
    np.savetxt(f"{args['out']}/powspec1d_{os.path.basename(args['filename'])}", Pk1d)
    Pk1d=np.c_[poles['k'], poles['power_0'].real-poles.attrs['shotnoise']]
    np.savetxt(f"{args['out']}/powspec2d_ell0_{os.path.basename(args['filename'])}", Pk1d)
    plt.gcf()
    plt.savefig(f"{args['out']}/powspec_{os.path.basename(args['filename'])}.pdf", dpi=300, rasterize=True)
