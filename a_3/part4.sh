#!/bin/bash

keywords=$(awk '{print FILENAME $0}' | sed 's/[[:punct:]]//g')
keywords_arr=($(echo $keywords | tr ' ' ' '))

files=*.txt
index=$[$1-1]
echo $keywords
echo ${keywords_arr[@]}

for article in $files
do
  line_count=$(awk 'END{print NR}' $article)
  word_found=false
  for (( i=$2; i<=$line_count; i++ ))
  do
    if [[ $word_found = false ]]
    then
      line=$(awk -F: -v i=$i '(NR == i){print}' $article)
      word_arr=($(echo $line | tr ' ' ' '))
      for item in "${keywords_arr[@]}"
      do
        if [[ ${word_arr[$index]} == "$item" ]]
        then
          echo $article
          if [[ ! -d $3 ]]
          then
            echo 'not exist'
            mkdir $3
          fi
          cp $article $3/$article
          word_found=true
          break
        fi
      done
    fi
  done
done
