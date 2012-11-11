#!/bin/bash

#stop script if a command fails
set -e

input_file="data/all.dat"
if [ $# -ge 1 ] #if there's 1 or more parameters, the 1st one is filenam
then
    input_file=$1
fi

echo "Input file: $input_file"

# make a clean, custom header
cp header.dat czyste.dat
#only write numbers, only write if all 26 fields are present
awk '{ if ((NF == 26 || NF == 27) && $1 ~ /^[-0-9.+eE]+$/) print $0}' < $input_file >> czyste.dat

echo "Please enter the three variables you want to plot against"
echo "or press [Enter] to use last choice:"
cat last_choice_phase

read line
if [ "$line" = "" ]
then
    line=`cat last_choice_phase`
else
    echo $line > last_choice_phase
fi

arr=(`echo $line | tr " " "\n"`) # a = ("bolek", "lolek") -> array
num_elem=${#arr[@]}  # '#' -> liczba elementow
echo "Number of elements: " $num_elem

if [ $num_elem -ne 4 ]
then
    echo "Please enter 4 variables (plot will be created against 2 first vars)."
    exit 1
fi

ruby select_columns.rb $line

mv dane_tmp.dat dane.dat

python lines.py

