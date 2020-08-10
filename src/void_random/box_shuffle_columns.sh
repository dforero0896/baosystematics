#/bin/bash
BOX_SIZE=2500

if [[ $# -ne 3 ]]; then
    echo 'ERROR: Unexpected number of arguments.'
    echo USAGE: bash $0 BINS_DIR KIND OVERWRITE
    exit 1
fi
BINSDIR=$1
SHUFCOLSDIR=$(dirname $BINSDIR)/shuf_cols
ODIR=$(dirname $BINSDIR)
OFILE=${ODIR}/BIG_RAN_VOID.dat

zin=0
zfin=$(( $BOX_SIZE ))
zbin_width=100
rin=0
rfin=21
rbin_width=1
redges=($(seq $rin $rbin_width $rfin) 25 30 50)
zedges=($(seq $zin $zbin_width $zfin))
kind=$2
if [[ -e ${OFILE} ]]
then
rm -v $OFILE
fi

for zid in $(seq 1 1 $(( ${#zedges[@]} )))
do
    for rid in $(seq 1 1 $(( ${#redges[@]})))
    do
    echo $zid, $rid
    if [[ "$kind" == "ang" ]];then
        awk '$3 == 0' <(ls ${BINSDIR}/*_zmax${zid}_rmax${rid}.left 2>/dev/null | xargs -I '{}' cat {})
    fi
    paste <(ls -p ${BINSDIR}/*_zmax${zid}_rmax${rid}.left 2>/dev/null | xargs -I '{}' cat {} | shuf) <(ls -p ${BINSDIR}/*_zmax${zid}_rmax${rid}.right 2>/dev/null  | xargs -I '{}' cat {}) | sed -e "s/\t/ /g" >> $OFILE || exit 1
    done

done
if [[ "$kind" == "ang" ]]; then
if [[ "$(awk '{print NF; exit}' ${OFILE})" -eq 5 ]]; then
awk '{print $1 "\t" $2 "\t"  $4  "\t" $5 "\t" $3}' ${OFILE} > ${OFILE}_TMP
elif [[ "$(awk '{print NF; exit}' ${OFILE})" -eq 6 ]]; then
awk '{print $1 "\t" $2 "\t"  $4  "\t" $5 "\t" $6 "\t" $3}' ${OFILE} > ${OFILE}_TMP
fi
mv ${OFILE}_TMP ${OFILE}
fi

