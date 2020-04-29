import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import sys
import os
import re
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get('WORKDIR')
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
sys.path.append(f"../misc")
from style_plots import set_size
from params import * 
from cycler import cycler
if __name__ == '__main__':
    colorlist = list(mcolors.TABLEAU_COLORS.keys())
    colorlist = ['k', 'r'] 
    linestyle=['-','--','-.', '-', '--','-.','-','--','-.', '-']
    linestyle=['-', '--']
    default_cycler = (cycler(color=colorlist)+cycler(linestyle=linestyle))
			
    fig, ax = plt.subplots(1,1, figsize=set_size('mnras', fraction=2))
    ax.set_prop_cycle(default_cycler)
    boxes = ['1', '5']
    for box in boxes:
        data, dirnames = np.loadtxt(f"{WORKDIR}/patchy_results/box{box}/plots/snr_analysis.dat", usecols=(0,1), unpack=True, dtype=str)
        data = data.astype(float)
        Rvals = np.array([re.findall('R.[0-9].*-50$', \
		s)[0].replace('R-','').replace('-50','') for s in dirnames],\
									 dtype=float)
        
        rvals = NGAL[box]**(1./4) * Rvals
        line, = ax.plot(rvals, data, label=f"Box {box}", marker='o')
        #ax.axvline(NGAL[box]**(1./4) * 16, color = line.get_color(), ls = ':')
    ax.grid()
    ax.set_xlabel(r'$\bar{n}_{\mathrm{gal}}^{1/4}~R$ [(Mpc/$h$)$^{1/4}$]', fontsize=11)
    ax.set_ylabel(r'SNR', fontsize=11)
    ax.legend(loc=0, fontsize=10)
    fig.tight_layout()
    oname = f"{WORKDIR}/patchy_results/box1/plots/snr_allboxes.pdf"
    fig.savefig(oname, dpi=200)
    print(f"==> Saved figure in {oname}")
