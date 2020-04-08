#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get('WORKDIR')
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(f"USAGE: {sys.argv[0]} NOSYST_AVG_2PCF SYST_AVG_2PCF")
        
    nosyst_fn = sys.argv[1]
    syst_fn = sys.argv[2]
    
    nosyst = np.loadtxt(nosyst_fn)
    syst = np.loadtxt(syst_fn)
    s = nosyst[:,0]
    s_mask = (s>=50) & (s<=80)
    for i in [1, 3, 5]:
        pole_ratio = (nosyst[s_mask,i]/syst[s_mask,i]).mean()
        syst[:,i]*=pole_ratio
    o,ext = os.path.splitext(syst_fn)
    oname = f"{o}_rescaled{ext}"
    np.savetxt(oname, syst)
    print(f"==> Saved 2pcf in {oname}")



