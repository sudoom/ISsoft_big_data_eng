#!/usr/bin/env bash

mongoimport --db=topNmovies --collection=movies_raw --ignoreBlanks --type=csv --headerline --file=data/tmp/datalake/movies/movies.csv
mongoimport --db=topNmovies --collection=ratings_raw --ignoreBlanks --type=csv --headerline --file=data/tmp/datalake/ratings/ratings.csv

