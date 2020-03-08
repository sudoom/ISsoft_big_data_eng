#!/usr/bin/env bash

links="links"
movies="movies"
ratings="ratings"
tags="tags"

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
for var in $(ls ${tar_path}/`ls ${tar_path}`); do
case ${var} in
    "${links}.csv")
      mkdir ${tmp_path}/${links}
      cp ${tar_path}/`ls ${tar_path}`/${var} ${tmp_path}/${links}
      ;;
    "${movies}.csv")
      mkdir ${tmp_path}/${movies}
      cp ${tar_path}/`ls ${tar_path}`/${var} ${tmp_path}/${movies}
      ;;
    "${ratings}.csv")
      mkdir ${tmp_path}/${ratings}
      cp ${tar_path}/`ls ${tar_path}`/${var} ${tmp_path}/${ratings}
      ;;
    "${tags}.csv")
      mkdir ${tmp_path}/${tags}
      cp ${tar_path}/`ls ${tar_path}`/${var} ${tmp_path}/${tags}
      ;;
    *)
      continue
esac
done

rm -R tar
rm ${file_path}
