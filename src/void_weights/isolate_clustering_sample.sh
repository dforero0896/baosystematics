#!/bin/bash
source ../.env
N=${1:-16}

task(){
awk '$5>2.2' $1 > ${2}_TMP
mv -v ${2}_TMP $2
}
for box in 1 5
do

for syst in smooth/parabola_0.8 radialgauss
do
IDIR=${WORKDIR}/patchy_linhalo/box${box}/real/${syst}/mocks_void_xyz_scaledR
ODIR=${WORKDIR}/patchy_linhalo/box${box}/real/${syst}/mocks_void_xyz_scaledR_Csamp
if [[ ! -e ${ODIR} ]]; then
mkdir -v $ODIR
fi
for file in $(ls ${IDIR}/*)
do
ofile=${ODIR}/$(basename $file)
((i=i%N)); ((i++==0)) && wait
echo Processing  ${file}
task $file $ofile &
done

done
done
