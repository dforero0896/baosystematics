#!/bin/env/bash
SEED=1005638091
side=$1
if [[ "$side" == "S" ]]; then
find ~+ -wholename "*nosyst*${SEED}*" | grep -v baofit > copy_to_local.dat
fi

if [[ "$side" == "L" ]]; then
DIR=${2:-"."}
head -1 copy_to_local.dat | xargs -I'{}' scp -P 4022 -u -v dforero@localhost:{} --parents ${DIR}
fi

