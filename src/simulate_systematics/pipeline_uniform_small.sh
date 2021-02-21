#!/bin/bash


source ../.env
N=${SLURM_NTASKS:-1}
BOX=1
RUNFCFC=${WORKDIR}/bin/FCFC/FCFC_2PT_BOX
task() {

    file=$1
    bdir=$(dirname $(dirname ${file}))/
    bname=$(basename ${file} | sed -e 's/.dat.*$//g')
    if [[ "${file}" == *".xz" ]]; then 
        xz --decompress ${file}
        newfile=$(echo ${file} | sed -e 's/\.xz//g')
    else
        ifile=${file}
        newfile=${file}
    fi
    for dr in 0.5 0.6 0.7 0.8 0.9 1.0
    do
        NGAL=$(awk -v C="${comp}" 'BEGIN {print 4e-4 * C}')
        RMAX=$(awk -v r="${dr}" -v n="${NGAL}" 'BEGIN {print r * n ^(-1/3)}')
        selection="\$4<${RMAX}"
        cfdir=${bdir}/tpcf_void_mock_nowt_R-0-dr${dr}
        cffile=${cfdir}/TwoPCF_${bname}.dat
        ddfile=${cfdir}/DD_files/DD_${bname}.dat
        if [[ "${newfile}" == *".npy" ]];then
            bname=$(basename ${file} | sed -e 's/.npy.*$//g')
            ifile=${newfile}.fifo
            mkfifo -v ${ifile}
            python ${WORKDIR}/bin/pydive/pydive/void_npy_to_text.py -npy_file ${newfile} -text_file ${ifile} &
        else
            ifile=${newfile}
        fi
        if [[ ! -e ${cfdir} ]]; then
            mkdir -vp ${cfdir}/DD_files
        fi
        srun -n1 -c16 -N1  ${RUNFCFC} --conf=fcfcnew.conf --input=${ifile} --pair-output=${ddfile} --cf-output=${cffile} --select=${selection}  
    done

    xz -9 -T0 -v ${newfile}



}
i=$1
j=$2
allcomps=(0.95 0.9 0.85 0.8 0.75 0.7 0.65 0.6 0.55 0.5 0.45 0.4 0.35 0.3 0.25 0.2 0.15 0.1)

for recon in patchy_results #patchy_recon_nods
do

#for comp in 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95
for comp in ${allcomps[@]} 
do
        
    BDIR=${WORKDIR}/${recon}/box${BOX}/redshift/smooth/flat_${comp}/
    allfiles=($(ls ${BDIR}/mocks_void_xyz/CAT*))
    for file in ${allfiles[$j]}
    do
        ((i=i%N)); ((i++==0)) && wait
        task ${file} 
        
    done

done
done
