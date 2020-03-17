#!/bin/bash

RUN=./tests_analyt.py
JOBLIST=joblist_analyt.sh
PREFIX=$1
echo Running ${RUN}.
for sigma in 0.2 0.3 0.4 0.5
do
$RUN $sigma 2500 && mv -v $JOBLIST ${PREFIX}${sigma}.sh 
done

#./fit_tests.py

for grid in 250 25
do
$RUN 0.4 $grid && mv -v $JOBLIST ${PREFIX}${grid}.sh 
done

./void_tests_analytic.py
split -d -l 2 joblist_void_analyt.sh ${PREFIX}void
