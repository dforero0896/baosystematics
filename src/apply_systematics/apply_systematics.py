import os
from astropy.table import Table
import numpy as np
import sys
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
delta_z = 0.005
z_min = 0.5
z_max = 1.2
z_bin_edges = np.arange(z_min, z_max+delta_z, delta_z)
z_bin_centers = ((z_bin_edges + 0.5 * delta_z))[:-1]
def apply_systematics(table):
	table['WEIGHT_COMP'] = np.prod([table['WEIGHT_%s'%s] for s in sys_effect], axis = 0)
	return table[table['WEIGHT_COMP']!=0]

table_dat = Table.read(filename_dat, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_dat))
table_ran = Table.read(filename_ran, format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(filename_ran))
table_dat_syst = apply_systematics(table_dat)
z_counts_dat, _ = np.histogram(table_dat_syst['Z'], z_bin_edges)
table_ran_syst = apply_systematics(table_ran)
z_counts_ran, _ = np.histogram(table_ran_syst['Z'], z_bin_edges)
t['WEIGHT_ALL'] = t['WEIGHT_COMP'] * t['WEIGHT_FKP']
#t['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'][t['veto']].write(sys.argv[2], format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(sys.argv[2]))
