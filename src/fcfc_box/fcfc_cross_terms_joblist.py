#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
load_dotenv()
WORKDIR = os.getenv('WORKDIR')
SRC = os.getenv('SRC')
BIN = os.getenv('BIN')
RUN = f"{BIN}/FCFC_box/2pcf"
CONFDIR = f"{SRC}/fcfc_box"
def fcfc_cross_gv_command(ncores, run, conf_file, galaxy_cat, void_cat, dr, output, void_wt_col, gal_wt_col, rmin, rmax, cf_mode=0, count_mode=2):

    return f"srun -n 1 -c {ncores} {run} --conf={os.path.realpath(conf_file)} --rand={os.path.realpath(galaxy_cat)} --data={os.path.realpath(void_cat)} --dr={os.path.realpath(dr)} --output={os.path.realpath(output)} --data-wt-col={void_wt_col} --rand-wt-col={gal_wt_col} --data-aux-col=4 --data-aux-min={rmin} --data-aux-max={rmax} --cf-mode={cf_mode} --count-mode={count_mode}"


if __name__ == '__main__':

    if len(sys.argv) != 4:
        sys.exit(f"USAGE: {sys.argv[0]} CONF_FILE GAL_CAT_LIST VOID_CAT_LIST")

    conf_file = sys.argv[1]
    gal_cats_list = sys.argv[2]
    void_cats_list = sys.argv[3]

    with open(gal_cats_list, 'r') as f:
        gal_cats = f.readlines()

    with open(void_cats_list, 'r') as f:
        void_cats = f.readlines()

    rmin = 16
    rmax = 50
    odir = os.path.dirname(void_cats[0].strip())+f"/../tpcf_xgv_R_{rmin}-{rmax}"
    os.makedirs(f"{odir}/DD_files", exist_ok=True)
    drs = [f"{odir}/DD_files/DD_{os.path.basename(f.strip())}".replace('.dat', f".R_{rmin}-{rmax}.dat").replace('VOID', 'CROSS') for f in void_cats]
    outs = [f"{odir}/TwoPCF_{os.path.basename(f.strip())}".replace('.dat', f".R_{rmin}-{rmax}.dat").replace('VOID', 'CROSS') for f in void_cats]
    for i in range(len(drs)):
        gal = gal_cats[i].strip()
        void = void_cats[i].strip()
        command = fcfc_cross_gv_command(16, RUN, conf_file, gal, void, drs[i], outs[i], 0, 0, rmin, rmax, cf_mode=0, count_mode=2)
        tpcf_command = SRC+f"/2pcf/2pcf.py {drs[i]} {outs[i]}"

        full_command = f"{command} && {tpcf_command}"
        print(full_command)
        
