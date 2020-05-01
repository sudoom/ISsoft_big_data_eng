#!/usr/bin/env bash

mongoexport --db=topNmovies --collection=to_csv --type=csv --fields=genre,title,year,avg_rating --out=output/output.csv