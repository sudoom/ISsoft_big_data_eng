#!/usr/bin/env bash

movies="`pwd`/data/tmp/datalake/movies/movies.csv"
./1.sh && cat ${movies} | python mapper.py -regexp bomb | sort | python reducer.py