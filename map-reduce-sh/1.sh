#!/usr/bin/env bash

links="links"
movies="movies"
ratings="ratings"
tags="tags"

dir_path=`pwd`/data
tar_path=${dir_path}/tar
tmp_path=${dir_path}/tmp/datalake
file_path=${dir_path}/ml-latest.zip
cd ${dir_path}

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
