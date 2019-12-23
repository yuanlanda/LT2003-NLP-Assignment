#!/bin/bash

keywords=$(awk '{print FILENAME $0}' | sed 's/[[:punct:]]//g')
keywords_arr=($(echo $keywords | tr ' ' ' '))

files=*.txt
index=$[$1-1]

for article in $files
do
  line_count=$(awk 'END{print NR}' $article)
  line=$(awk -F: -v i=$2 '(NR == i){print}' $article)
  word_arr=($(echo $line | tr ' ' ' '))
  for item in "${keywords_arr[@]}"
  do
    if [[ ${word_arr[$index]} == "$item" ]]
    then
      echo $article
      if [[ ! -d $3 ]]
      then
        mkdir $3
      fi
      cp $article $3/$article
      break
    fi
  done
done
