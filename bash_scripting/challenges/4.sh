#!/bin/bash

file=$1

if [ -e $file ]; then
	echo "File exists"
else
	echo "File does not exist"
fi
