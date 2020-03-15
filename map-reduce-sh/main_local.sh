#!/usr/bin/env bash

movies="`pwd`/data/tmp/datalake/movies/movies.csv"


#######################################
# Download dataset and unzip.
#######################################
function download {
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
    -getfiles)
    download
    ./1.sh && cat ${movies} | python mapper.py | sort | python reducer.py
    ;;
    *)
    echo "use flag -getfiles to download files"
    exit
    ;;
  esac
  shift
done

cat ${movies} | python mapper.py -regexp bomb | sort | python reducer.py