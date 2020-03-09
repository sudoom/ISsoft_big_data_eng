#!/usr/bin/env bash

movies="`pwd`/data/tmp/datalake/movies/movies.csv"




function gettr {
    current_path=`pwd`
    mkdir data
    dir_path=${current_path}/data
    cd ${dir_path}
    wget http://files.grouplens.org/datasets/movielens/ml-latest.zip
    file_path=${dir_path}/`ls`
    tar_path=${dir_path}/tar
    mkdir -p ${tar_path}
    unzip ${file_path} -d ${tar_path}
    tmp_path=${dir_path}/tmp/datalake
    mkdir -p ${tmp_path}
    cd ${current_path}
}

while [[ -n "$1" ]]; do
case "$1" in
    -getfiles) gettr;;
esac
shift
done
echo "`pwd`"
./1.sh && cat ${movies} | python mapper.py | sort | python reducer.py