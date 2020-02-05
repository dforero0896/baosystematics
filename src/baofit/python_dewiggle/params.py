# Parameters for BAO fitting
## Range of alpha (Eq. 25 of Xu et al. 2012)
amin            = 0.8
amax            = 1.2
anum            = 201
## s range for fitting alpha
fit_smin        = 60
fit_smax        = 150

# Input/Output
## The input 2PCF to be fitted, with the first two columns being (s, xi_0)
input_data      = "ELG/2PCF_eBOSS_ELG_clustering_NS_v4_z0.6z1.1.dat"
## Directory for outputs.
output_dir      = "output/"
## True for detailed standard output
verbose         = True

# Covariance matrix
## If `compute_cov` = True, then read `input_mocks` for a list of mock files,
##   and then compute the covariance matrix using the mocks.
## If `compute_cov` = True and `save_cov` = True, then write the pre-processed
##   covariance matrix to file `cov_file`.
## If `compute_cov` = False, then read the covariance matrix from `cov_file`.
compute_cov     = True
save_cov        = False
input_mocks     = "ELG/mocks.dat"
cov_file        = "input/cov.dat"

# Theoretical model
## True for generating the linear P(k) using CAMB, otherwise read (k, P(k))
##   From the file `input_plin`
plin_run        = False
#input_plin      = "input/Albert_Plin.dat"
input_plin      = "/hpcstorage/dforero/projects/baosystematics/bin/BAOfit_void/input/CAMB_matterpower.dat"
## True for generating the linear no BAO P(k) using the Eisenstein & Hu (1998)
##   formulae, otherwise read (k, Pnw(k)) from the file `input_pnw`
pnw_run         = True
input_pnw       = "/hpcstorage/dforero/projects/baosystematics/bin/BAOfit_void/input/Albert_Pnw.dat"
### Maximum k value for normalizing Pnw
k_norm          = 5e-4
## Configurations for the template P(k) and xi(s)
smin            = 10
smax            = 250
num_s_bin       = 241
### `kmin`, `kmax`, and `num_lnk_bin` are only used if `k_interp` = True
k_interp        = True
kmin            = 7.5e-5
kmax            = 250
num_lnk_bin     = 5000
### a in Eq. 27 of Xu et al. 2012
damp_a          = 1.0
### Number of polynomial parameters
npoly           = 3
## Parameters for the linear P(k) and no BAO P(k) (optional)
h               = 0.6777
Omega_m         = 0.307115
Omega_b         = 0.048143
Tcmb            = 2.7255
w               = -1
omnuh2          = 0.00064
omk             = 0
helium_fraction = 0.24
massless_neutrinos = 2.046
nu_mass_eigenstates = 1
massive_neutrinos = 1
nu_mass_fractions = 1
transfer_kmax   = 500           # kmax could vary with transfer_k_per_logint=0
transfer_redshift = 0.61
ns              = 0.97
scalar_amp      = 2.1e-9
## Executable for CAMB
camb_exe        = "/home/czhao/programs/CAMB/camb"

