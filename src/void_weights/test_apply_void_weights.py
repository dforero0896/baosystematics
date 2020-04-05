from apply_void_weights import get_known_void_weight_matrix, edges_to_centers, get_known_void_weight, get_known_void_weight_matrix_digitize
from params import *
import xarray as xr
raw_void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/nosyst/plots/void_density_map.npy"
void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/smooth/parabola_0.8/plots/void_density_map.npy"

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
test_centers = get_known_void_weight_matrix_digitize(Rc, Xc, Yc, void_matrix)
print(np.allclose(test_centers, void_matrix))
Rc = Rc.ravel()
Xc=Xc.ravel()
Yc=Yc.ravel()
expensive = get_known_void_weight(Rt, Xt, Yt, void_matrix, rc, xc, yc)
print("Ravel")
test_centers = get_known_void_weight_matrix_digitize(Rc, Xc, Yc, void_matrix)
print(f"With searchsorted {np.allclose(test_centers, void_matrix.ravel())}")
