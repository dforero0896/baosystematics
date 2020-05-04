#!/bin/bash
BOX=1
SPACE=redshift
WORKDIR=/hpcstorage/dforero/projects/baosystematics/patchy_results
for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
do
${WORKDIR}/../src/void_radius_cut/signal_to_noise.py <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled0.87-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.0-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.07-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.13-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.19-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.25-50/T*) <(ls ${WORKDIR}/box${BOX}/${SPACE}/smooth/flat_${comp}/tpcf_void_mock_nowt_R-scaled1.33-50/T*) | sort -k1 -n | tail -1
done

