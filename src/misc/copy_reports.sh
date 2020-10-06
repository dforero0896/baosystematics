#!/bin/bash
find abacus_results/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find abacus_results/ -wholename '*/avg*' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -wholename '*plots/*' -size -3G| xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -wholename '*baofit/avg*/*' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -wholename '*baofit/*/alpha_samples.dat' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon/ -wholename '*plots/*' -size -3G| xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon/ -wholename '*baofit/avg*/*' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon_nods/ -wholename '*plots/*' -size -3G| xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon_nods/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_recon_nods/ -wholename '*baofit/avg*/*' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_linhalo/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -wholename '*baofit/*/alpha_samples.dat' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -wholename '*plots/*' -size -3G| xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find lrg_results/ -wholename '*plots/*' -size -3G| xargs -I '{}' cp -u -v {} --parents reports/
find lrg_results/ -name '*.npy' -size -3G | xargs -I '{}' cp -u -v {} --parents reports/
find patchy_results/ -name '*mockavg*' | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*mockavg*ascii' | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*xi0*mean*' | xargs -I '{}' cp -u -v {} --parents reports/
find results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
find lrg_results/ -name '*.pdf' | xargs -I '{}' cp -u -v {} --parents reports/
