#!/bin/bash

for article in $2
do
  line_count=$(wc -l $article | sed 's/[:space:].*$//g')
  if [ $line_count -gt $1 ]
  then
    echo $article
  fi
done
