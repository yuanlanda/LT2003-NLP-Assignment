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

sortWords(){
  word_arr=()
  line_count=$(awk 'END{print NR}' $1)
  for (( i=1; i<=$line_count; i++ ))
  do
    line=$(awk -v i=$i '(NR == i){print}' $1)
    line_arr=($(echo $line | tr ' ' '\n'))
    for word in ${line_arr[@]}
    do
      word_arr+=($word)
    done
  done

  sorted_arr=( $(for val in "${word_arr[@]}" 
  do
    echo "$val"
  done | sort | uniq )
  )

  printf "%s\n" "${sorted_arr[@]}" > $1
}


j=0
while(( $j < $1 ))
do
  str_1=$(echo ${sorted_path_1_arr[j]} | sed 's/^[[:space:]]*[0-9]*[ ]//')
  str_2=$(echo ${sorted_path_2_arr[j]} | sed 's/^[[:space:]]*[0-9]*[ ]//')
  printf "%-30s  %-30s\n" "$str_1" "$str_2"
  if [[ ! -d $4 ]]
  then
    mkdir $4
  fi

  file_path=$4/$j'.txt'
  cp $str_1 $file_path
  cat $str_2 >> $file_path
  sortWords $file_path
  j=$[j+1]
done
