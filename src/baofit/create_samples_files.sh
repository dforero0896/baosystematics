#!/bin/bash
BOX="1"
WORKDIR=/hpcstorage/dforero/projects/baosystematics/patchy_results/box${BOX}
OVERWRITE=0
for case_ in 1 2 3
do
for space in real redshift
do
for tracer in individual_gal individual_gal_nowt ind_void_parabola_case${case_} ind_void_nowt_parabola_case${case_} individual_void_nowt_case${case_}_template
do

files=$WORKDIR/$space/nosyst/baofit/${tracer}/*mystats*
ofile=$WORKDIR/$space/nosyst/baofit/${tracer}/alpha_samples.dat
if [[ ! -e $ofile ]] || [[ ${OVERWRITE} -eq 1 ]]; then
rm -v $ofile
cat $files >> $ofile
fi
wc -l $ofile
for map in smooth #noise
do
files=$WORKDIR/$space/$map/parabola_0.8/baofit/${tracer}/*mystats*
ofile=$WORKDIR/$space/$map/parabola_0.8/baofit/${tracer}/alpha_samples.dat
if [[ ! -e $ofile ]] || [[ ${OVERWRITE} -eq 1 ]]; then
rm -v $ofile
cat $files >> $ofile
fi
wc -l $ofile
done
files=$WORKDIR/$space/radialgauss/baofit/${tracer}/*mystats*
ofile=$WORKDIR/$space/radialgauss/baofit/${tracer}/alpha_samples.dat
if [[ ! -e $ofile ]] || [[ ${OVERWRITE} -eq 1 ]]; then
rm -v $ofile
cat $files >> $ofile
fi
wc -l $ofile
done
done
done
