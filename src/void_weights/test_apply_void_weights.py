from apply_void_weights import get_known_void_weight_matrix, edges_to_centers, get_known_void_weight, get_known_void_weight_matrix_digitize
from params import *
import xarray as xr
raw_void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/nosyst/plots/void_density_map.npy"
void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/smooth/parabola_0.8/plots/void_density_map.npy"

void_weight_matrix, void_matrix = get_known_void_weight_matrix(raw_void_dist_fn, void_dist_fn)
rt = np.linspace(0, 50, 100)
xt = np.linspace(0, 2500, 100)
yt = np.copy(xt)

Rt, Xt, Yt = np.meshgrid(rt, xt, yt)
Rt = Rt.ravel()
Xt=Xt.ravel()
Yt=Yt.ravel()
dims = ['r', 'x', 'y']
rc, _, xc,_,  yc, _ = *edges_to_centers(radius_bins), *edges_to_centers(xedges), *edges_to_centers(yedges)
expensive = get_known_void_weight(Rt, Xt, Yt, void_matrix, rc, xc, yc)
cheap = void_weight_matrix(Rt, Xt, Xt)
print(get_known_void_weight_matrix_digitize(0, 0, 0, void_matrix))
print(get_known_void_weight_matrix_digitize(50, 2500, 2500, void_matrix))
diffid=np.argwhere(expensive!=cheap)[0]
print(expensive[diffid], cheap[diffid], get_known_void_weight_matrix_digitize(Rt[diffid], Xt[diffid], Yt[diffid], void_matrix))
print(Rt[diffid], Xt[diffid], Yt[diffid])
print('Test centers')
Rc, Xc, Yc = np.meshgrid(rc, xc, yc)
Rc = Rc.ravel()
Xc=Xc.ravel()
Yc=Yc.ravel()
test_centers = get_known_void_weight_matrix_digitize(Rc, Xc, Yc, void_matrix)
print(sum(test_centers==void_matrix.ravel()))

