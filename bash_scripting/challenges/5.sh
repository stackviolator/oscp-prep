#!/bin/bash

FILE=$1
LINES=$(cat $FILE)
filenames=()

for line in $LINES; do
	words=($(echo $line | tr "/" "\n"))
	for word in "${words[@]}"; do
		if [[ "$word" == *'.js'* ]]; then
			filenames+=("$word")
		fi
	done
done

arr=($(for file in "${filenames[@]}"; do echo ${file}; done| sort -u))

for i in "${arr[@]}"; do
	echo $i
done
