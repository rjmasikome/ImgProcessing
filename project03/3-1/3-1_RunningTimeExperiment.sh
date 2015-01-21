#!/bin/bash
mkdir -p data
rm -r data/*
cmake .
make
for (( SIGMA=2; SIGMA<=20; SIGMA+=2 ));
do
	for i in {1..10}
	do
	   ./3-1 $SIGMA 0
	done
done