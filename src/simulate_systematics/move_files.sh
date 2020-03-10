#!/bin/bash
SPACE=redshift
WORKDIR=/home/epfl/dforero/scratch/projects/baosystematics
IDIR=$WORKDIR/patchy_results/box1/${SPACE}/masked/mocks_gal_xyz
VETODIR=$WORKDIR/patchy_results/box1/${SPACE}/veto/mocks_gal_xyz
ANGDIR=$WORKDIR/patchy_results/box1/${SPACE}/ang/mocks_gal_xyz
VETOANGDIR=$WORKDIR/patchy_results/box1/${SPACE}/vetoang/mocks_gal_xyz

if [[ ! -e $VETODIR ]]; then
mkdir -v -p $VETODIR
fi
if [[ ! -e $ANGDIR ]]; then
mkdir -v -p $ANGDIR
fi
if [[ ! -e $VETOANGDIR ]]; then
mkdir -v -p $VETOANGDIR
fi
if [[ -e ${JOBLIST} ]]; then
rm -v ${JOBLIST}
fi

mv -v $IDIR/*VETO_ANG* $VETOANGDIR
mv -v $IDIR/*VETO* $VETODIR
mv -v $IDIR/*ANG* $ANGDIR
