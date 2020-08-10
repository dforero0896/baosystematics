#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *

def comp_mask_catalog(fn, odir, sigma_noise=0.2, function=parabola, cmin=0.8, names=['x', 'y', 'z'], N_grid=2500, seed=2, noise_sampler=noise_sampler, rmin=RMIN, rmax=RMAX, cat_type='mock', use_scaled_r=0, scaled_rmin=None, scaled_rmax=None, space=SPACE, isfirst=False, nu=1./4):
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
    conf_file_gal = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%space
    conf_file_void = WORKDIR+"/src/fcfc_box/fcfc_box_void_count_%s.conf"%space
    random_shuf=f"{obases[0]}/void_ran/void_ran.dat" # Not considering random for noise
    rr_file_shuf = os.path.join(os.path.dirname(random_shuf), 'RR_'+os.path.basename(random_shuf))
    joblist=open('joblist.sh', 'w')
    for i , on in enumerate(onames):
        if i==1: continue
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
					 cmin=0, noise_sampler=nsampler, seed=seed)
            masked_dat.to_csv(on, sep = ' ', header=False, index=False)
        #print(f"==> WARNING: Saving voids in 'nearest' directory")
        #This line should be changed if we wish to have selection wrt rescaled radii
        if use_scaled_r == 0 :
            rmin_fid = rmin 
            rmax_fid = rmax 
            void_aux_col=4
            void_dir_suffix=''
        elif use_scaled_r==1 :
            N_gal_incomp = line_count(on)
            n_gal_incomp = get_average_galaxy_density(N_gal_incomp)
            print(f"==> Using scaled R min = {scaled_rmin}")
            print(f"==> rmin param. is ignored")
            if N_gal_incomp==0: print(on);sys.exit(0)
            print(N_gal_incomp, scaled_rmin, n_gal_incomp)
            rmin = np.round(scaled_rmin / (n_gal_incomp)**(nu), 2)
            rmin_fid = f"scaled{scaled_rmin}"
            rmax_fid = rmax 
            void_aux_col=4
            void_dir_suffix=''
        elif use_scaled_r==2:
            print(f"==> Using scaled R in ({scaled_rmin}, {scaled_rmax})")
            print(f"==> rmin, rmax params are ignored")
            rmin = scaled_rmin
            rmax = scaled_rmax
            rmin_fid = f"loc_scaled{scaled_rmin}"
            rmax_fid = f"loc_scaled{scaled_rmax}" 
            void_aux_col=6
            void_dir_suffix='_wt_scaledR'
            rr_file_shuf = rr_file_shuf.replace('.dat',f"R-{rmin_fid}-{rmax_fid}.dat") 
        else: 
            raise(NotImplementedError(f"Value {use_scaled_r} not understood."))

        oname_void = [os.path.join(obases[i],\
			 f"{cat_type}s_void_xyz",\
			 #f"{cat_type}s_void_xyz_wt_scaledR",\
			 os.path.basename(on).replace('.dat', f".VOID.dat")), \
			 os.path.join(obases[i], 
			 f"{cat_type}s_void_xyz_wt_scaledR",\
			 os.path.basename(on).replace('.dat', f".VOID.dat"))]
        [os.makedirs(os.path.dirname(oname_void[i]), exist_ok=True) for i in range(2)]
        dive_command = f"{RUN_DIVE} {on} {oname_void[0]} {box_size} 0 999\n"
        # Write command to create void catalog
        if not os.path.exists(oname_void[0]) or write_void:
            joblist.write(dive_command)
            complete_command+=dive_command
        print(f"==> Using radius range [{rmin}, {rmax}]")
        # Define files for fcfc
        data_wt_cols_gal= [0, 4]
        data_wt_cols_void= [0, 5]
        tpcf_gal_dirs = [obases[i]+f"/tpcf_gal_{cat_type}_nowt", \
		obases[i]+f"/tpcf_gal_{cat_type}"]
        tpcf_void_dirs = [obases[i]+\
			f"/tpcf_void_{cat_type}_nowt_R-{rmin_fid}-{rmax_fid}", \
			obases[i]+\
			f"/tpcf_void_{cat_type}_R-{rmin_fid}-{rmax_fid}"]
        tpcf_xgv_dirs = [obases[i]+\
			f"/tpcf_xgv_{cat_type}_vnw_gnw_R-{rmin_fid}-{rmax_fid}", \
			obases[i]+\
			f"/tpcf_xgv_{cat_type}_vnw_gw_R-{rmin_fid}-{rmax_fid}", \
			obases[i]+\
			f"/tpcf_xgv_{cat_type}_vw_gnw_R-{rmin_fid}-{rmax_fid}", \
			obases[i]+\
			f"/tpcf_xgv_{cat_type}_vw_gw_R-{rmin_fid}-{rmax_fid}"]
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
                fcfc_gal_command = f"{WORKDIR}/bin/2pcf.py -dd {dd_file_gal} -o {out_file_gal}\n"
            joblist.write(fcfc_gal_command)    
            complete_command+=fcfc_gal_command
            
            
            # For voids
#            if weight==0: #Remove this condition to implement void weights
        #    if not os.path.isfile(oname_void[weight]): 
        #        continue; print(f"==> File {oname_void[weight]} does not exist.")
            os.makedirs(tpcf_void_dirs[weight]+"/DD_files", exist_ok=True)
            dd_file_void = os.path.join(tpcf_void_dirs[weight],"DD_files",\
		"DD_"+os.path.basename(oname_void[weight]).replace('.dat',\
						f".R-{rmin_fid}-{rmax_fid}.dat"))
            out_file_void = os.path.join(tpcf_void_dirs[weight],\
		 "TwoPCF_"+os.path.basename(oname_void[weight]).replace('.dat',\
						f".R-{rmin_fid}-{rmax_fid}.dat"))
            data_wt_col=data_wt_cols_void[weight]
            rr_file_shuf = rr_file_shuf.replace('.dat', f"_wt{weight}.dat")
            if not os.path.exists(dd_file_void):
                if use_scaled_r == 2:
                    if not os.path.exists(rr_file_shuf) and isfirst: 
                        count_mode = 4#5
                    else:
                        count_mode =0#1    
                    cf_mode = 2
                else:  count_mode=1; cf_mode=3
                ncores = NCORES
                fcfc_void_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --data={oname_void[weight]} --rand={random_shuf} --count-mode={count_mode} --dd={dd_file_void} --rr={rr_file_shuf} --output={out_file_void} --data-wt-col={data_wt_col} --rand-wt-col={data_wt_col} --data-aux-col={void_aux_col} --data-aux-min={rmin} --data-aux-max={rmax} --rand-aux-col={void_aux_col} --rand-aux-min={rmin} --rand-aux-max={rmax} --rand-select=23 --cf-mode={cf_mode}\n"
            else:
                ncores=1
                count_mode=0
                fcfc_void_command = f"{WORKDIR}/bin/2pcf.py -dd {dd_file_void} -o {out_file_void}\n"
            joblist.write(fcfc_void_command)    
            complete_command+=fcfc_void_command
             # Compute cross-terms
            for weight_gal in [0,1]:
                id_ = np.ravel_multi_index((weight, weight_gal), (2,2))
                os.makedirs(tpcf_xgv_dirs[id_]+"/DD_files", exist_ok=True)
                dgdv_file = os.path.join(tpcf_xgv_dirs[id_], "DD_files", \
			"DD_"+os.path.basename(on).replace('.dat', \
						f".CROSS.R_{rmin_fid}-{rmax_fid}.dat"))
                out_file_xgv = os.path.join(tpcf_xgv_dirs[id_],\
			"TwoPCF_"+os.path.basename(on).replace('.dat', \
						f".CROSS.R_{rmin_fid}-{rmax_fid}.dat"))
                if not os.path.exists(dgdv_file):
                    count_mode=2
                    ncores = NCORES
                    fcfc_cross_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --rand={on} --data={oname_void[weight]} --count-mode={count_mode} --dr={dgdv_file} --output={out_file_xgv} --data-wt-col={data_wt_cols_void[weight]} --rand-wt-col={data_wt_cols_gal[weight_gal]} --data-aux-col={void_aux_col} --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode=0 && {WORKDIR}/bin/2pcf.py -dd {dgdv_file} -o {out_file_xgv}\n"
                else:
                    ncores=1
                    fcfc_cross_command = f"{WORKDIR}/bin/2pcf.py -dd {dgdv_file} -o {out_file_xgv}\n"
                joblist.write(fcfc_cross_command)    
                complete_command+=fcfc_cross_command
      

    joblist.close()
    return complete_command
if __name__ == '__main__':
    import argparse
    from mpi4py import MPI
    from fractions import Fraction
    nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
    iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
    inode = MPI.Get_processor_name()    # Node where this MPI process runs
    parser = argparse.ArgumentParser()
    parser.add_argument("INDIR")
    parser.add_argument("-c", "--mincomp", required=False, help="Minimum completeness for the angular map.") 
    parser.add_argument("-b", "--box", required=False, help="Box to use: 1 or 5.") 
    parser.add_argument("-s", "--space", required=False, help="Space in which to compute: real or redshift.") 
    parser.add_argument("-r", "--scaledrmin", required=False, help="Scaled rmin value to use.")
    parser.add_argument("-nu", "--nu_exponent", required=False, help="Exponent of the galaxy density to rescale radii.")
    parsed = parser.parse_args()
    args = vars(parsed)
    indir = args['INDIR']
    comp_min = float(args['mincomp']) or cmin_map
    box = args['box'] or BOX
    RMIN=RMIN_DICT[box]
    space = args['space'] or SPACE
    scaled_rmin = args['scaledrmin'] or SCALED_RMIN
    scaled_rmin=float(scaled_rmin)
    nu_str = args['nu_exponent'] or "1/4"
    nu=float(Fraction(nu_str))
    print(parsed)
    print(f"==> Using params: box={box}, space={space} scaled_rmin={scaled_rmin}, nu={nu}.") 
    filenames = [os.path.join(indir, f) for f in os.listdir(indir)][:NMOCKS]
    filenames_split = np.array_split(filenames, nproc)
    joblist = open(f"joblists/jobs_{space}_{FUNCTION.__name__}_{comp_min}_{iproc}_box{box}_scaled_rmin{scaled_rmin}.sh", 'w')
#    seeds = np.array_split(np.arange(0, len(filenames)), nproc)
    seeds = np.array_split(2 * np.ones(len(filenames), dtype=int), nproc)
    for i,f in enumerate(filenames_split[iproc]):
        print(i, iproc)
        odir = os.path.abspath(os.path.dirname(f)+'/../..')
        command=comp_mask_catalog(f, odir, noise_sampler=noise_sampler, \
				function = FUNCTION, cmin = comp_min, \
				N_grid = NGRID, rmin = RMIN, rmax = RMAX, \
				sigma_noise=0.2, use_scaled_r=USE_SCALED_R,\
				scaled_rmin=scaled_rmin, scaled_rmax=SCALED_RMAX,\
				space=space, isfirst=i==0, seed = seeds[iproc][i], nu=nu)
        joblist.write(command)
    joblist.close()
    MPI.COMM_WORLD.Barrier()
    if iproc==0:
        from save_spatial_densities import mp_save_ang_density
        #if not os.path.exists(f"{odir}/noise/{FUNCTION.__name__}_{cmin_map}/plots"):
        #    mp_save_ang_density(f"{odir}/noise/{FUNCTION.__name__}_{cmin_map}/mocks_gal_xyz")
        if True:#not os.path.exists(f"{odir}/smooth/{FUNCTION.__name__}_{cmin_map}/plots"):
            mp_save_ang_density(f"{odir}/smooth/{FUNCTION.__name__}_{cmin_map}/mocks_gal_xyz")
    MPI.Finalize()
    
