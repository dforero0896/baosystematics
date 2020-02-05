#!/usr/bin/env python
import sys
import os
from astropy.table import Table
if len(sys.argv) != 3:
  sys.stderr.write('Usage: {} INPUT OUTPUT'.format(sys.argv[0]))
  sys.exit(1)
t = Table.read(sys.argv[1], format='fits', hdu=1)
sys.stdout.write('Read file %s\n'%os.path.basename(sys.argv[1]))
t['WEIGHT_COMP'] = t['WEIGHT_SYSTOT'] * t['WEIGHT_CP'] * t['WEIGHT_NOZ']
t['WEIGHT_ALL'] = t['WEIGHT_COMP'] * t['WEIGHT_FKP']
t['RA','DEC','Z','WEIGHT_ALL','WEIGHT_COMP','WEIGHT_FKP','NZ'][t['veto']].write(sys.argv[2], format='ascii.commented_header', overwrite=True, formats={'RA':'%.8g','DEC':'%.8g','Z':'%.8g', 'WEIGHT_ALL':'%.8g','WEIGHT_COMP':'%.8g','WEIGHT_FKP':'%.8g', 'NZ':'%.8g'})
sys.stdout.write('Wrote file %s\n'%os.path.basename(sys.argv[2]))
