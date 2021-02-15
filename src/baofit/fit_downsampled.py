#!/usr/bin/env python
import numpy as np
import os, sys, glob
from dotenv import load_dotenv
load_dotenv() 
WORKDIR = os.getenv("WORKDIR") 
sys.path.append(f"{WORKDIR}/bin/2pcf_bao_fitter")
from src.fit import BAO_Fitter
import multiprocessing
from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
#dr = [0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
dr = [1.13, 1.18, 1.19, 1.25, 1.33]
comps = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
dr=[1.07]
comps=[0.4]
nthreads = 32
def fit_average_2pcf(ifile, mocks, plin, pnw, ptemp, outdir, symlinkid):
    long_path = (len(outdir) > 80)

    base = os.path.basename(ifile).replace("tpcf_void_mock_nowt_", "")

    if long_path:
        print(f"==> Long path detected, using symbolic links")
        if rank==0:
            os.makedirs("run", exist_ok=True)
        sym_odir = f"run/{symlinkid:03d}"
        try:
            if rank==0:
                os.symlink(outdir, sym_odir)

        except FileExistsError:
            if rank==0:
                os.unlink(sym_odir)
                os.symlink(outdir, sym_odir)
        #exit(0)

    if os.path.isdir(mocks):
        mocks = glob.glob(f"{mocks}/TwoPCF*")

    s_obs, xi_obs = np.loadtxt(ifile, usecols=(0, 1), unpack=True)
    bao_fitter = BAO_Fitter(plin_fn = plin, plin_nw_fn=pnw, pnw_temp_fn=ptemp,
            prior_params=((0.8, 1.2), (0, 25), (0,30)), 
            prior_types=('flat', 'flat', 'flat'),
            backend='multinest',
            a_smooth=1,
            k_norm=8e-3,
            smin=60,
            smax=150,
            sbin_size=5,
            kmin=2.5e-3,
            kmax=600,
            num_lnk_bin=2048,
            tolerance=0.01,
            live_points=1000,
            parameters=['a', 'B', 'Snl']
            )

    bao_fitter.compute_covariance(mocks)
    resume=False
    if long_path:
        map_params = bao_fitter.fit_analyze(xi_obs, s_obs, resume=resume, 
                outbase=f"{sym_odir}/{base}_")
        MPI.COMM_WORLD.Barrier()
        if rank==0:
            os.unlink(sym_odir)
    else:
        map_params = bao_fitter.fit_analyze(xi_obs, s_obs, resume=resume, 
                outbase=f"{outdir}/{os.path.basename(ifile)}_")


    return map_params

if __name__ == '__main__':
    plin = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Plin.dat"
    pnw = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Pnw.dat"
    counter = 1

    #pool = multiprocessing.Pool(processes = 16)
    for rec in ['patchy_results', 'patchy_recon_nods']:

        main_path = f"{WORKDIR}/{rec}/box1/redshift/smooth/"

        avg_tpcf_dir = f"{main_path}/tpcf_avg"

        process_list = []
        for r in dr:
            for comp in comps:
                ifile_list = glob.glob(f"{avg_tpcf_dir}/*flat_{comp}_*scaled{r}-*ascii")
                mockdir_list = glob.glob(f"{main_path}/flat_{comp}/tpcf_void_mock_nowt_R-scaled{r}-*/")
                
                if len(mockdir_list)>1: print(mockdir_list); sys.exit(f"Found more than one mock directory")
                #exit(0)
                template_list = glob.glob(f"{WORKDIR}/data/templates/templates/powspecFST*dr{r:.2f}*flat{comp:.2f}*N20*")
  
                if (len(ifile_list)==0) or (len(mockdir_list)==0) or (len(template_list)==0):
                    print(len(ifile_list), len(mockdir_list), len(template_list))
                    continue
                outdir = f"{main_path}/flat_{comp}/baofit/tpcf_void_mock_nowt_R-scaled{r}-50_AVG"
                os.makedirs(os.path.basename(outdir), exist_ok=True)
                os.makedirs(outdir, exist_ok=True)
                args = (ifile_list[0], mockdir_list[0], plin, pnw, template_list[0], outdir, counter)
                #pool.apply_async(fit_average_2pcf, args)
                #p = multiprocessing.Process(target=fit_average_2pcf, args=args)
                #process_list.append(p)
                #p.start()
                #p.join()
                fit_average_2pcf(*args)
                print(f"DONE")
                counter+=1
                #exit(0) 
            #for p in process_list:
            #    p.join()
    #pool.close()
    #pool.join()
