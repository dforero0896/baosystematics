#!/usr/bin/env python
import numpy as np
import os, sys, glob
from dotenv import load_dotenv
load_dotenv() 
WORKDIR = os.getenv("WORKDIR") 
sys.path.append(f"{WORKDIR}/bin/2pcf_bao_fitter")
import multiprocessing
import subprocess
import tempfile
dr = [0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
#dr = [0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
comps = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
nthreads = 1
def fit_average_2pcf(ifile, mocks, plin, pnw, ptemp, outdir, symlinkid):
    long_path = (len(outdir) > 80)

    base = os.path.basename(ifile).replace("tpcf_void_mock_nowt_", "")

    mock_file = tempfile.NamedTemporaryFile(mode='w+t')
    for mock in mocks:
        mock_file.writelines(f"{mock}\n")
    mock_file.seek(0)
    s_obs, xi_obs = np.loadtxt(ifile, usecols=(0, 1), unpack=True) 
    resume="F"
    subprocess.check_call([f"{WORKDIR}/bin/BAOflit/BAOflit", f"--conf={WORKDIR}/src/baofit/baoflit.conf", f"--data=[{ifile}]", f"--mock=[{mock_file.name}]", f"--pk-lin={plin}", f"--pk-nw={pnw}", f"--pk-tracer={ptemp}", f"--output={outdir}/{os.path.basename(ifile)}_", f"--best-fit={outdir}/{os.path.basename(ifile)}_bestfit.dat", f"--cov={outdir}/{os.path.basename(ifile)}_cov.dat", f"--resume={resume}"])
    mock_file.close()
    s_best, xi_best = np.loadtxt(f"{outdir}/{os.path.basename(ifile)}_bestfit.dat", usecols=(0, 1), unpack=True) 

    fig, ax = plt.subplots(1, 1)
    ax.plot(s_obs, s_obs**2*xi_obs, label="Data")
    ax.plot(s_best, s_best**2*xi_obs, label="Best fit")
    ax.legend(loc=0)

    fig.savefig(f"{outdir}/{os.path.basename(ifile)}_bestfit.pdf", dpi=200)
    plt.close(fig)



if __name__ == '__main__':
    plin = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Plin.dat"
    pnw = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Pnw.dat"
    counter = 1

    pool = multiprocessing.Pool(processes = nthreads)
    for rec in ['patchy_results', 'patchy_recon_nods']:

        main_path = f"{WORKDIR}/{rec}/box1/redshift/smooth/"

        avg_tpcf_dir = f"{main_path}/tpcf_avg"

        process_list = []
        for r in dr:
            for comp in comps:
                ifile_list = glob.glob(f"{avg_tpcf_dir}/*flat_{comp}_*scaled{r}-*ascii")
                mockdir_list = glob.glob(f"{main_path}/flat_{comp}/tpcf_void_mock_nowt_R*{r}-*/")
                
                if len(mockdir_list)>1: print(mockdir_list); exit(0)
                #exit(0)
                template_list = glob.glob(f"{WORKDIR}/data/templates/templates/powspecFST*dr{r:.2f}*flat{comp:.2f}*N20*")
  
                if (len(ifile_list)==0) or (len(mockdir_list)==0) or (len(template_list)==0):
                    print(len(ifile_list), len(mockdir_list), len(template_list))
                    continue
                outdir = f"{main_path}/flat_{comp}/baofit/tpcf_void_mock_nowt_R-scaled{r}-50_AVG"
                os.makedirs(os.path.basename(outdir), exist_ok=True)
                os.makedirs(outdir, exist_ok=True)
                args = (ifile_list[0], mockdir_list[0], plin, pnw, template_list[0], outdir, counter)
                pool.apply_async(fit_average_2pcf, args)
                #p = multiprocessing.Process(target=fit_average_2pcf, args=args)
                #process_list.append(p)
                #p.start()
                #p.join()
                #fit_average_2pcf(*args)
                #print(f"DONE")
                counter+=1
                #exit(0) 
            #for p in process_list:
            #    p.join()
    pool.close()
    pool.join()
