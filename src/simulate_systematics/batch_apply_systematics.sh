#!/bin/bash
WORKDIR=/home/epfl/dforero/scratch/projects/baosystematics
RUN=$WORKDIR/bin/apply_systematics
JOBLIST=joblist.sh
SEED=1
BOX=1
SPACE=real
TRACER=void
SYST=ang
IDIR=$WORKDIR/patchy_results/box${BOX}/${SPACE}/${SYST}/mocks_${TRACER}_xyz
ODIR=$WORKDIR/patchy_results/box${BOX}/${SPACE}/masked/${SYST}_mocks_${TRACER}_xyz
if [[ ! -e $ODIR ]]; then
mkdir -v -p $ODIR
fi
if [[ -e ${JOBLIST} ]]; then
rm -v ${JOBLIST}
fi

for filename in $(ls -p $IDIR/*)
do
outname=${ODIR}/$(basename $filename | sed -e "s/\.dat//g")
echo "${RUN} ${filename} ${SEED} ${outname}" >> ${JOBLIST}
done
