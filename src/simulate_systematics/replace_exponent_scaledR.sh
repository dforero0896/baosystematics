#!/bin/bash
N=${SLURM_NTASKS:-1}
echo "Using ${N} tasks"
source ../.env
task_rad () {
base=$(basename ${1})
echo "==> Processing ${1}"
awk '{print $1" "$2" "$3" "$4" "$4 * (($5/$4)^(4))^(0.238)}' ${1} > ${2}/mocks_void_xyz_scaledR/${base}.TMP
mv -v ${2}/mocks_void_xyz_scaledR/${base}.TMP ${2}/mocks_void_xyz_scaledR/${base}
}

task_ang () {
base=$(basename ${1})
echo "==> Processing ${1}"
awk '{print $1" "$2" "$3" "$4" "$5" "$4 * (($6/$4)^(4))^(0.238)}' ${1} > ${2}/mocks_void_xyz_wt_scaledR/${base}.TMP
mv -v ${2}/mocks_void_xyz_wt_scaledR/${base}.TMP ${2}/mocks_void_xyz_wt_scaledR/${base}
}
for SPACE in real redshift
do
for BOX in 1 5
do
for SYST in smooth/parabola_0.8 radialgauss
do

DIR=${WORKDIR}/patchy_results/box${BOX}/${SPACE}/${SYST}/
case ${SYST} in
smooth/parabola_0.8)
ODIR=${DIR}/mocks_void_xyz_wt_scaledR
mv -v ${DIR}/void_ran/void_ran.dat ${DIR}/void_ran/void_ran_old.dat
awk '{print $1" "$2" "$3" "$4" "$5" "$4 * (($6/$4)^(4))^(0.238)}' ${DIR}/void_ran/void_ran_old.dat > ${DIR}/void_ran/void_ran.dat.TMP
mv -v ${DIR}/void_ran/void_ran.dat.TMP ${DIR}/void_ran/void_ran.dat
;;
radialgauss)
ODIR=${DIR}/mocks_void_xyz_scaledR
mv -v ${DIR}/void_ran/void_ran.dat ${DIR}/void_ran/void_ran_old.dat
awk '{print $1" "$2" "$3" "$4" "$4 * (($5/$4)^(4))^(0.238)}' ${DIR}/void_ran/void_ran_old.dat > ${DIR}/void_ran/void_ran.dat.TMP
mv -v ${DIR}/void_ran/void_ran.dat.TMP ${DIR}/void_ran/void_ran.dat
;;
esac
mkdir -v ${ODIR}
IDIR=${ODIR}_onefourth
if [[ -e ${ODIR}_onethird ]] ; then
du -h ${ODIR}_onethird
rm -rv ${ODIR}_onethird
fi
if [[ -e ${IDIR} ]]; then

echo ${IDIR} exists, skipping.
du -h ${IDIR}
#if [[ -e ${ODIR} ]]; then
#echo "==> ${ODIR} exists"
#fi
#continue
else

mv -v ${ODIR} ${IDIR}

fi


for file in $(ls ${IDIR}/*)
do
((i=i%N)); ((i++==0)) && wait
case ${SYST} in
smooth/parabola_0.8)
#task_ang ${file} ${DIR} &
;;
radialgauss)
#task_rad ${file} ${DIR} &
;;
esac

done
done
done
done

wait
echo "==> Done"
