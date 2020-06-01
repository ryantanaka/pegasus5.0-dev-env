#!/bin/bash

INPUT_FILE=$1
OUTPUT_FILE=$2

cp $INPUT_FILE $OUTPUT_FILE

words=("carousel_horse" "snake" "books")

for w in "${words[@]}"
do
    sed -i -e "s/$w/:$w:/g" $OUTPUT_FILE
done
