from pyspark.sql import SparkSession
N = 5
movies_file = "hdfs:///user/zeppelin/sparkSQL/input/movies.csv"
ratings_file = "hdfs:///user/zeppelin/sparkSQL/input/ratings.csv"
output_dir = "hdfs:///user/zeppelin/sparkSQL/output"
spark = SparkSession.builder.appName("pyspark-topN-movies(SQL)").getOrCreate()

spark.sql("""
CREATE TABLE movies (
    movieId INT, 
    title STRING, 
    genres STRING
    )
USING csv
OPTIONS (HEADER=TRUE, 
         PATH="{}")
""".format(movies_file))

spark.sql("""
CREATE TABLE ratings (
    userId INT,
    movieId INT, 
    rating FLOAT
    )
USING csv
OPTIONS (HEADER=TRUE, 
         PATH="{}")
""".format(ratings_file))

spark.sql("""
CREATE TABLE ratings_normalized AS (
    SELECT movieId, 
           round(avg(rating), 2) AS avg_rating
    FROM ratings 
    GROUP BY movieId
    )
""")

spark.sql("""
CREATE TABLE movies_normalized AS (
    SELECT movieId,
           REGEXP_EXTRACT(title, "(.+)[ ]+[(](\\\d{4})[)]", 1) AS title,
           REGEXP_EXTRACT(title, '(.+)[ ]+[(](\\\d{4})[)]', 2) AS year,
           EXPLODE(SPLIT(genres, "[|]")) AS genre
    FROM movies
    )
""")

spark.sql("""
CREATE TABLE movies_nullable_title_year AS (
    SELECT movieId,
           genre,
    CASE
        WHEN ( title != "") THEN title
        ELSE NULL
           END AS title,
    CASE
        WHEN ( year != "") THEN year
        ELSE NULL
           END AS year
    FROM movies_normalized
    )
""")

spark.sql("""
CREATE TABLE movies_blanked AS (
    SELECT *
    FROM movies_nullable_title_year
    WHERE title IS NOT NULL OR year IS NOT NULL
)
""")

spark.sql("""
CREATE TABLE joined AS (
    SELECT genre,
           title,
           year,
           avg_rating
    FROM movies_blanked
    JOIN ratings_normalized
    ON movies_blanked.movieId=ratings_normalized.movieId
    )
""")

spark.sql("""
CREATE TABLE to_csv AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY genre ORDER BY avg_rating DESC) AS  rank
    FROM joined
    )
""")

spark.sql("""
CREATE TABLE final
USING csv
OPTIONS (HEADER=TRUE, 
         MODE="overwrite",
         PATH="{0}")
AS (
    SELECT genre,
           title,
           year,
           avg_rating
    FROM to_csv
    WHERE rank <={1}
    ORDER BY genre ASC, 
             avg_rating DESC
    )
DISTRIBUTE BY 1
""".format(output_dir, N))
