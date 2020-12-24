#!/usr/bin/env python

import numpy as np
import os
import sys
import subprocess
import tempfile

if __name__ == '__main__':
    data = np.zeros((10000000, 4))
    tf = tempfile.NamedTemporaryFile()
    print("Saving data", flush=True)
    np.savetxt(tf, data)

    subprocess.check_call(["/home/astro/dforero/codes/FCFC_box/2pcf", f"--data={tf.name}"])
    tf.close()

