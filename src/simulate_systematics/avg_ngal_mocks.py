import numpy as np
import os
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f"ERROR: Unexpected number of arguments\nUSAGE: {sys.argv[0]} NGAL")
        
    iname = sys.argv[1]
    name,ext = os.path.splitext(iname)
    oname = name+"_avg"+ext
    print(f"==> Loading file {iname}")
    data = np.load(iname)
    print(f"==> Saving file {oname}")
    np.save(oname, data.mean(axis=-1))


