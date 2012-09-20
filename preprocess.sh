#!/bin/bash

#stop script if a command fails
set -e

# make a clean, custom header
cp header.dat czyste.dat
#only write numbers, only write if all 26 fields are present
awk '{ if (NF == 26 && $1 ~ /^[0-9]+$/) print $0}' < wszystkie.dat >> czyste.dat

echo "Please enter the three variables you want to plot against"
echo "or press [Enter] to use last choice:"
cat last_choice

read line
if [ "$line" = "" ]
then
    line=`cat last_choice`
else
    echo $line > last_choice
fi

arr=(`echo $line | tr " " "\n"`) # a = ("bolek", "lolek") -> array

num_elem=${#arr[@]}  # '#' -> liczba elementow
echo "Number of elements: " $num_elem

if [ $num_elem -le 3 ]
then
    echo "Please enter 3 variables (x,y,z) to plot against."
    exit 1
fi

ruby select_columns.rb $line

ruby check_dups.rb dane_tmp.dat dane.dat --avg

python contour.py
