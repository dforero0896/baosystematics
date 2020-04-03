from apply_void_weights import get_known_void_weight_matrix, edges_to_centers, get_known_void_weight
from params import *

raw_void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/nosyst/plots/void_density_map.npy"
void_dist_fn = f"{WORKDIR}/patchy_results/box1/real/smooth/parabola_0.8/plots/void_density_map.npy"

void_weight_matrix, void_matrix = get_known_void_weight_matrix(raw_void_dist_fn, void_dist_fn)
rt = np.linspace(0, 55, 100)
xt = np.linspace(0, 2600, 100)
yt = np.copy(xt)

Rt, Xt, Yt = np.meshgrid(rt, xt, yt)
Rt = Rt.ravel()
Xt=Xt.ravel()
Yt=Yt.ravel()


rc, _, xc,_,  yc, _ = *edges_to_centers(radius_bins), *edges_to_centers(xedges), *edges_to_centers(yedges)
expensive = get_known_void_weight(Rt, Xt, Yt, void_matrix, rc, xc, yc)
cheap = void_weight_matrix(Rt, Xt, Xt)
print((expensive==cheap).sum())
print(Rt.shape)
