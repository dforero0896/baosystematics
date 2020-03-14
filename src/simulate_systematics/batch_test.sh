#!/bin/bash

RUN=./tests_analyt.py
JOBLIST=joblist_analyt.sh
echo Running ${RUN}.
for sigma in 0.2 0.3 0.4 0.5
do
$RUN $sigma 2500 && mv -v $JOBLIST ${sigma}.sh 
done

#./fit_tests.py

for grid in 250 25
do
$RUN 0.4 $grid && mv -v $JOBLIST ${grid}.sh 
done
