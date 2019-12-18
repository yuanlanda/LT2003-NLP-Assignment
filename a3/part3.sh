#!/bin/bash

path_1=$2
files_1=$(ls $path_1)

path_1_word_count_arr=()
i=0
for article_1 in $files_1
do
  line_count_1=$(wc -w $path_1/$article_1)
  path_1_word_count_arr[$i]=$line_count_1
  i=$[i+1]
done

IFS=$'\n'
sorted_path_1_arr=( $(for val in "${path_1_word_count_arr[@]}" 
do
    echo "$val"
done | sort -nr)
)


path_2=$3
files_2=$(ls $path_2)
path_2_word_count_arr=()
i=0
for article_2 in $files_2
do
  line_count_2=$(wc -w $path_2/$article_2)
  path_2_word_count_arr[$i]=$line_count_2
  i=$[i+1]
done

IFS=$'\n'
sorted_path_2_arr=( $(for val in "${path_2_word_count_arr[@]}" 
do
    echo "$val"
done | sort -nr)
)


j=0
while(( $j < $1 ))
do
  str_1=$(echo ${sorted_path_1_arr[j]} | sed 's/^[[:space:]]*[0-9]*[ ]//')
  str_2=$(echo ${sorted_path_2_arr[j]} | sed 's/^[[:space:]]*[0-9]*[ ]//')
  printf "%-30s  %-30s\n" "$str_1" "$str_2"
  j=$[j+1]
done
