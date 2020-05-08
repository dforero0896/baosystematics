#!/bin/bash
BOX="1"
WORKDIR=/hpcstorage/dforero/projects/baosystematics/patchy_results/box${BOX}
for space in real redshift
do
for tracer in gal gal_nowt void void_nowt
do

files=$WORKDIR/$space/nosyst/baofit/individual_${tracer}/*mystats*
ofile=$WORKDIR/$space/nosyst/baofit/individual_${tracer}/alpha_samples.dat
rm -v $ofile
cat $files >> $ofile
wc -l $ofile
for map in noise smooth
do
files=$WORKDIR/$space/$map/parabola_0.8/baofit/individual_${tracer}/*mystats*
ofile=$WORKDIR/$space/$map/parabola_0.8/baofit/individual_${tracer}/alpha_samples.dat
rm -v $ofile
cat $files >> $ofile
wc -l $ofile
done
done
done

