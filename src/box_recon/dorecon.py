import os
import sys
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.getenv("WORKDIR")
sys.path.append(f"{WORKDIR}/bin/Revolver")
import argparse
import time
import numpy as np
from python_tools.galaxycat import GalaxyCatalogue
from python_tools.recon import Recon
from python_tools.fastmodules import survey_cuts_logical



# ==== Read in settings ==== #
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-p', '--par', dest='par', default="", help='path to parameter file.', required=True)
parser.add_argument('-han-d', '--handle', dest='handle', help='string to identify the run; used to set filenames.')
parser.add_argument('-han-r', '--handle-ran', dest='handle_ran', help='string to identify the run; used to set filenames.')
parser.add_argument('-o', '--output-folder', dest='output_folder', help="/path/to/folder/ where output should be placed.")
parser.add_argument('-t', '--tracer-file', dest='tracer_file', help="Path to tracer file.")
parser.add_argument('-r', '--random-file', dest='random_file', help="Path to random file.")
parser.add_argument('-f', '--f', dest="f", help="Linear growth rate at the mean redshift.", type=float)
parser.add_argument('-b', '--bias', dest="bias", help="Linear tracer bias.", type=float)
args = parser.parse_args()


# user-provided settings
filename = args.par
if os.access(filename, os.F_OK):
    print('Loading parameters from %s' % filename)
    if sys.version_info.major <= 2:
        import imp
        parms = imp.load_source("name", filename)
    elif sys.version_info.major == 3 and sys.version_info.minor <= 4:
        from importlib.machinery import SourceFileLoader
        parms = SourceFileLoader("name", filename).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location("name", filename)
        parms = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parms)
else:
    sys.exit('Did not find settings file %s, aborting' % filename)
# Override config file with command line options

for name in vars(args):
    if args.__dict__[name] is not None:
        if name == 'tracer_file':
            print("==> Tracer file provided via CL, overriding handles.")
            handle_dat = os.path.splitext(os.path.basename(args.__dict__[name]))[0]
            handle_ran = handle_dat+'.ran'
            parms.__dict__['handle'] = handle_dat
            parms.__dict__['handle_ran'] = handle_ran
        parms.__dict__[name] = args.__dict__[name]
for name in vars(args):
    print(f"{name}:\t{parms.__dict__[name]}")





# === check output path === #
if not os.access(parms.output_folder, os.F_OK):
    os.makedirs(parms.output_folder)
# ========================= #

# ==== run reconstruction ==== #
if parms.do_recon:
    print('\n ==== Running reconstruction for real-space positions ==== ')

    cat = GalaxyCatalogue(parms, randoms=False)

    if parms.random_file == '':
        recon = Recon(cat, ran=None, parms=parms)
    else:
        print("==> Found random filename, using randoms.")
        if not os.access(parms.random_file, os.F_OK):
            sys.exit('ERROR: randoms data required for reconstruction but randoms file not provided or not found!' +
                     'Aborting.')

        # initializing randoms
        ran = GalaxyCatalogue(parms, randoms=True)
        if not parms.is_box:
            # perform basic cuts on the data: vetomask and low redshift extent if survey
            wgal = np.empty(cat.size, dtype=int)
            survey_cuts_logical(wgal, cat.veto, cat.redshift, parms.z_low_cut, parms.z_high_cut)
            wgal = np.asarray(wgal, dtype=bool)
            wran = np.empty(ran.size, dtype=int)
            survey_cuts_logical(wran, ran.veto, ran.redshift, parms.z_low_cut, parms.z_high_cut)
            wran = np.asarray(wran, dtype=bool)
            cat.cut(wgal)
            ran.cut(wran)

        recon = Recon(cat, ran, parms)

    start = time.time()
    # now run the iteration loop to solve for displacement field
    
    for i in range(parms.niter):
        recon.iterate(i, debug=parms.debug)

    # get new ra, dec and redshift for real-space positions
    
    if not parms.is_box:
        cat.ra, cat.dec, cat.redshift = recon.get_new_radecz(recon.cat)

    #recon.summary()    
    print("==> Applying shifts") 
    recon.apply_shifts_full()    
    #recon.summary()    
    # save real-space positions to file
    root = parms.output_folder + parms.handle + '_pos'
    root2 = parms.output_folder + parms.handle_ran + '_pos'
    recon.export_shift_pos(root, root2=root2, rsd_only=False)

    print(" ==== Done reconstruction ====\n")
    end = time.time()
    print("Reconstruction took %0.3f seconds" % (end - start))

