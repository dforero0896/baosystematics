#!/usr/bin/env python
import sys
import os
import pandas as pd
import numpy as np
from mask_comp_func import mask_with_function
from params import *


def comp_mask_catalog(fn, odir, sigma_noise=0.2, function=parabola, cmin=0.8, names = ['x', 'y', 'z'], N_grid=2500, noise_sampler=noise_sampler, rmin=16, rmax=50):
    complete_command=''
    # Create data catalog with mask
    fn_base = os.path.basename(fn)
    oname_gal = fn_base.replace('.dat', f".{function.__name__}.sigma{sigma_noise}.dat")
    oname_gal_noise = os.path.join(odir, f"noise/{function.__name__}/mocks_gal_xyz/{oname_gal}")
    oname_gal_smooth = os.path.join(odir, f"smooth/{function.__name__}/mocks_gal_xyz/{oname_gal.replace(str(sigma_noise), '0.0')}")
    onames = [oname_gal_smooth, oname_gal_noise]
    obases = [os.path.join(odir, s,f"{function.__name__}") for s in ['smooth', 'noise']]
    conf_file_gal = WORKDIR+"/src/fcfc_box/fcfc_box_count_%s.conf"%SPACE
    conf_file_void = WORKDIR+"/src/fcfc_box/fcfc_box_void_count_%s.conf"%SPACE
    joblist=open('joblist.sh', 'w')
    for i , on in enumerate(onames):
        write_void=False #So they are not recomputed in reruns
        if not os.path.exists(on):
            write_void = True #In case of error, in galaxies, overwrite voids too.
            data = pd.read_csv(fn, delim_whitespace = True, usecols=(0, 1, 2), names = names)
            os.makedirs(os.path.dirname(on), exist_ok=True)
            print(f"Creating {on}")
            mask_function = lambda y, x: function(y, x, N_grid, cmin)
            if noise_sampler is not None:
                nsampler = lambda n_samples: noise_sampler(sigma_noise, n_samples)
            else:
                nsampler=None
            masked_dat = mask_with_function(data, mask_function, noise=bool(i), box_size=2500, N_grid=N_grid, sigma_noise=sigma_noise, cmin=0, noise_sampler=nsampler)
            masked_dat.to_csv(on, sep = ' ', header=False, index=False)

        oname_void = os.path.join(obases[i], 'mocks_void_xyz', os.path.basename(on).replace('.dat', f".VOID.dat"))
        os.makedirs(os.path.dirname(oname_void), exist_ok=True)
        dive_command = f"{RUN_DIVE} {on} {oname_void} {box_size} 0 999\n"
        if not os.path.exists(oname_void) or write_void:
            joblist.write(dive_command)
            complete_command+=dive_command

        # Define files for fcfc
        tpcf_gal_dirs = [obases[i]+f"/tpcf_gal_mock_nowt", obases[i]+f"/tpcf_gal_mock"]
        data_wt_cols_gal= [0, 4]
        tpcf_void_dirs = [obases[i]+f"/tpcf_void_mock_nowt", obases[i]+f"/tpcf_void_mock"]
        data_wt_cols_gal= [0, 4]
        data_wt_cols_void= [0, 5]
        for weight in [0,1]:
            os.makedirs(tpcf_gal_dirs[weight]+"/DD_files", exist_ok=True)
            dd_file_gal = os.path.join(tpcf_gal_dirs[weight],"DD_files","DD_"+os.path.basename(on))
            out_file_gal = os.path.join(tpcf_gal_dirs[weight], "TwoPCF_"+os.path.basename(on))
            if not os.path.exists(dd_file_gal):
                count_mode=1
                ncores = NCORES
            else:
                ncores=1
                count_mode=0
            data_wt_col=data_wt_cols_gal[weight]
            fcfc_gal_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_gal} --data={on} --count-mode={count_mode} --dd={dd_file_gal} --output={out_file_gal} --data-wt-col={data_wt_col} --cf-mode=3\n"
            joblist.write(fcfc_gal_command)    
            complete_command+=fcfc_gal_command
            # For voids
            if weight==0:
                os.makedirs(tpcf_void_dirs[weight]+"/DD_files", exist_ok=True)
                dd_file_void = os.path.join(tpcf_void_dirs[weight],"DD_files","DD_"+os.path.basename(oname_void))
                out_file_void = os.path.join(tpcf_void_dirs[weight], "TwoPCF_"+os.path.basename(oname_void).replace('.dat', f".R-{rmin}-{rmax}.dat"))
                if not os.path.exists(dd_file_void):
                    count_mode=1
                    ncores = NCORES
                else:
                    ncores=1
                    count_mode=0
                data_wt_col=data_wt_cols_void[weight]
                fcfc_void_command = f"srun -n 1 -c {ncores} {RUN_FCFC} --conf={conf_file_void} --data={oname_void} --count-mode={count_mode} --dd={dd_file_void} --output={out_file_void} --data-wt-col={data_wt_col} --data-aux-col=4 --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode=3\n"
                joblist.write(fcfc_void_command)    
                complete_command+=fcfc_void_command
    joblist.close()
    return complete_command
if __name__ == '__main__':
    from mpi4py import MPI

    nproc = MPI.COMM_WORLD.Get_size()   # Size of communicator
    iproc = MPI.COMM_WORLD.Get_rank()   # Ranks in communicator
    inode = MPI.Get_processor_name()    # Node where this MPI process runs
    if len(sys.argv) != 2:
        sys.exit(f"ERROR: Unexpected number of arguments\nUSAGE: {sys.argv[0]} INDIR")
    indir = sys.argv[1]
    filenames = [os.path.join(indir, f) for f in os.listdir(indir)]
    filenames_split = np.array_split(filenames, nproc)
    joblist = open(f"jobs_{SPACE}_{iproc}.sh", 'w')
    for f in filenames_split[iproc]:
        odir = os.path.abspath(os.path.dirname(f)+'/../..')
        command=comp_mask_catalog(f, odir, noise_sampler=noise_sampler)
        joblist.write(command)
    joblist.close()
    MPI.Finalize()
