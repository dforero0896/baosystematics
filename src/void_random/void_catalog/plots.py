#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
mocks100 = pd.read_csv('mocksCombined100.ascii', sep = '\t', dtype=float, header = None)
print mocks100[3]

Rs = mocks100[3][mocks100[3]<=35]
minR =  Rs.min()
maxR =  Rs.max()
fig = plt.figure()
for i in range(3*3):
	x, y = np.unravel_index(i, (3,3))
	fig.add_subplot(3, 3, i+1)
	b=int((maxR-minR)/(i+1))
	ax = Rs.plot.hist(bins=b, alpha=0.5, label = 'bins=%i'%b)
	ax.set_xlim(0,30)
plt.legend()

plt.gcf()
plt.savefig('/home/epfl/dforero/results/R_hist.png', dpi = 300)




print 'ok'

