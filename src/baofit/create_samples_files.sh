#!/bin/bash
BOX="1"
WORKDIR=/hpcstorage/dforero/projects/baosystematics/patchy_results/box${BOX}
for space in real redshift
do
for map in noise smooth
do
for tracer in gal gal_nowt void void_nowt
do
files=$WORKDIR/$space/$map/parabola/baofit/individual_${tracer}/*mystats*
echo "$files"
ofile=$WORKDIR/$space/$map/parabola/baofit/individual_${tracer}/alpha_samples.dat
rm -v $ofile
cat $files >> $ofile
wc -l $ofile
done
done
done

