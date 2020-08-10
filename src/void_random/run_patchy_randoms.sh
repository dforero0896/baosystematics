#!/bin/bash
source ../.env
BOXES=patchy_results
for box in 1 5
do
for syst in smooth/parabola_0.8 #radialgauss
do
for space in real redshift
do
if [[ "$syst" == "radialgauss" ]]; then
kind=radial
elif [[ "$syst" == "smooth/parabola_0.8" ]]; then
kind=ang
else
exit 1
fi
echo "sbatch -p p4 -N2 -c16 -J void_ran --wrap='./box_void_ran_gen.sh ${WORKDIR}/${BOXES}/box${box}/${space}/${syst} 1 $kind'"
done
done
done

