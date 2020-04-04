#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *


def comp_mask_catalog(fn, odir, sigma_noise=0.2, function=parabola,\
			cmin=0.8, names = ['x', 'y', 'z'], N_grid=2500, \
			noise_sampler=noise_sampler, rmin=16, rmax=50, \
			cat_type='mock'):
    print(f"==> Using function {function.__name__}")
    print(f"==> Using min. completeness {cmin}")
    complete_command='module load spack/default  gcc/5.4.0 boost\n'
    # Create data catalog with mask
    fn_base = os.path.basename(fn)
    oname_gal = fn_base.replace('.dat',\
	 f".{function.__name__}.sigma{sigma_noise}.dat")
    oname_gal_noise = os.path.join(odir,\
	 f"noise/{function.__name__}_{cmin}/{cat_type}s_gal_xyz/{oname_gal}")
    oname_gal_smooth = os.path.join(odir,\
	 f"smooth/{function.__name__}_{cmin}/{cat_type}s_gal_xyz/{oname_gal.replace('sigma'+str(sigma_noise), 'sigma0.0')}")
    onames = [oname_gal_smooth, oname_gal_noise]
    obases = [os.path.join(odir, \
	 s,f"{function.__name__}_{cmin}") for s in ['smooth', 'noise']]
    conf_file_gal = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%SPACE
    conf_file_void = WORKDIR+"/src/fcfc_box/fcfc_box_void_count_%s.conf"%SPACE
    joblist=open('joblist.sh', 'w')
    for i , on in enumerate(onames):
        write_void=False #So they are not recomputed in reruns
        if not os.path.exists(on):
            write_void = True #In case of error, in galaxies, overwrite voids too.
            data = pd.read_csv(fn, delim_whitespace = True, \
				usecols=(0, 1, 2), names = names)
            os.makedirs(os.path.dirname(on), exist_ok=True)
            print(f"Creating {on}")
            mask_function = lambda y, x: function(y, x, N_grid, cmin)
            if noise_sampler is not None:
                nsampler = lambda n_samples: noise_sampler(sigma_noise, n_samples)
            else:
                nsampler=None
            masked_dat = mask_with_function(data, mask_function,\
					 noise=bool(i), box_size=2500,\
					 N_grid=N_grid, sigma_noise=sigma_noise,\
					 cmin=0, noise_sampler=nsampler)
            masked_dat.to_csv(on, sep = ' ', header=False, index=False)

        print(f"==> WARNING: Saving voids in 'nearest' directory")
        oname_void = [os.path.join(obases[i],\
			 f"{cat_type}s_void_xyz",\
			 os.path.basename(on).replace('.dat', f".VOID.dat")), \
			 os.path.join(obases[i], 
			 f"{cat_type}s_void_xyz_wt_nearest",\
			 os.path.basename(on).replace('.dat', f".VOID.dat"))]
        [os.makedirs(os.path.dirname(oname_void[i]), exist_ok=True) for i in range(2)]
        dive_command = f"{RUN_DIVE} {on} {oname_void[0]} {box_size} 0 999\n"
        if not os.path.exists(oname_void[0]) or write_void:
            joblist.write(dive_command)
            complete_command+=dive_command

        # Define files for fcfc
        tpcf_gal_dirs = [obases[i]+f"/tpcf_gal_{cat_type}_nowt", \
			obases[i]+f"/tpcf_gal_{cat_type}"]
        tpcf_void_dirs = [obases[i]+f"/tpcf_void_{cat_type}_nowt_R-{rmin}-{rmax}", \
			obases[i]+f"/tpcf_void_{cat_type}_R-{rmin}-{rmax}"]
        tpcf_xgv_dirs = [obases[i]+f"/tpcf_xgv_{cat_type}_vnw_gnw_R-{rmin}-{rmax}", \
			obases[i]+f"/tpcf_xgv_{cat_type}_vnw_gw_R-{rmin}-{rmax}", \
			obases[i]+f"/tpcf_xgv_{cat_type}_vw_gnw_R-{rmin}-{rmax}", \
			obases[i]+f"/tpcf_xgv_{cat_type}_vw_gw_R-{rmin}-{rmax}"]
        data_wt_cols_gal= [0, 4]
        data_wt_cols_void= [0, 5]
        for weight in [0,1]:
            os.makedirs(tpcf_gal_dirs[weight]+"/DD_files", exist_ok=True)
            dd_file_gal = os.path.join(tpcf_gal_dirs[weight],"DD_files",\
					"DD_"+os.path.basename(on))
            out_file_gal = os.path.join(tpcf_gal_dirs[weight],\
					 "TwoPCF_"+os.path.basename(on))
            data_wt_col=data_wt_cols_gal[weight]
            if not os.path.exists(dd_file_gal):
                count_mode=1
                ncores = NCORES
                fcfc_gal_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_gal} --data={on} --count-mode={count_mode} --dd={dd_file_gal} --output={out_file_gal} --data-wt-col={data_wt_col} --cf-mode=3\n"
            else:
                ncores=1
                count_mode=0
                fcfc_gal_command = f"{WORKDIR}/bin/2pcf.py {dd_file_gal} {out_file_gal}\n"
            joblist.write(fcfc_gal_command)    
            complete_command+=fcfc_gal_command
            
            
            # For voids
#            if weight==0: #Remove this condition to implement void weights
            if not os.path.isfile(oname_void[weight]): 
                continue; print(f"==> File {oname_void[weight]} does not exist.")
            os.makedirs(tpcf_void_dirs[weight]+"/DD_files", exist_ok=True)
            dd_file_void = os.path.join(tpcf_void_dirs[weight],"DD_files",\
		"DD_"+os.path.basename(oname_void[weight]).replace('.dat',\
							f".R-{rmin}-{rmax}.dat"))
            out_file_void = os.path.join(tpcf_void_dirs[weight],\
		 "TwoPCF_"+os.path.basename(oname_void[weight]).replace('.dat',\
							f".R-{rmin}-{rmax}.dat"))
            data_wt_col=data_wt_cols_void[weight]
            if not os.path.exists(dd_file_void):
                count_mode=1
                ncores = NCORES
                fcfc_void_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --data={oname_void[weight]} --count-mode={count_mode} --dd={dd_file_void} --output={out_file_void} --data-wt-col={data_wt_col} --data-aux-col=4 --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode=3\n"
            else:
                ncores=1
                count_mode=0
                fcfc_void_command = f"{WORKDIR}/bin/2pcf.py {dd_file_void} {out_file_void}\n"
            joblist.write(fcfc_void_command)    
            complete_command+=fcfc_void_command
             # Compute cross-terms
            for weight_gal in [0,1]:
                id_ = np.ravel_multi_index((weight, weight_gal), (2,2))
                os.makedirs(tpcf_xgv_dirs[id_]+"/DD_files", exist_ok=True)
                dgdv_file = os.path.join(tpcf_xgv_dirs[id_], "DD_files", \
			"DD_"+os.path.basename(on).replace('.dat', \
						f".CROSS.R_{rmin}-{rmax}.dat"))
                out_file_xgv = os.path.join(tpcf_xgv_dirs[id_],\
			"TwoPCF_"+os.path.basename(on).replace('.dat', \
						f".CROSS.R_{rmin}-{rmax}.dat"))
                if not os.path.exists(dgdv_file):
                    count_mode=2
                    ncores = NCORES
                    fcfc_cross_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --rand={on} --data={oname_void[weight]} --count-mode={count_mode} --dr={dgdv_file} --output={out_file_xgv} --data-wt-col={data_wt_cols_void[weight]} --rand-wt-col={data_wt_cols_gal[weight_gal]} --data-aux-col=4 --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode=0 && {WORKDIR}/bin/2pcf.py {dgdv_file} {out_file_xgv}\n"
                else:
                    ncores=1
                    fcfc_cross_command = f"{WORKDIR}/bin/2pcf.py {dgdv_file} {out_file_xgv}\n"
                joblist.write(fcfc_cross_command)    
                complete_command+=fcfc_cross_command
      

    joblist.close()
    return complete_command
if __name__ == '__main__':
    from mpi4py import MPI

    nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
    iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
    inode = MPI.Get_processor_name()    # Node where this MPI process runs
    if len(sys.argv) > 3 or len(sys.argv)<2:
        sys.exit(f"ERROR: Unexpected number of arguments\nUSAGE: {sys.argv[0]} INDIR MIN_COMP")
    indir = sys.argv[1]
    try:
        cmin_map = float(sys.argv[2])
        print(f"==> Using completeness from command line = {cmin_map}.")
    except:
        print(f"==> Using completeness from params.py file.")
    filenames = [os.path.join(indir, f) for f in os.listdir(indir)][:NMOCKS]
    filenames_split = np.array_split(filenames, nproc)
    joblist = open(f"joblists/jobs_{SPACE}_{FUNCTION.__name__}_{cmin_map}_{iproc}.sh", 'w')
    for f in filenames_split[iproc]:
        odir = os.path.abspath(os.path.dirname(f)+'/../..')
        command=comp_mask_catalog(f, odir, noise_sampler=noise_sampler, \
				function = FUNCTION, cmin = cmin_map, \
				N_grid = 2500, rmin = 16, rmax = 50, \
				sigma_noise=0.2)
        joblist.write(command)
    joblist.close()
    MPI.Finalize()
