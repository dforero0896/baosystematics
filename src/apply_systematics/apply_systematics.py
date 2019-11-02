import os
from astropy.table import Table
import numpy as np
import sys
from scipy import interpolate
import matplotlib.pyplot as plt
if len(sys.argv) > 6:
	sys.stderr.write('Usage: {} INPUT OUTPUT SYS_EFFECT [SYS_EFFECT SYS_EFFECT]\n'.format(sys.argv[0]))
	sys.exit(1)
systematic_effects = ['CP', 'NOZ', 'SYSTOT']
sys_effect = [s.upper() for s in sys.argv[3:]]
sys_effect_test = [not s in systematic_effects for s in sys_effect]
if any(sys_effect_test):
	sys.stderr.write('ERROR: SYS_EFFECT not understood.\nPlease choose SYS_EFFECT=CP, NOZ, SYSTOT\n')
	sys.exit(1)
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
def apply_systematics(table):
	table['WEIGHT_COMP'] = np.prod([table['WEIGHT_%s'%s] for s in sys_effect], axis = 0)
	t_new = table[(table['WEIGHT_COMP']!=0) & (table['COMP_BOSS'] != 0) & (table['veto'])]
	sys.stdout.write('%i lines left after applying systematics\n'%len(t_new))
	return t_new 

table_dat = Table.read(filename_dat, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_dat))
table_ran = Table.read(filename_ran, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_ran))
table_dat_syst = apply_systematics(table_dat)
print(np.mean(table_dat_syst.group_by('chunk')['WEIGHT_SYSTOT'].groups[0]))
print(min(table_dat_syst['Z']))
z_counts_dat, _ = np.histogram(table_dat_syst['Z'].data, z_bin_edges, weights = table_dat_syst['WEIGHT_COMP'].data)
table_ran_syst = apply_systematics(table_ran)
z_counts_ran, _ = np.histogram(table_ran_syst['Z'].data, z_bin_edges, weights = table_ran_syst['COMP_BOSS'].data**-1)
volume_eff = z_counts_ran / raw_random_density
new_nz = z_counts_dat / volume_eff
new_nz_interp = interpolate.interp1d(z_bin_edges, np.pad(new_nz, (0,1), 'constant', constant_values=new_nz[-1]), kind = 'linear')
table_dat_syst['NZ'] = new_nz_interp(table_dat_syst['Z'].data)
#for i in range(len(z_bin_centers)):
#	table_dat_syst['NZ'][(table_dat_syst['Z'] > z_bin_edges[i]) & (table_dat_syst['Z'] < z_bin_edges[i+1])] = new_nz[i] #= z_counts_dat / volume_eff
table_dat_syst['WEIGHT_FKP'] = (1 + table_dat_syst['NZ']*P0)**(-1)
table_ran_syst['WEIGHT_FKP'] = (1 + table_ran_syst['NZ']*P0)**(-1)
table_dat_syst['WEIGHT_ALL'] = table_dat_syst['WEIGHT_COMP'] * table_dat_syst['WEIGHT_FKP']
table_ran_syst['WEIGHT_ALL'] = table_ran_syst['WEIGHT_COMP'] * table_ran_syst['WEIGHT_FKP']
#table_dat_syst['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].write(outname_dat, format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(outname_dat))
#table_ran_syst['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'].write(outname_ran, format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(outname_ran))
