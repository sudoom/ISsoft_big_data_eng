#!/usr/bin/env bash

movies="`pwd`/data/tmp/datalake/movies/movies.csv"
hadoop_streaming="$HADOOP_HOME/share/hadoop/tools/lib"

#hdfs dfs -mkdir -p /user/input
hdfs dfs -rm -r /user/input/output
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
    ./1.sh
    hdfs dfs -put ${movies} /user/input
	hadoop jar ${hadoop_streaming}/hadoop-streaming-3.2.1.jar \
	-input "/user/input/movies.csv" \
	-output "/user/input/output" \
	-file "`pwd`/mapper.py" \
	-mapper "python mapper.py -regexp love" \
	-file "`pwd`/reducer.py" \
	-reducer "python reducer.py"
	exit
    ;;
    *)
    echo "use flag -getfiles to download files"
    exit
    ;;
  esac
  shift
done

#hdfs dfs -put ${movies} /user/input
hadoop jar ${hadoop_streaming}/hadoop-streaming-3.2.1.jar \
-input "/user/input/movies.csv" \
-output "/user/input/output" \
-file "`pwd`/mapper.py" \
-mapper "python mapper.py -regexp bomb" \
-file "`pwd`/reducer.py" \
-reducer "python reducer.py"
