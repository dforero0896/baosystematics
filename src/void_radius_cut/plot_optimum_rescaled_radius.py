import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from numpy.polynomial import polynomial as P
import sys
import os
import re
from dotenv import load_dotenv
load_dotenv()
WORKDIR=os.environ.get('WORKDIR')
SRC=os.environ.get('SRC')
sys.path.append(f"{SRC}/simulate_systematics")
from params import * 
from cycler import cycler
if __name__ == '__main__':
    colorlist = list(mcolors.TABLEAU_COLORS.keys())
    default_cycler = (cycler(color=colorlist)+cycler(linestyle=['-','--','-.', '-', '--','-.','-','--','-.', '-']))
    #os.system(f"bash {SRC}/simulate_systematics/optimum_rescaled_radius.sh | tee {WORKDIR}/patchy_results/box1/redshift/plots/optimum_rescaled_radius.dat")			
    fig, ax = plt.subplots(1,1)
    ax.set_prop_cycle(default_cycler)
    space='redshift'
    boxes = ['1']
    for box in boxes:
        data, dirnames = np.loadtxt(f"{WORKDIR}/patchy_results/box{box}/{space}/plots/optimum_rescaled_radius.dat", usecols=(0,1), unpack=True, dtype=str)
        data = data.astype(float)
        Rvals = np.array([re.findall('R.scaled[0-9].*-50$', \
		s)[0].replace('R-scaled','').replace('-50','') for s in dirnames],\
									 dtype=float)
        Cvals = np.array([re.findall('flat_[0-9].*\/tpcf', \
		s)[0].replace('flat_','').replace('/tpcf','') for s in dirnames],\
									 dtype=float)
        ngals = Cvals * NGAL[box]
        c = P.polyfit(ngals * 1e4,Rvals,1,full=False) 
        ngal_linsp = np.linspace(0.1, 4, 20)
        #rvals = NGAL[box]**(1./3) * Rvals
        line, = ax.plot(1e4 * ngals, Rvals, marker='*', lw=0, c = 'k')
        #ax.axhline(1.13, color = line.get_color(), ls = ':')
        ax.plot(ngal_linsp, c[0] + c[1]*ngal_linsp, label=r"$\bar{n}_{\mathrm{gal}}^{1/3}~R^* =%+.2f %+.2f\times 10^4\bar{n}_{\mathrm{gal}}$"%tuple(c), c = 'k')
    ax.set_ylabel(r'Optimum $\bar{n}_{\mathrm{gal}}^{1/3}~R^*$', fontsize=12)
    ax.set_xlabel(r'$\bar{n}_{\mathrm{gal}}$ [$10^{-4}h^3$/Mpc$^3]$', fontsize=12)
    ax.legend(loc=0)
    fig.tight_layout()
    oname = f"{WORKDIR}/patchy_results/box1/redshift/plots/optimum_rescaled_radius.pdf"
    fig.savefig(oname, dpi=200)
    print(f"==> Saved figure in {oname}")
