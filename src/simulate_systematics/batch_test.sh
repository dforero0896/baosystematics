#!/bin/bash

RUN=./tests.py

for sigma in 0.2 0.3 0.4 0.5
do
$RUN $sigma 2500 && mv -v joblist.sh ${sigma}.sh
done

./fit_tests.py

for grid in 250 25
do
$RUN 0.4 $grid && mv -v joblist.sh ${grid}.sh
done
