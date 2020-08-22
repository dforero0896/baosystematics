#!/bin/env/bash
SEED=1005638091
side=$1
if [[ "$side" == "S" ]]; then
find ~+ -wholename "*nosyst*${SEED}*" | grep -v baofit > copy_to_local.dat
sed -e "s/baosystematics/baosystematics\/./g" copyt_to_local.dat
fi

if [[ "$side" == "L" ]]; then
DIR=${2:-"."}
head -1 copy_to_local.dat | xargs -I'{}' rsync -av -e 'ssh -p 4022' dforero@localhost:{} --parents ${DIR}
fi

