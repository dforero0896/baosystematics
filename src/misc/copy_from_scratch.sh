#!/usr/bin/bash
#copy_from_scratch.sh
HOME=/global/homes/d/dforero
for dir in $(ls -d $SCRATCH/baosystematics/results/*); do
for subdir in $(ls -d $dir/* | grep avg); do
echo $subdir
dest=$(echo $subdir | sed -e 's/\/global\/cscratch1\/sd\/dforero/\/global\/homes\/d\/dforero\/projects/g')
if [[ ! -e $(dirname $dest) ]]; then
mkdir $(dirname $dest)
fi
if [[ ! -e $dest ]]; then
mkdir $dest
fi
echo $dest
cp -r $subdir/* $dest/
done
done
