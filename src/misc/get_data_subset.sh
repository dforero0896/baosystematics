#!/bin/env/bash
SEED=1005638091
side=$1
if [[ "$side" == "S" ]]; then
find ~+ -wholename "*nosyst*${SEED}*" | grep -v baofit > copy_to_local.dat.TMP
sed -e "s/baosystematics/baosystematics\/./g" copy_to_local.dat.TMP > copy_to_local.dat
rm -v copy_to_local.dat.TMP
fi

if [[ "$side" == "L" ]]; then
DIR=${2:-"."}
head -1 copy_to_local.dat | xargs -I'{}' rsync -P --relative -av -e 'ssh -p 4022' dforero@localhost:{} ${DIR}
fi

