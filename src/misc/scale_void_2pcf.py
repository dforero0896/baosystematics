#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get('WORKDIR')
import numpy as np

def get_rescaling_amplitude_match(syst, nosyst, smin=50, smax=80):
    s = nosyst[:,0]
    s_mask = (s>=50) & (s<=80)
    pole_ratio = []
    for i in [1, 3, 5]:
        pole_ratio.append((nosyst[s_mask,i]/syst[s_mask,i]).mean())
    
    print(pole_ratio)
    return pole_ratio

def get_rescaling_baoerr_match(syst, nosyst, smin=82.5, smax=122.5):
    s = nosyst[:,0]
    s_mask = (s>=50) & (s<=80)
    pole_ratio = []
    for i in [2, 4, 6]:
        pole_ratio.append((nosyst[s_mask,i]/syst[s_mask,i]).mean())
    print(pole_ratio)
    return pole_ratio

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(f"USAGE: {sys.argv[0]} NOSYST_AVG_2PCF SYST_AVG_2PCF")
        
    nosyst_fn = sys.argv[1]
    syst_fn = sys.argv[2]
    
    nosyst = np.loadtxt(nosyst_fn)
    syst = np.loadtxt(syst_fn)
    get_rescaling_amplitude_match(syst, nosyst)
    pole_ratio = get_rescaling_baoerr_match(syst, nosyst)
    for j,i in enumerate([1, 3, 5]):
        syst[:,i]*=pole_ratio[j]
    o,ext = os.path.splitext(syst_fn)
    oname = f"{o}_rescaled_baoerr{ext}"
    np.savetxt(oname, syst)
    print(f"==> Saved 2pcf in {oname}")



