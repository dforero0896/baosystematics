#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_radial_gauss
from params import *


def radial_mask_catalog(fn, odir, sigma=0.235, center=0.5,\
			names = ['x', 'y', 'z'], N_grid=2500, \
			rmin=RMIN, rmax=RMAX, \
			cat_type='mock', use_scaled_r=0, scaled_rmin=None,\
			scaled_rmax=None, space=SPACE, crosscorr=False,\
			weight2pcf=False, overwrite=False, isfirst=True):
    complete_command='module load spack/default  gcc/5.4.0 boost\n'
    # Create data catalog with mask
    fn_base = os.path.basename(fn)
    oname_gal = fn_base.replace('.dat',\
	 f".radialgauss.sigma{sigma}.dat")
    oname_gal_radial = os.path.join(odir,\
	 f"radialgauss/{cat_type}s_gal_xyz/{oname_gal}")
    onames = [oname_gal_radial]
    obases = [os.path.join(odir, f"radialgauss")]
    conf_file_gal = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%space
    conf_file_void = WORKDIR+"/src/fcfc_box/fcfc_box_void_count_%s.conf"%space
    random_mask=f"{WORKDIR}/patchy_results/randoms/box_uniform_random_seed1_0-2500.radialgauss.sigma0.235.dat"
    rr_file_mask = os.path.join(os.path.dirname(random_mask), 'RR_'+os.path.basename(random_mask))
    random_shuf=f"{obases[0]}/void_ran/void_ran.dat"
    rr_file_shuf = os.path.join(os.path.dirname(random_shuf), 'RR_'+os.path.basename(random_shuf))
    joblist=open('joblist.sh', 'w')
    for i , on in enumerate(onames):
        write_void=False #So they are not recomputed in reruns
        if not os.path.exists(on):
            write_void = True #In case of error, in galaxies, overwrite voids too.
            data = pd.read_csv(fn, delim_whitespace = True, \
				usecols=(0, 1, 2), names = names)
            os.makedirs(os.path.dirname(on), exist_ok=True)
            print(f"Creating {on}")
            masked_dat = mask_radial_gauss(data, seed=2,\
					 box_size=2500,\
					 N_grid=N_grid, sigma=sigma,\
					 center=center)
            masked_dat.to_csv(on, sep = ' ', header=False, index=False)
        #print(f"==> WARNING: Saving voids in 'nearest' directory")
        #This line should be changed if we wish to have selection wrt rescaled radii
        oname_void = [os.path.join(obases[i],\
			 f"{cat_type}s_void_xyz",\
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
        if use_scaled_r == 0 :
            rmin_fid = rmin 
            rmax_fid = rmax 
            void_aux_col=4
        elif use_scaled_r==1 :
            N_gal_incomp = line_count(on)
            n_gal_incomp = get_average_galaxy_density(N_gal_incomp)
            print(f"==> Using scaled R min = {scaled_rmin}")
            print(f"==> rmin param. is ignored")
            rmin = np.round(scaled_rmin / (n_gal_incomp)**(1./3), 2)
            rmin_fid = f"scaled{scaled_rmin}"
            rmax_fid = rmax 
            void_aux_col=4
        elif use_scaled_r==2:
            print(f"==> Using scaled R in ({scaled_rmin}, {scaled_rmax})")
            print(f"==> rmin, rmax params are ignored")
            rmin = scaled_rmin
            rmax = scaled_rmax
            rmin_fid = f"loc_scaled{scaled_rmin}"
            rmax_fid = f"loc_scaled{scaled_rmax}" 
            void_aux_col=6
            oname_void[0] = oname_void[0].replace('void_xyz', 'void_xyz_scaledR')
            if not weight2pcf: void_aux_col-=1
        else: 
            raise(NotImplementedError(f"Value {use_scaled_r} not understood."))
        print(f"==> Using radius range [{rmin}, {rmax}]")
        # Define files for fcfc
        cf_mode=2
        rr_file_shuf = rr_file_shuf.replace('.dat',f"R-{rmin_fid}-{rmax_fid}.dat") 
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
            if weight==1 and not weight2pcf: continue
            os.makedirs(tpcf_gal_dirs[weight]+"/DD_files", exist_ok=True)
            os.makedirs(tpcf_gal_dirs[weight]+"/DR_files", exist_ok=True)
            dd_file_gal = os.path.join(tpcf_gal_dirs[weight],"DD_files",\
					"DD_"+os.path.basename(on))
            dr_file_gal = os.path.join(tpcf_gal_dirs[weight],"DR_files",\
					"DR_"+os.path.basename(on))
            out_file_gal = os.path.join(tpcf_gal_dirs[weight],\
					 "TwoPCF_"+os.path.basename(on))
            data_wt_col=data_wt_cols_gal[weight]
            if not os.path.exists(rr_file_mask) and isfirst:
                count_mode=5#7
                ncores = NCORES
                fcfc_gal_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_gal} --data={on} --rand={random_mask} --count-mode={count_mode} --dd={dd_file_gal} --dr={dr_file_gal} --rr={rr_file_mask} --output={out_file_gal} --data-wt-col={data_wt_col} --cf-mode={cf_mode}\n"
            else:
                ncores=NCORES
                count_mode=1#3
                fcfc_gal_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_gal} --data={on} --rand={random_mask} --count-mode={count_mode} --dd={dd_file_gal} --dr={dr_file_gal} --rr={rr_file_mask} --output={out_file_gal} --data-wt-col={data_wt_col} --cf-mode={cf_mode}\n"
            if not os.path.exists(out_file_gal) or overwrite:
                joblist.write(fcfc_gal_command)    
                complete_command+=fcfc_gal_command
            
            
            # For voids
#            if weight==0: #Remove this condition to implement void weights
        #    if not os.path.isfile(oname_void[weight]): 
        #        continue; print(f"==> File {oname_void[weight]} does not exist.")
            os.makedirs(tpcf_void_dirs[weight]+"/DD_files", exist_ok=True)
            os.makedirs(tpcf_void_dirs[weight]+"/DR_files", exist_ok=True)
            dd_file_void = os.path.join(tpcf_void_dirs[weight],"DD_files",\
		"DD_"+os.path.basename(oname_void[weight]).replace('.dat',\
						f".R-{rmin_fid}-{rmax_fid}.dat"))
            dr_file_void = os.path.join(tpcf_void_dirs[weight],"DR_files",\
		"DR_"+os.path.basename(oname_void[weight]).replace('.dat',\
						f".R-{rmin_fid}-{rmax_fid}.dat"))
            out_file_void = os.path.join(tpcf_void_dirs[weight],\
		 "TwoPCF_"+os.path.basename(oname_void[weight]).replace('.dat',\
						f".R-{rmin_fid}-{rmax_fid}.dat"))
            data_wt_col=data_wt_cols_void[weight]
            if  not os.path.exists(rr_file_shuf) and isfirst:
                count_mode=5#7
                ncores = NCORES
                fcfc_void_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --data={oname_void[weight]} --rand={random_shuf} --count-mode={count_mode} --dd={dd_file_void} --dr={dr_file_void} --rr={rr_file_shuf} --output={out_file_void} --data-wt-col={data_wt_col} --data-aux-col={void_aux_col} --data-aux-min={rmin} --data-aux-max={rmax} --rand-aux-col={void_aux_col} --rand-aux-min={rmin} --rand-aux-max={rmax} --rand-select=23 --cf-mode={cf_mode}\n"
            else:
                ncores=NCORES
                count_mode=1#3
                fcfc_void_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --data={oname_void[weight]} --rand={random_shuf} --count-mode={count_mode} --dd={dd_file_void} --dr={dr_file_void} --rr={rr_file_shuf} --output={out_file_void} --data-wt-col={data_wt_col} --data-aux-col={void_aux_col} --data-aux-min={rmin} --data-aux-max={rmax} --rand-aux-col={void_aux_col} --rand-aux-min={rmin} --rand-aux-max={rmax} --rand-select=23 --cf-mode={cf_mode}\n"
            if not os.path.exists(out_file_void) or overwrite:
                joblist.write(fcfc_void_command)    
                complete_command+=fcfc_void_command
             # Compute cross-terms
            for weight_gal in [0,1]:
                if weight_gal==1 and not weight2pcf: continue
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
                    fcfc_cross_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --rand={on} --data={oname_void[weight]} --count-mode={count_mode} --dr={dgdv_file} --output={out_file_xgv} --data-wt-col={data_wt_cols_void[weight]} --rand-wt-col={data_wt_cols_gal[weight_gal]} --data-aux-col={void_aux_col} --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode=0\n"
                else:
                    ncores=1
                    fcfc_cross_command = f"{WORKDIR}/bin/2pcf.py {dgdv_file} {out_file_xgv}\n"
                joblist.write(fcfc_cross_command)    
                if crosscorr:
                    complete_command+=fcfc_cross_command
      

    joblist.close()
    return complete_command
if __name__ == '__main__':
    from mpi4py import MPI

    nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
    iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
    inode = MPI.Get_processor_name()    # Node where this MPI process runs
    if len(sys.argv) > 4 or len(sys.argv)<2:
        sys.exit(f"ERROR: Unexpected number of arguments\nUSAGE: {sys.argv[0]} INDIR [BOX SPACE]")
    indir = sys.argv[1]
    try:
        box = sys.argv[2]
        space = sys.argv[3]
        print(f"==> Using params from command line: box={box}, space={space}.")
    except IndexError:
        box=BOX
        space=SPACE
        print(f"==> Using params from params.py file: box={box}, space={space}.")
    filenames = [os.path.join(indir, f) for f in os.listdir(indir)][:NMOCKS]
    filenames_split = np.array_split(filenames, nproc)
    joblist = open(f"joblists/jobs_{space}_radialgauss_{iproc}_box{box}.sh", 'w')

    for i, f in enumerate(filenames_split[iproc]):
        odir = os.path.abspath(os.path.dirname(f)+'/../..')
        command=radial_mask_catalog(f, odir, N_grid = NGRID, rmin = RMIN, rmax = RMAX, \
				sigma=0.235, center = 0.5, use_scaled_r=USE_SCALED_R,\
				scaled_rmin=SCALED_RMIN, scaled_rmax=SCALED_RMAX,\
				space=space, overwrite=False, isfirst=i==0)
        joblist.write(command)
    joblist.close()
    MPI.COMM_WORLD.Barrier()
    if iproc == 0:
        from save_spatial_densities import mp_save_radial_density
        mp_save_radial_density(f"{odir}/radialgauss/mocks_gal_xyz")
    MPI.Finalize()
