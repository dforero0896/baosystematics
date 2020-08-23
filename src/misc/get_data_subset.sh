#!/bin/env/bash
SEED=1005638091
side=$1
if [[ "$side" == "S" ]]; then
echo Running server side
find ~+ -wholename "*nosyst*${SEED}*" | grep -v baofit > copy_to_local.dat.TMP
sed -e "s/baosystematics/baosystematics\/./g" copy_to_local.dat.TMP > copy_to_local.dat
rm -v copy_to_local.dat.TMP
elif [[ "$side" == "L" ]]; then
DIR=${2:-"."}
echo Running local side
echo Saving in ${DIR}
rsync -P --relative -av -e 'ssh -p 4022' --files-from=:/hpcstorage/dforero/projects/baosystematics/copy_to_local.dat dforero@localhost:/ ${DIR}
else
echo Option not understood
exit 1
fi

