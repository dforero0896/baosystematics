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
sys.path.append(f"../misc")
from params import * 
from style_plots import set_size
from cycler import cycler
from scipy.optimize import curve_fit
from scipy import stats
def R_vs_ngal(ngal, a, b, c, d):
    return a * (ngal - b)**c + d
if __name__ == '__main__':
    colorlist = list(mcolors.TABLEAU_COLORS.keys())
    default_cycler = (cycler(color=colorlist)+cycler(linestyle=['-','--','-.', '-', '--','-.','-','--','-.', '-']))
    #os.system(f"bash {SRC}/simulate_systematics/optimum_rescaled_radius.sh | tee {WORKDIR}/patchy_results/box1/redshift/plots/optimum_rescaled_radius.dat")			
    fig, ax = plt.subplots(1,1, figsize=set_size('mnras', fraction=2, subplots=(1,1)))
    ax.set_prop_cycle(default_cycler)
    space='redshift'
    boxes = ['1']
    for box in boxes:
        data, dirnames = np.loadtxt(f"{WORKDIR}/patchy_results/box{box}/{space}/plots/optimum_rescaled_radius.dat", usecols=(0,-2), unpack=True, dtype=str)
        data = data.astype(float)
        Rvals = np.array([re.findall('R.scaled[0-9].*-50$', \
		s)[0].replace('R-scaled','').replace('-50','') for s in dirnames],\
									 dtype=float)
        Cvals = np.array([re.findall('flat_[0-9].*\/tpcf', \
		s)[0].replace('flat_','').replace('/tpcf','') for s in dirnames],\
									 dtype=float)
        ngals = Cvals * NGAL[box]
        Rvals/=ngals**(1./3)
        np.savetxt(f"{WORKDIR}/patchy_results/box{box}/{space}/plots/optimum_rescaled_radius_clean.dat", np.c_[Rvals, ngals], header='Roptimum ngal')
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(ngals*1e4), np.log(Rvals))
        c, stats = P.polyfit(np.log(ngals * 1e4),np.log(Rvals),1,full=True) 
        print(slope, intercept, r_value, std_err)
        ngal_linsp = np.linspace(0.1, 4, 20)
        #rvals = NGAL[box]**(1./3) * Rvals
        line, = ax.plot(1e4 * ngals, Rvals*ngals**(-slope), marker=(5, 1, 180), lw=0, c = 'k')
        print(np.mean(Rvals*ngals**(-slope)))
        ax.axhline(np.exp(intercept)*10**(4*slope), c='k', ls='--', label=r'$\bar{n}_{\mathrm{gal}}^{%0.2f}~R^* = %+.2f$ (Mpc/$h$)$^{%.2f}$'%(-slope,np.exp(intercept)*10**(4*slope), -slope))
        ax.plot(ngal_linsp, (ngal_linsp*1e-4)**(-slope)*np.exp(slope*np.log(ngal_linsp) + intercept), label=r"$\log R^* =%+.2f %+.2f \log(10^4\bar{n}_{\mathrm{gal}})$"%(intercept, slope), c = 'r')
    ax.set_ylabel(r'$\bar{n}_{\mathrm{gal}}^{%.2f}~R^*$ [(Mpc/$h$)$^{%.2f}$]'%(-slope, -slope), fontsize=11)
    ax.set_xlabel(r'$\bar{n}_{\mathrm{gal}}$ [$10^{-4}h^3$/Mpc$^3]$', fontsize=11)
    ax.set_ylim(1,3)
    ax.legend(loc=0)
    fig.tight_layout()
    oname = f"{WORKDIR}/patchy_results/box1/redshift/plots/optimum_rescaled_radius.pdf"
    fig.savefig(oname, dpi=200)
    print(f"==> Saved figure in {oname}")
