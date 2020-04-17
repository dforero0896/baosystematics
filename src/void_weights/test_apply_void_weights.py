from apply_void_weights import edges_to_centers, get_known_void_weight, get_known_void_weight_matrix, get_numdens_from_matrix
from params import *
import xarray as xr
raw_void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/nosyst/plots/void_density_map.npy"
void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/smooth/parabola_0.8/plots/void_density_map.npy"
n_matrix_fn = f"{WORKDIR}/patchy_results/box1/real/smooth/parabola_0.8/plots/ngal.npy"

void_matrix = get_known_void_weight_matrix(raw_void_dist_fn, void_dist_fn)
rt = np.linspace(0, 50, 100)
xt = np.linspace(0, 2500, 100)
yt = np.copy(xt)

Rt, Xt, Yt = np.meshgrid(rt, xt, yt)
Rt = Rt.ravel()
Xt=Xt.ravel()
Yt=Yt.ravel()
dims = ['r', 'x', 'y']
rc, _, xc,_,  yc, _ = *edges_to_centers(radius_bins), *edges_to_centers(xedges), *edges_to_centers(yedges)
print('Test centers')
print(f"rc = {rc}")
Rc, Xc, Yc = np.meshgrid(rc, xc, yc, indexing='ij')
print(f"Check that the matrix from sampling the centers is the same as the input.")
print(f"No ravel")
test_centers = get_known_void_weight(Rc, Xc, Yc, void_matrix)
print(np.allclose(test_centers, void_matrix))
Rc = Rc.ravel()
Xc=Xc.ravel()
Yc=Yc.ravel()
print("Ravel")
test_centers = get_known_void_weight(Rc, Xc, Yc, void_matrix)
print(f"With searchsorted {np.allclose(test_centers, void_matrix.ravel())}")


print("TESTING NUMDENS")
import matplotlib.pyplot as plt
n_matrix = np.load(n_matrix_fn)
n_matrix = n_matrix.mean(axis=-1)

x = np.linspace(0, 2500, 50)
y = x
z = x

X, Y, Z = np.meshgrid(x,y,z, indexing='ij')
result = get_numdens_from_matrix(X, Y, Z, n_matrix)
print(result.mean())
print(n_matrix.sum()/box_size**3)
#plt.imshow(result)
#plt.show()

n_matrix = np.load('/home/epfl/dforero/scratch/projects/baosystematics/patchy_results/box1/real/radialgauss/plots/ngal_radial.npy')
from apply_void_weights import get_numdens_radial
result = get_numdens_radial(X,Y,Z, n_matrix)
print(result.mean())
print(n_matrix.sum()/box_size**3)
