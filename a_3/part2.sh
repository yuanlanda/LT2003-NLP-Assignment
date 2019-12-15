#!/bin/bash

for article in $3
do
  line_count=$(awk 'END{print NR}' $article)
  word_found=false
  for (( i=1; i<=$line_count; i++ ))
  do
    if [[ $word_found = false ]]
    then
      line=$(awk -v i=$i '(NR == i){print}' $article | tr -d '[:punct:]')
      word_count=$(echo $line | wc -w)
      word_arr=($(echo $line | tr ' ' ' '))
      for (( j=$[$1-1]; j<=word_count; j++ ))
      do
        if [[ ${word_arr[j]} = $2 ]]
        then
          echo $article
          word_found=true
          break
        fi
      done
    fi
  done
done
