#!/bin/bash

#stop script if a command fails
set -e

if [ "$#" -eq 0 ]; then #standard operation

  # make a clean, custom header
  cp header.dat czyste.dat
  #only write numbers, only write if all 26 fields are present
  awk '{ if ((NF == 26 || NF == 27) && $1 ~ /^[-0-9.+eE]+$/) print $0}' < data/wszystkie.dat >> czyste.dat

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
      echo "Please enter 3 variables (x,y,z) to plot against and at least one constraint (e.g. diam=60)."
      exit 1
  fi

  line=$line+" alpha"
  ruby select_columns.rb $line

  ruby check_dups.rb dane_tmp.dat dane.dat --avg

  if [ -e 'clicks.dat' ]
  then
      rm clicks.dat
  fi

  python contour.py

else
  if [ "$#" -ne 4 ]; then
    echo "Incorrect argument count! Use: preprocess.sh file x y title"
    exit 77
  fi

  cp header.dat czyste.dat
  awk '{ if ((NF == 26 || NF == 27) && $1 ~ /^[-0-9.+eE]+$/) print $0}' < $1 >> czyste.dat

  line="$2 $3 sq alpha"
  ruby select_columns.rb $line
  ruby check_dups.rb dane_tmp.dat dane.dat --avg
  python contour.py $4
fi
