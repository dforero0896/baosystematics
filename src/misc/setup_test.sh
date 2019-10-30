#!/usr/bin/env bash
RAW_DIR=$1
TEST_DIR=$2
OVERWRITE=$3
if [[ $# -ne 3 ]]; then
	echo ERROR: Unexpected number of arguments.
	echo USAGE: $0 RAW_DIR TEST_DIR OVERWRITE
	exit 1
fi
#Get random data
if [[ ! -e $TEST_DIR ]]; then
	mkdir $TEST_DIR
fi
if [[ $OVERWRITE -eq 1 ]]; then
	rm -rf $TEST_DIR/*
fi

for d in $(ls -d $RAW_DIR/* |grep ^.*NGC.*dat.* | shuf -n 9); do
	echo Copying $d
	cp $d $TEST_DIR
	cp $(echo $d | sed -e "s/\.dat\./.ran./g") $TEST_DIR
	cp $(echo $d | sed -e "s/\.dat\./.ran./g" | sed -e "s/NGC/SGC/g") $TEST_DIR
	cp $(echo $d | sed -e "s/NGC/SGC/g") $TEST_DIR
done

