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
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

dr = [0.7, 0.75, 0.8, 0.87, 0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
#dr = [0.93, 1.0, 1.07, 1.13, 1.18, 1.19, 1.25, 1.33]
comps = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
nthreads = 1
def fit_average_2pcf(ifile, mocks, plin, pnw, ptemp, outdir, symlinkid):
    long_path = (len(outdir) > 80)
    parameters = ['alpha', 'B_v', 'Snl_vv']
    nparams=len(parameters)
    base = os.path.basename(ifile).replace("tpcf_void_mock_nowt_", "")
    print(f"Using mocks, {mocks}", flush=True)
    mock_file = tempfile.NamedTemporaryFile(mode='w+t', delete=True)
    data =[]
    for mock in glob.glob(f"{mocks}/TwoPCF*"):
        data.append(np.loadtxt(mock, usecols=(1,))) 
        mock_file.writelines(f"{mock}\n")
        mock_file.flush()
    mock_file.seek(0)

    s_obs, xi_obs, std = np.loadtxt(ifile, usecols=(0, 1, 2), unpack=True) 
    resume="F"
    subprocess.check_call([f"{WORKDIR}/bin/BAOflit/BAOflit", f"--conf={WORKDIR}/src/baofit/baoflit.conf", f"--data=[{ifile}]", f"--mock=[{mock_file.name}]", f"--pk-lin={plin}", f"--pk-nw={pnw}", f"--pk-tracer={ptemp}", f"--output={outdir}/{base}_", f"--cov={outdir}/{base}_cov.dat", f"--resume={resume}"])
    mock_file.close()
    s_best, xi_best = np.loadtxt(f"{outdir}/{base}_bestfit.dat", usecols=(0, 1), unpack=True) 
    s_map, xi_map = np.loadtxt(f"{outdir}/{base}_model_map.dat", usecols=(0, 1), unpack=True) 
    s_maxl, xi_maxl = np.loadtxt(f"{outdir}/{base}_model_maxlike.dat", usecols=(0, 1), unpack=True) 
    s_mean, xi_mean = np.loadtxt(f"{outdir}/{base}_model_mean.dat", usecols=(0, 1), unpack=True) 

    fig, ax = plt.subplots(1, 1)
    ax.errorbar(s_obs, s_obs**2*xi_obs,yerr=s_obs**2*std, label="Data")
    #ax.plot(s_best, s_best**2*xi_best, label="Best fit")
    ax.plot(s_map, s_map**2*xi_map, label="MAP fit")
    ax.plot(s_maxl, s_maxl**2*xi_maxl, label="MaxLike fit")
    ax.plot(s_mean, s_mean**2*xi_mean, label="Mean fit")
    ax.legend(loc=0)

    fig.savefig(f"{outdir}/{base}_bestfit.pdf", dpi=200)
    print(f"==> Saved bestfit plot in {outdir}/{base}_bestfit.pdf", flush=True)
    plt.close(fig)
    import pymultinest as pmn
    res = pmn.Analyzer(outputfiles_basename=f"{outdir}/{base}_", n_params=nparams)
    bestpar = res.get_best_fit()['parameters']
    print(bestpar)
    stats = res.get_stats()['marginals']
    p = pmn.PlotMarginalModes(res)
    fig = plt.figure(figsize=(5*nparams, 5*nparams))
    olist = []
    for i in range(nparams):
        median = stats[i]['median']
        onesigma = stats[i]['1sigma']
        low = median - onesigma[0]
        high = onesigma[1] - median
        olist.append(median)
        olist.append(stats[i]['sigma'])
        plt.subplot(nparams, nparams, nparams * i + i + 1)
        p.plot_marginal(i, with_ellipses = True, with_points = False, grid_points=50)
        
        plt.title(f"${parameters[i]} = {stats[i]['median']:.4f}_{{-{low:.4f}}}^{{-{high:.4f}}}$")
        plt.ylabel("Probability")
        plt.xlabel(parameters[i])

        for j in range(i):
            plt.subplot(nparams, nparams, nparams * j + i + 1)
            p.plot_conditional(i, j, with_ellipses = False, with_points = True, grid_points=30)
            plt.xlabel(parameters[i])
            plt.ylabel(parameters[j])
            plt.savefig(f"{outdir}/{base}_multinest_marginals_post.pdf") #, bbox_inches='tight')
    fig.clear()
    plt.close(fig)
    return bestpar
 
if __name__ == '__main__':
    plin = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Plin.dat"
    pnw = f"{WORKDIR}/bin/2pcf_bao_fitter/data/Albert_Pnw.dat"
    counter = 1

    #pool = multiprocessing.Pool(processes = nthreads)
    for rec in ['patchy_results', 'patchy_recon_nods']:

        main_path = f"{WORKDIR}/{rec}/box1/redshift/smooth/"

        avg_tpcf_dir = f"{main_path}/tpcf_avg"

        process_list = []
        for r in dr:
            for comp in comps:
                ifile_list = glob.glob(f"{avg_tpcf_dir}/*flat_{comp}_*scaled{r}-*ascii")
                mockdir_list = glob.glob(f"{main_path}/flat_{comp}/tpcf_void_mock_nowt_R-scaled*{r}-*/")
                
                if len(mockdir_list)>1: print(mockdir_list)
                #exit(0)
                template_list = glob.glob(f"{WORKDIR}/data/templates/templates/powspecFST*dr{r:.2f}*flat{comp:.2f}*N20*")
  
                if (len(ifile_list)==0) or (len(mockdir_list)==0) or (len(template_list)==0):
                    print(len(ifile_list), len(mockdir_list), len(template_list))
                    continue
                outdir = f"{main_path}/flat_{comp}/baofit/tpcf_void_mock_nowt_R-scaled{r}-50_AVG"
                os.makedirs(outdir, exist_ok=True)
                args = (ifile_list[0], mockdir_list[0], plin, pnw, template_list[0], outdir, counter)
                #pool.apply_async(fit_average_2pcf, args)
                #p = multiprocessing.Process(target=fit_average_2pcf, args=args)
                #process_list.append(p)
                #p.start()
                #p.join()
                fit_average_2pcf(*args)
                #print(f"DONE")
                counter+=1
                exit(0) 
            #for p in process_list:
            #    p.join()
    #pool.close()
    #pool.join()
