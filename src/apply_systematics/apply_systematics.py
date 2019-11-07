import os
from astropy.table import Table
import numpy as np
import sys
from scipy import interpolate
import matplotlib.pyplot as plt
if len(sys.argv) > 6 or len(sys.argv) < 4:
	sys.stderr.write('ERROR:\tUnexpected number of arguments.\n')
	sys.stderr.write('Usage:\t{} INPUT OUTPUT SYS_EFFECT [SYS_EFFECT SYS_EFFECT]\n'.format(sys.argv[0]))
	sys.exit(1)
systematic_effects = ['CP', 'NOZ', 'SYSTOT', 'NONE']
sys_effect = [s.upper() for s in sys.argv[3:]]
sys_effect_test = [not s in systematic_effects for s in sys_effect]
if any(sys_effect_test):
	sys.stderr.write('ERROR: SYS_EFFECT not understood.\nPlease choose SYS_EFFECT=CP, NOZ, SYSTOT\n')
	sys.exit(1)
sys.stdout.write('Applying %s\n'%sys_effect)
no_syst_test = [s == 'NONE' for s in sys_effect]
none=False
if any(no_syst_test): none=True;
filename_dat = sys.argv[1]
filename_ran = filename_dat.replace('.dat.', '.ran.')
outname_dat = sys.argv[2]
outname_ran = outname_dat.replace('.dat.', '.ran.')
outpath = os.path.dirname(outname_dat)
results_path = os.path.join(outpath, '../')
raw_random_density = 20 * 6.4e-4
delta_z = 0.005
P0 = 4000
z_min = 0.6
z_max = 1.1
z_bin_edges = np.arange(z_min, z_max+delta_z, delta_z)
z_bin_centers = ((z_bin_edges + 0.5 * delta_z))[:-1]

def apply_systematics(table, none=none):
	table['WEIGHT_COMP_ALLSYS'] = table['WEIGHT_SYSTOT'] * table['WEIGHT_CP'] * table['WEIGHT_NOZ'] * table['veto']
	allsys_weight_comp = table['WEIGHT_COMP_ALLSYS'].sum() 
	sys.stdout.write('Original effective number of tracers %.2f\n'%allsys_weight_comp)
	if none:
		table['WEIGHT_COMP']=1.
	else:
		table['WEIGHT_COMP'] = np.prod([table['WEIGHT_%s'%s] for s in sys_effect], axis = 0)
	t_new = table[(table['WEIGHT_COMP']!=0) & (table['veto'])]
	partialsys_weight_comp = t_new['WEIGHT_COMP'].sum()
	t_new['WEIGHT_COMP']*=allsys_weight_comp/partialsys_weight_comp
	sys.stdout.write('New effective number of tracers %.2f\n'%t_new['WEIGHT_COMP'].sum())
	sys.stdout.write('%i lines left after applying systematics\n'%len(t_new))
	return t_new 

table_dat = Table.read(filename_dat, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_dat))
table_dat_syst = apply_systematics(table_dat)
table_ran = Table.read(filename_ran, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_ran))
table_ran_syst = apply_systematics(table_ran) #Renormalize to only SYSTOT
#z_counts_dat, _ = np.histogram(table_dat_syst['Z'].data, z_bin_edges, weights = table_dat_syst['WEIGHT_COMP'].data)
#z_counts_ran, _ = np.histogram(table_ran_syst['Z'].data, z_bin_edges, weights = table_ran_syst['WEIGHT_COMP'].data)
#new_nz_interp = interpolate.interp1d(z_bin_edges, np.pad(new_nz, (0,1), 'constant', constant_values=new_nz[-1]), kind = 'linear') # Interpolation with bin edges.
#table_dat_syst['NZ'] = new_nz_interp(table_dat_syst['Z'].data)
#for i in range(len(z_bin_centers)): # Instead of linear interpolation.
#	table_dat_syst['NZ'][(table_dat_syst['Z'] > z_bin_edges[i]) & (table_dat_syst['Z'] < z_bin_edges[i+1])] = new_nz[i] #= z_counts_dat / volume_eff
#table_dat_syst['WEIGHT_FKP'] = (1 + table_dat_syst['NZ']*P0)**(-1)
table_dat_syst['WEIGHT_ALL'] = table_dat_syst['WEIGHT_COMP'] * table_dat_syst['WEIGHT_FKP']
table_ran_syst['WEIGHT_ALL'] = table_ran_syst['WEIGHT_COMP'] * table_ran_syst['WEIGHT_FKP']
table_dat_syst['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].write(outname_dat, format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(outname_dat))
table_ran_syst['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].write(outname_ran, format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(outname_ran))
